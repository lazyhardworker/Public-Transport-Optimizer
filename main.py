import os
import sys
import webbrowser
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from routing.dijkstra import find_best_route
from routing.stop_resolver import resolve_stop  # <-- ADD THIS
from viz.map_view import create_map
from data.stops import STOPS


def show_all_stops():
    print("\nAvailable stops:")
    stops = list(STOPS.keys())
    for i, stop in enumerate(stops):
        print(f"  {i+1:2}. {stop}")
    return stops


def pick_stop(prompt, stops):
    """Fuzzy-aware stop picker — replaces the old exact-match version."""
    while True:
        print(f"\n{prompt}")
        choice = input("Type stop name, landmark, or number: ").strip()

        if not choice:
            continue

        # Pick by number
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(stops):
                return stops[idx]
            print(f"  Enter a number between 1 and {len(stops)}")
            continue

        # Run fuzzy resolver
        result = resolve_stop(choice)

        # Confident match — just return it
        if result["confidence"] in ("exact", "high"):
            matched = result["matched"]
            if result["method"] != "exact":
                print(f"  ✓ Interpreted as: '{matched}'")
            return matched

        # Possible match — ask user to confirm
        if result["confidence"] in ("medium", "low") and result["matched"]:
            matched = result["matched"]
            confirm = input(f"  Did you mean '{matched}'? (y/n): ").strip().lower()
            if confirm == "y":
                return matched
            # Show top alternatives
            print("  Closest matches:")
            for i, (name, score) in enumerate(result["candidates"][:3], 1):
                print(f"    {i}. {name}  ({score:.0%})")
            continue

        # No match at all
        print(f"  Could not find '{choice}'. Try a different spelling or pick by number.")


def print_result(result):
    print("\n" + "="*50)
    print("  OPTIMAL ROUTE FOUND")
    print("="*50)
    print(f"  From      : {result['origin']}")
    print(f"  To        : {result['destination']}")
    print(f"  Path      : {' → '.join(result['path'])}")
    print("-"*50)
    print(f"  Total time  : {result['total_time']} minutes")
    print(f"  Travel time : {result['travel_time']} minutes")
    print(f"  Wait time   : {result['wait_time']} minutes")
    print(f"  Transfers   : {result['transfers']}")
    print("-"*50)
    print("\n  Journey breakdown:")
    for i, leg in enumerate(result["legs"]):
        print(f"    {i+1}. {leg['from']} → {leg['to']}")
        print(f"       Bus  : {leg['route']}")
        print(f"       Ride : {leg['travel_time']} min | Wait: {leg['wait_time']:.0f} min")
    print("="*50)


def main():
    print("\n" + "="*50)
    print("  KATHMANDU PUBLIC TRANSPORT OPTIMIZER")
    print("="*50)
    print("  Find the fastest route between any two stops.")
    print("  You can type stop names, landmarks, or numbers.\n")

    while True:
        stops = show_all_stops()

        origin      = pick_stop("Select your ORIGIN stop:", stops)
        destination = pick_stop("Select your DESTINATION stop:", stops)

        if origin == destination:
            print("\n  Origin and destination are the same. Pick different stops.")
            continue

        print(f"\n  Finding best route from {origin} to {destination}...")
        result = find_best_route(origin, destination)

        if "error" in result: # Error from either optimal or naive path calculation
            print(f"\n  Error: {result['error']}")
            print("  Try a different combination.")
        else:
            optimal_route = result["optimal_route"]
            naive_route = result["naive_route"]

            print("\n" + "="*50)
            print("  ROUTE COMPARISON")
            print("="*50)
            print(f"  Origin      : {origin}")
            print(f"  Destination : {destination}")
            print("\n  --- Optimal Route (Traffic Avoidance) ---")
            print(f"  Path        : {' → '.join(optimal_route['path'])}")
            print(f"  Total time  : {optimal_route['total_time']} minutes")
            print(f"  Travel time : {optimal_route['travel_time']} minutes")
            print(f"  Wait time   : {optimal_route['wait_time']} minutes")
            print(f"  Transfers   : {optimal_route['transfers']}")
            print("\n  --- Naive Route (Actual Time, No Avoidance) ---")
            print(f"  Path        : {' → '.join(naive_route['path'])}")
            print(f"  Total time  : {naive_route['total_time']} minutes")
            print(f"  Travel time : {naive_route['travel_time']} minutes")
            print(f"  Wait time   : {naive_route['wait_time']} minutes")
            print(f"  Transfers   : {naive_route['transfers']}")
            print("="*50)

            # Print detailed breakdown for the optimal route
            print_result(optimal_route) 

            print("\n  Opening map in browser...")
            map_file = "map.html"
            create_map(optimal_route, naive_route, map_file) # Pass both routes
            
            # Cross-platform way to open the HTML file
            full_path = os.path.abspath(map_file)
            webbrowser.open(f"file://{full_path}")

        print("\n" + "-"*50)
        again = input("\n  Search another route? (y/n/q): ").strip().lower()
        if again != "y":
            print("\n  Thank you for using Kathmandu Transport Optimizer!")
            print("  Good luck at the hackathon!\n")
            break

if __name__ == "__main__":
    main()