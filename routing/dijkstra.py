import networkx as nx
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from graph.builder import build_graph
from routing.realtime_service import get_edge_weight

def _calculate_route_details(G, origin, destination, weight_func):
    """Helper to calculate a single route's path, cost, and legs."""
    try:
        cost, path = nx.bidirectional_dijkstra(G, origin, destination, weight=weight_func)
    except nx.NetworkXNoPath:
        return {"error": f"No route found from {origin} to {destination}."}

    legs = []
    total_travel = 0
    total_wait = 0

    for i in range(len(path) - 1):
        edge = G[path[i]][path[i+1]]
        legs.append({
            "from":        path[i],
            "to":          path[i+1],
            "route":       edge["route"],
            "travel_time": edge["travel_time"],
            "wait_time":   edge["wait_time"],
        })
        total_travel += edge["travel_time"]
        total_wait   += edge["wait_time"]

    transfers = 0
    if legs:
        current_route = legs[0]["route"]
        for leg in legs[1:]:
            if leg["route"] != current_route:
                transfers += 1
                current_route = leg["route"]

    return {
        "origin":       origin,
        "destination":  destination,
        "path":         path,
        "legs":         legs,
        "total_time":   round(cost),
        "travel_time":  total_travel,
        "wait_time":    round(total_wait),
        "transfers":    transfers,
    }

def find_best_route(origin, destination, G=None):
    # Reuse provided graph or build a new one (fallback)
    if G is None:
        G = build_graph()

    if origin not in G.nodes:
        return {"error": f"Stop '{origin}' not found."}
    if destination not in G.nodes:
        return {"error": f"Stop '{destination}' not found."}

    # 1. Calculate Optimal Route (with traffic avoidance penalty)
    def weight_func_optimal(u, v, d):
        return get_edge_weight(u, v, d.get("weight", 1), avoidance_factor=2.0) # Using 2.0 as example

    optimal_route = _calculate_route_details(G, origin, destination, weight_func_optimal)
    if "error" in optimal_route:
        return optimal_route # Return error if optimal path not found

    # 2. Calculate Naive Route (actual time, no extra avoidance penalty)
    def weight_func_naive(u, v, d):
        return get_edge_weight(u, v, d.get("weight", 1), avoidance_factor=1.0)

    naive_route = _calculate_route_details(G, origin, destination, weight_func_naive)
    # If naive route has an error, it means no path exists at all, so return optimal_route's error
    if "error" in naive_route:
        return naive_route

    return {
        "optimal_route": optimal_route,
        "naive_route": naive_route,
    }

if __name__ == "__main__":
    # Example usage for testing
    comparison_result = find_best_route("Kalanki", "Chabahil")

    if "error" in comparison_result:
        print(comparison_result["error"])
    else:
        optimal = comparison_result["optimal_route"]
        naive = comparison_result["naive_route"]

        print("\n--- Optimal Route (Traffic Avoidance) ---")
        print(f"Path: {' → '.join(optimal['path'])}")
        print(f"Total time: {optimal['total_time']} min (Travel: {optimal['travel_time']} min, Wait: {optimal['wait_time']} min)")
        print(f"Transfers: {optimal['transfers']}")
        print("\n--- Naive Route (Actual Time, No Avoidance) ---")
        print(f"Path: {' → '.join(naive['path'])}")
        print(f"Total time: {naive['total_time']} min (Travel: {naive['travel_time']} min, Wait: {naive['wait_time']} min)")
        print(f"Transfers: {naive['transfers']}")