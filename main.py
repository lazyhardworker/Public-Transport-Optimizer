import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from routing.dijkstra import find_best_route
from viz.map_view import create_map
from data.stops import STOPS

def show_all_stops():
    print("\nAvailable stops:")
    stops = list(STOPS.keys())
    for i, stop in enumerate(stops):
        print(f"  {i+1:2}. {stop}")
    return stops

def pick_stop(prompt, stops):
    while True:
        print(f"\n{prompt}")
        choice = input("Type the stop name exactly (or number): ").strip()

        # Allow picking by number
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(stops):
                return stops[idx]
            else:
                print(f"  Please enter a number between 1 and {len(stops)}")
                continue

        # Allow typing the name
        if choice in STOPS:
            return choice

        # Case-insensitive match
        for stop in stops:
            if stop.lower() == choice.lower():
                return stop

        print(f"  '{choice}' not found. Try again.")

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
        print(f"  {i+1}. {leg['from']} → {leg['to']}")
        print(f"     Bus    : {leg['route']}")
        print(f"     Ride   : {leg['travel_time']} min  |  Wait: {leg['wait_time']:.0f} min")
    print("="*50)

def main():
    print("\n" + "="*50)
    print("  KATHMANDU PUBLIC TRANSPORT OPTIMIZER")
    print("="*50)
    print("  Find the fastest route between any two stops")
    print("  in Kathmandu using smart path optimization.")

    while True:
        stops = show_all_stops()

        origin      = pick_stop("Select your ORIGIN stop:", stops)
        destination = pick_stop("Select your DESTINATION stop:", stops)

        if origin == destination:
            print("\n  Origin and destination are the same. Pick different stops.")
            continue

        print(f"\n  Finding best route from {origin} to {destination}...")
        result = find_best_route(origin, destination)

        if "error" in result:
            print(f"\n  No route found: {result['error']}")
            print("  Try a different combination.")
        else:
            print_result(result)

            print("\n  Opening map in browser...")
            create_map(origin, destination, "map.html")
            os.system("start map.html")

        print("\n" + "-"*50)
        again = input("\n  Search another route? (y/n): ").strip().lower()
        if again != "y":
            print("\n  Thank you for using Kathmandu Transport Optimizer!")
            print("  Good luck at the hackathon!\n")
            break

if __name__ == "__main__":
    main()