import networkx as nx
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.stops import STOPS, ROUTES

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

    return G

if __name__ == "__main__":
    G = build_graph()
    print(f"Nodes (stops): {G.number_of_nodes()}")
    print(f"Edges (segments): {G.number_of_edges()}")
    print("\nSample edges:")
    for u, v, data in list(G.edges(data=True))[:5]:
        print(f"  {u} → {v} | cost: {data['weight']:.1f} min | route: {data['route']}")