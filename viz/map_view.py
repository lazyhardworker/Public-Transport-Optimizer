import folium
import requests
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from routing.dijkstra import find_best_route
from data.stops import STOPS


def get_road_coordinates(stop_sequence):
    all_coords = []

    for i in range(len(stop_sequence) - 1):
        src = stop_sequence[i]
        dst = stop_sequence[i + 1]

        src_lon = STOPS[src]["lon"]
        src_lat = STOPS[src]["lat"]
        dst_lon = STOPS[dst]["lon"]
        dst_lat = STOPS[dst]["lat"]

        url = (
            "http://router.project-osrm.org/route/v1/driving/"
            + str(src_lon) + "," + str(src_lat)
            + ";" + str(dst_lon) + "," + str(dst_lat)
            + "?overview=full&geometries=geojson"
        )

        try:
            response = requests.get(url, timeout=10)
            data = response.json()
            print("  OSRM " + src + " to " + dst + ": " + data["code"] + ", points: " + str(len(data["routes"][0]["geometry"]["coordinates"])))

            if data["code"] == "Ok":
                coords = data["routes"][0]["geometry"]["coordinates"]
                segment = [[c[1], c[0]] for c in coords]
                if all_coords:
                    all_coords.extend(segment[1:])
                else:
                    all_coords.extend(segment)
            else:
                print("  FALLBACK: " + src + " to " + dst)
                all_coords.append([src_lat, src_lon])
                all_coords.append([dst_lat, dst_lon])

        except Exception as e:
            print("  FALLBACK exception: " + src + " to " + dst + " — " + str(e))
            all_coords.append([src_lat, src_lon])
            all_coords.append([dst_lat, dst_lon])

    print("  Total road coordinates: " + str(len(all_coords)))
    return all_coords


def create_map(optimal_route_data, naive_route_data, output_file="map.html"):
    if "error" in optimal_route_data or "error" in naive_route_data:
        print("Error: Cannot create map due to routing error.")
        return

    origin = optimal_route_data["origin"]
    destination = optimal_route_data["destination"]

    m = folium.Map(
        location=[27.7041, 85.3145],
        zoom_start=13,
        tiles="CartoDB positron"
    )

    for name, info in STOPS.items():
        is_on_path = name in optimal_route_data["path"] or name in naive_route_data["path"]
        folium.CircleMarker(
            location=[info["lat"], info["lon"]],
            radius=6 if is_on_path else 4,
            color="#1D9E75" if is_on_path else "#888780",
            fill=True,
            fill_color="#1D9E75" if is_on_path else "#B4B2A9",
            fill_opacity=0.9 if is_on_path else 0.5,
            tooltip=name,
        ).add_to(m)

        if is_on_path:
            folium.Marker(
                location=[info["lat"] + 0.0012, info["lon"]],
                icon=folium.DivIcon(
                    html="<div style='font-size:11px;font-weight:600;color:#0F6E56;white-space:nowrap'>" + name + "</div>",
                    icon_size=(120, 20),
                    icon_anchor=(0, 0),
                )
            ).add_to(m)

    print("  Fetching road route from OSRM...")
    
    # Draw Optimal Route
    optimal_road_coords = get_road_coordinates(optimal_route_data["path"])
    folium.PolyLine(
        locations=optimal_road_coords,
        color="#1D9E75", # Green for optimal
        weight=5,
        opacity=0.85,
        tooltip=f"Optimal Route — {optimal_route_data['total_time']} min",
    ).add_to(m)

    # Draw Naive Route (Chaos Path)
    naive_road_coords = get_road_coordinates(naive_route_data["path"])
    folium.PolyLine(
        locations=naive_road_coords,
        color="#E74C3C", # Red for naive/chaos
        weight=3,
        opacity=0.7,
        dash_array="5, 5", # Dashed line for distinction
        tooltip=f"Naive Route — {naive_route_data['total_time']} min",
    ).add_to(m)

    folium.Marker(
        location=[STOPS[origin]["lat"], STOPS[origin]["lon"]],
        icon=folium.Icon(color="blue", icon="play"),
    ).add_to(m)

    folium.Marker(
        location=[STOPS[destination]["lat"], STOPS[destination]["lon"]],
        tooltip="END: " + destination,
        icon=folium.Icon(color="red", icon="flag"),
    ).add_to(m)

    # Create summary HTML for both routes
    optimal_path_str = " → ".join(optimal_route_data["path"])
    naive_path_str = " → ".join(naive_route_data["path"])

    summary_html = (
        "<div style='position:fixed;bottom:30px;left:30px;z-index:1000;"
        "background:white;padding:14px 18px;border-radius:10px;"
        "border:1.5px solid #1D9E75;font-family:sans-serif;"
        "box-shadow:0 2px 8px rgba(0,0,0,0.15);min-width:200px'>"
        "<div style='font-size:13px;font-weight:700;color:#0F6E56;margin-bottom:8px'>Route Comparison</div>"
        "<div style='font-size:12px;color:#333;margin-bottom:4px'><b>From:</b> " + origin + "</div>"
        "<div style='font-size:12px;color:#333;margin-bottom:4px'><b>To:</b> " + destination + "</div>"
        "<hr style='border:none;border-top:1px solid #eee;margin:8px 0'>"
        "<div style='font-size:12px;font-weight:600;color:#0F6E56;margin-bottom:4px'>Optimal (Traffic-Aware)</div>"
        "<div style='font-size:12px;color:#333;margin-bottom:3px'>Path: " + optimal_path_str + "</div>"
        "<div style='font-size:12px;color:#333;margin-bottom:3px'>Total time: <b>" + str(optimal_route_data["total_time"]) + " min</b></div>"
        "<div style='font-size:12px;color:#333;margin-bottom:3px'>Travel time: " + str(optimal_route_data["travel_time"]) + " min</div>"
        "<div style='font-size:12px;color:#333;margin-bottom:3px'>Wait time: " + str(optimal_route_data["wait_time"]) + " min</div>"
        "<div style='font-size:12px;color:#333'>Transfers: " + str(optimal_route_data["transfers"]) + "</div>"
        "<hr style='border:none;border-top:1px solid #eee;margin:8px 0'>"
        "<div style='font-size:12px;font-weight:600;color:#E74C3C;margin-bottom:4px'>Naive (Actual Time)</div>"
        "<div style='font-size:12px;color:#333;margin-bottom:3px'>Path: " + naive_path_str + "</div>"
        "<div style='font-size:12px;color:#333;margin-bottom:3px'>Total time: <b>" + str(naive_route_data["total_time"]) + " min</b></div>"
        "<div style='font-size:12px;color:#333;margin-bottom:3px'>Travel time: " + str(naive_route_data["travel_time"]) + " min</div>"
        "<div style='font-size:12px;color:#333;margin-bottom:3px'>Wait time: " + str(naive_route_data["wait_time"]) + " min</div>"
        "<div style='font-size:12px;color:#333'>Transfers: " + str(naive_route_data["transfers"]) + "</div>"
        "</div>"
    )

    m.get_root().html.add_child(folium.Element(summary_html))
    m.save(output_file)
    print("  Map saved to: " + output_file)