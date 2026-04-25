from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import sys
from pathlib import Path
import folium
import requests
import traceback

sys.path.append(str(Path(__file__).parent))

from data.stops import STOPS

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class RouteRequest(BaseModel):
    origin: str
    destination: str

def find_stop_key(stop_name):
    """Find the correct key in STOPS dictionary"""
    if not stop_name:
        return None
    
    if stop_name in STOPS:
        return stop_name
    
    for key in STOPS:
        if key.lower() == stop_name.lower():
            return key
    
    for key in STOPS:
        if stop_name.lower() in key.lower() or key.lower() in stop_name.lower():
            print(f"    Partial match: '{stop_name}' → '{key}'")
            return key
    
    print(f"    ❌ No match found for '{stop_name}'")
    return None

def get_road_coordinates(stop_sequence):
    """Get real road coordinates from OSRM"""
    all_coords = []
    print(f"\n🔍 Getting coordinates for {len(stop_sequence)} stops: {stop_sequence}")
    
    for i in range(len(stop_sequence) - 1):
        src = stop_sequence[i]
        dst = stop_sequence[i + 1]
        
        src_key = find_stop_key(src)
        dst_key = find_stop_key(dst)
        
        if not src_key or not dst_key:
            print(f"  ❌ Skipping segment: {src} → {dst}")
            continue
        
        src_lon = STOPS[src_key]["lon"]
        src_lat = STOPS[src_key]["lat"]
        dst_lon = STOPS[dst_key]["lon"]
        dst_lat = STOPS[dst_key]["lat"]
        
        print(f"  ✅ {src_key} → {dst_key}")
        
        url = f"http://router.project-osrm.org/route/v1/driving/{src_lon},{src_lat};{dst_lon},{dst_lat}?overview=full&geometries=geojson"
        
        try:
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                data = response.json()
                if data["code"] == "Ok" and data["routes"]:
                    coords = data["routes"][0]["geometry"]["coordinates"]
                    segment = [[c[1], c[0]] for c in coords]
                    if all_coords:
                        all_coords.extend(segment[1:])
                    else:
                        all_coords.extend(segment)
                    print(f"      ✅ Got {len(segment)} road points")
                else:
                    all_coords.append([src_lat, src_lon])
                    all_coords.append([dst_lat, dst_lon])
                    print(f"      ⚠️ Using straight line")
            else:
                all_coords.append([src_lat, src_lon])
                all_coords.append([dst_lat, dst_lon])
                print(f"      ⚠️ HTTP {response.status_code}, using straight line")
        except Exception as e:
            all_coords.append([src_lat, src_lon])
            all_coords.append([dst_lat, dst_lon])
            print(f"      ❌ Error, using straight line")
    
    print(f"📊 Total coordinates: {len(all_coords)}\n")
    return all_coords

@app.post("/api/map-html")
def get_map_html(request: RouteRequest):
    try:
        print(f"\n{'='*50}")
        print(f"📍 Route Request: {request.origin} → {request.destination}")
        print(f"{'='*50}")
        
        api_response = requests.get(
            f'http://localhost:8000/route',
            params={'origin': request.origin, 'destination': request.destination},
            timeout=30
        )
        
        if api_response.status_code != 200:
            error_html = f"""
            <div style="font-family: sans-serif; padding: 20px; text-align: center;">
                <div style="font-size: 48px; margin-bottom: 16px;">❌</div>
                <h3>Error: Could not find route</h3>
                <p>API returned status {api_response.status_code}</p>
                <p>From: <b>{request.origin}</b> To: <b>{request.destination}</b></p>
            </div>
            """
            return HTMLResponse(content=error_html, status_code=404)
        
        result = api_response.json()
        
    except Exception as e:
        error_html = f"""
        <div style="font-family: sans-serif; padding: 20px; text-align: center;">
            <div style="font-size: 48px; margin-bottom: 16px;">⚠️</div>
            <h3>Connection Error</h3>
            <p>Could not connect to the routing backend.</p>
            <p>Make sure server.py is running on port 8000.</p>
        </div>
        """
        return HTMLResponse(content=error_html, status_code=500)
    
    # Extract routes
    optimal_path = None
    naive_path = None
    optimal_time = 30
    naive_time = 60
    optimal_transfers = 0
    naive_transfers = 0
    
    if 'optimal_route' in result:
        optimal = result['optimal_route']
        optimal_path = optimal.get('path')
        optimal_time = optimal.get('total_time', 30)
        optimal_transfers = optimal.get('transfers', 0)
        print(f"OPTIMAL ROUTE: {optimal_path}")
        print(f"OPTIMAL TIME: {optimal_time} min")
    
    if 'naive_route' in result:
        naive = result['naive_route']
        naive_path = naive.get('path')
        naive_time = naive.get('total_time', 60)
        naive_transfers = naive.get('transfers', 0)
        print(f"NAIVE ROUTE: {naive_path}")
        print(f"NAIVE TIME: {naive_time} min")
    
    if not optimal_path:
        error_html = f"""
        <div style="font-family: sans-serif; padding: 20px; text-align: center;">
            <div style="font-size: 48px; margin-bottom: 16px;">🗺️</div>
            <h3>No Route Found</h3>
            <p>Could not find a path between <b>{request.origin}</b> and <b>{request.destination}</b>.</p>
        </div>
        """
        return HTMLResponse(content=error_html, status_code=404)
    
    # Determine better route
    better_path = optimal_path
    better_time = optimal_time
    better_transfers = optimal_transfers
    better_label = "Optimal Route (Dijkstra)"
    worse_path = naive_path
    worse_time = naive_time
    
    if naive_path and naive_time < optimal_time:
        better_path = naive_path
        better_time = naive_time
        better_transfers = naive_transfers
        better_label = "Better Route (Alternative)"
        worse_path = optimal_path
        worse_time = optimal_time
    
    # Create map
    m = folium.Map(location=[27.7041, 85.3145], zoom_start=13, tiles="CartoDB positron")
    
    # Add stops
    stops_added = 0
    for name, info in STOPS.items():
        if stops_added > 200:
            break
        is_on_path = name in (better_path or [])
        radius = 6 if is_on_path else 3
        color = "#1D9E75" if is_on_path else "#d1d5db"
        fill_opacity = 0.9 if is_on_path else 0.4
        
        folium.CircleMarker(
            location=[info["lat"], info["lon"]],
            radius=radius,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=fill_opacity,
            tooltip=f"{name} {'✅' if is_on_path else ''}",
        ).add_to(m)
        stops_added += 1
    
    # Add route lines
    if worse_path and len(worse_path) > 1:
        worse_coords = get_road_coordinates(worse_path)
        if worse_coords and len(worse_coords) > 1:
            folium.PolyLine(
                locations=worse_coords,
                color="#9ca3af",
                weight=4,
                opacity=0.6,
                dash_array='10, 10',
                tooltip=f"⚠️ Alternative Route — {worse_time} min",
            ).add_to(m)
    
    if better_path and len(better_path) > 1:
        better_coords = get_road_coordinates(better_path)
        if better_coords and len(better_coords) > 1:
            folium.PolyLine(
                locations=better_coords,
                color="#1D9E75",
                weight=6,
                opacity=0.95,
                tooltip=f"✅ {better_label} — {better_time} min",
            ).add_to(m)
        else:
            straight_coords = []
            for stop in better_path:
                stop_key = find_stop_key(stop)
                if stop_key and stop_key in STOPS:
                    straight_coords.append([STOPS[stop_key]["lat"], STOPS[stop_key]["lon"]])
            if len(straight_coords) > 1:
                folium.PolyLine(
                    locations=straight_coords,
                    color="#1D9E75",
                    weight=6,
                    opacity=0.95,
                    tooltip=f"✅ {better_label} — {better_time} min",
                ).add_to(m)
    
    # Add markers
    start_key = find_stop_key(request.origin)
    if start_key:
        folium.Marker(
            location=[STOPS[start_key]["lat"], STOPS[start_key]["lon"]],
            tooltip=f"🚩 START: {request.origin}",
            icon=folium.Icon(color="green", icon="play", prefix="fa"),
        ).add_to(m)
    
    end_key = find_stop_key(request.destination)
    if end_key:
        folium.Marker(
            location=[STOPS[end_key]["lat"], STOPS[end_key]["lon"]],
            tooltip=f"🏁 END: {request.destination}",
            icon=folium.Icon(color="red", icon="flag", prefix="fa"),
        ).add_to(m)
    
    # Calculate savings
    time_saved = abs(worse_time - better_time) if worse_time else 0
    savings_percent = round((time_saved / worse_time) * 100) if worse_time > 0 else 0
    
    # Info panel
    path_str = " → ".join(better_path[:15])
    
    comparison_html = ""
    if worse_path and worse_time:
        if better_time < worse_time:
            comparison_html = f"""
            <hr style="margin: 10px 0; border-color: #e5e7eb;">
            <div style="font-size: 11px; color: #666;">
                <div>📉 Alternative route: {worse_time} min</div>
                <div style="color: #1D9E75; font-weight: bold; margin-top: 5px;">
                    ⏱️ YOU SAVE: {time_saved} min ({savings_percent}% faster)
                </div>
                <div style="font-size: 10px; color: #888; margin-top: 8px;">
                    🟢 Solid green = Optimal route<br>
                    ⚪ Dashed gray = Alternative route
                </div>
            </div>
            """
        else:
            comparison_html = f"""
            <hr style="margin: 10px 0; border-color: #e5e7eb;">
            <div style="font-size: 11px; color: #666;">
                <div>📊 This is the only available route</div>
            </div>
            """
    
    info_html = f"""
    <div style="position: fixed; bottom: 20px; left: 20px; z-index: 1000;
                background: white; padding: 14px 18px; border-radius: 12px;
                border-left: 5px solid #1D9E75; font-family: 'Segoe UI', Arial, sans-serif;
                box-shadow: 0 4px 20px rgba(0,0,0,0.2); min-width: 260px;
                backdrop-filter: blur(2px); max-width: 300px;">
        <div style="font-weight: bold; color: #1D9E75; font-size: 14px; margin-bottom: 8px;">
            ✅ {better_label}
        </div>
        <div style="font-size: 12px; margin: 5px 0;">
            <span style="color: #555;">📍 From:</span> <b>{request.origin}</b>
        </div>
        <div style="font-size: 12px; margin: 5px 0;">
            <span style="color: #555;">🎯 To:</span> <b>{request.destination}</b>
        </div>
        <div style="font-size: 12px; margin: 5px 0;">
            <span style="color: #555;">⏱️ Time:</span> <b style="color: #1D9E75;">{better_time} minutes</b>
        </div>
        <div style="font-size: 12px; margin: 5px 0;">
            <span style="color: #555;">🔄 Transfers:</span> <b>{better_transfers}</b>
        </div>
        {comparison_html}
        <details style="margin-top: 10px;">
            <summary style="font-size: 11px; cursor: pointer; color: #1D9E75;">🗺️ View route path</summary>
            <div style="font-size: 10px; margin-top: 6px; padding: 8px; background: #f3f4f6; border-radius: 6px; color: #333; word-break: break-all;">
                {path_str}
            </div>
        </details>
        <div style="font-size: 10px; color: #888; margin-top: 8px; text-align: center; border-top: 1px solid #e5e7eb; padding-top: 8px;">
            🚀 Dijkstra's Algorithm | Real road routing via OSRM
        </div>
    </div>
    """
    
    m.get_root().html.add_child(folium.Element(info_html))
    
    print(f"✅ Map generated successfully for {request.origin} → {request.destination}\n")
    return HTMLResponse(content=m.get_root().render(), status_code=200)

if __name__ == "__main__":
    import uvicorn
    print("="*60)
    print("🗺️ KATHMANDU TRANSPORT OPTIMIZER - MAP API")
    print("📍 Server running on: http://localhost:8002")
    print("📡 Endpoint: POST /api/map-html")
    print("="*60)
    uvicorn.run(app, host="127.0.0.1", port=8002)