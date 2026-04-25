import networkx as nx
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from graph.builder import build_graph

def find_best_route(origin, destination):
    G = build_graph()

    if origin not in G.nodes:
        return {"error": f"Stop '{origin}' not found."}
    if destination not in G.nodes:
        return {"error": f"Stop '{destination}' not found."}

    try:
        path = nx.dijkstra_path(G, origin, destination, weight="weight")
        cost = nx.dijkstra_path_length(G, origin, destination, weight="weight")
    except nx.NetworkXNoPath:
        return {"error": f"No route found from {origin} to {destination}."}

    # Break down the journey leg by leg
    legs = []
    total_travel = 0
    total_wait   = 0

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

    return {
        "origin":       origin,
        "destination":  destination,
        "path":         path,
        "legs":         legs,
        "total_time":   round(cost),
        "travel_time":  total_travel,
        "wait_time":    round(total_wait),
        "transfers":    len(set(l["route"] for l in legs)) - 1,
    }

if __name__ == "__main__":
    result = find_best_route("Kalanki", "Chabahil")

    if "error" in result:
        print(result["error"])
    else:
        print(f"\nBest route: {' → '.join(result['path'])}")
        print(f"Total time: {result['total_time']} min")
        print(f"  Travel:   {result['travel_time']} min")
        print(f"  Waiting:  {result['wait_time']} min")
        print(f"Transfers:  {result['transfers']}")
        print("\nLegs:")
        for leg in result["legs"]:
            print(f"  {leg['from']} → {leg['to']}  ({leg['route']}, {leg['travel_time']} min ride + {leg['wait_time']:.0f} min wait)")