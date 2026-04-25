import networkx as nx
import sys
import os
from math import radians, cos, sin, asin, sqrt
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.stops import STOPS, ROUTES

def haversine(lat1, lon1, lat2, lon2):
    """Calculate the great circle distance between two points on the earth."""
    R = 6371  # Earth radius in kilometers
    dLat = radians(lat2 - lat1)
    dLon = radians(lon2 - lon1)
    a = sin(dLat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dLon / 2)**2
    c = 2 * asin(sqrt(a))
    return R * c

def build_graph():
    G = nx.DiGraph()  # directed graph — buses go in one direction per segment

    # Add all stops as nodes
    for name, info in STOPS.items():
        G.add_node(name, **info)

    # Add edges from each route
    for route_name, route in ROUTES.items():
        stops = route["stops"]
        times = route["times"]
        wait  = route["frequency_min"] / 2  # avg wait = half the headway

        for i in range(len(stops) - 1):
            src = stops[i]
            dst = stops[i + 1]
            travel_time = times[i]
            total_cost  = travel_time + wait

            # If edge already exists, keep the faster one
            if G.has_edge(src, dst):
                if G[src][dst]["weight"] > total_cost:
                    G[src][dst].update({
                        "weight": total_cost,
                        "travel_time": travel_time,
                        "wait_time": wait,
                        "route": route_name,
                    })
            else:
                G.add_edge(src, dst,
                    weight=total_cost,
                    travel_time=travel_time,
                    wait_time=wait,
                    route=route_name,
                )

    # SENSATIONAL FEATURE: Add walking interchanges between nearby stops (max 300m)
    # This allows the optimizer to suggest walking between stops to switch lines.
    stop_names = list(STOPS.keys())
    for i in range(len(stop_names)):
        for j in range(i + 1, len(stop_names)):
            s1, s2 = stop_names[i], stop_names[j]
            dist = haversine(STOPS[s1]["lat"], STOPS[s1]["lon"], STOPS[s2]["lat"], STOPS[s2]["lon"])
            
            if dist <= 0.3:  # 300 meters
                # Walking speed avg 5km/h => 1km in 12 mins.
                walk_time = dist * 12
                # Add bi-directional walking edges
                for u, v in [(s1, s2), (s2, s1)]:
                    if not G.has_edge(u, v) or G[u][v]["weight"] > walk_time:
                        G.add_edge(u, v,
                            weight=walk_time,
                            travel_time=walk_time,
                            wait_time=0,
                            route="Walking Transfer")

    _check_connectivity(G)
    return G

def _check_connectivity(G):
    """Internal helper to debug dead-end stops."""
    dead_ends = [node for node in G.nodes if G.out_degree(node) == 0]
    isolated = [node for node in G.nodes if G.degree(node) == 0]
    
    if dead_ends:
        print(f"  [DEBUG] Found {len(dead_ends)} 'Sink' stops (can't leave): {', '.join(dead_ends[:5])}...")
    if isolated:
        print(f"  [WARNING] Found {len(isolated)} isolated stops (no routes): {', '.join(isolated[:5])}...")

if __name__ == "__main__":
    G = build_graph()
    print(f"Nodes (stops): {G.number_of_nodes()}")
    print(f"Edges (segments): {G.number_of_edges()}")
    print("\nSample edges:")
    for u, v, data in list(G.edges(data=True))[:5]:
        print(f"  {u} → {v} | cost: {data['weight']:.1f} min | route: {data['route']}")