from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from graph.builder import build_graph
from routing.dijkstra import find_best_route
from routing.stop_resolver import resolve_stop
from data.stops import STOPS
import uvicorn

app = FastAPI(title="Kathmandu Transit API")

# Enable CORS so your frontend can talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# SENSATIONAL FEATURE: Build the graph once at startup.
# This makes the /route API response nearly instantaneous.
GLOBAL_GRAPH = build_graph()

@app.get("/stops")
def get_stops():
    """Returns all available stops for the frontend dropdowns."""
    return [{"id": name, "lat": data["lat"], "lon": data["lon"]} for name, data in STOPS.items()]

@app.get("/route")
def get_route(origin: str, destination: str):
    """Calculates the best route and returns it as JSON."""
    print("\n" + "="*40)
    print(f"Incoming Route Request")
    print(f"Origin:      {origin}")
    print(f"Destination: {destination}")
    # Resolve stops (fuzzy matching logic)
    origin_res = resolve_stop(origin)
    dest_res = resolve_stop(destination)

    if not origin_res["matched"] or not dest_res["matched"]:
        missing = []
        if not origin_res["matched"]: missing.append(f"Origin '{origin}'")
        if not dest_res["matched"]: missing.append(f"Destination '{destination}'")
        raise HTTPException(status_code=404, detail=f"Could not resolve: {', '.join(missing)}")

    # Calculate routes using the pre-built global graph
    comparison_result = find_best_route(origin_res["matched"], dest_res["matched"], G=GLOBAL_GRAPH)
    
    if "error" in comparison_result:
        raise HTTPException(status_code=400, detail=comparison_result["error"])

    optimal_route = comparison_result["optimal_route"]
    naive_route = comparison_result["naive_route"]

    # Add coordinates for the frontend to draw the line for both routes
    optimal_route["coordinates"] = [[STOPS[s]["lat"], STOPS[s]["lon"]] for s in optimal_route["path"] if s in STOPS]
    naive_route["coordinates"] = [[STOPS[s]["lat"], STOPS[s]["lon"]] for s in naive_route["path"] if s in STOPS]

    print("Route calculated successfully. Sending back to frontend...")
    return comparison_result

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)