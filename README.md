# Public-Transport-Optimizer
This is a Original hackathon Project at Infinity Codewave 2026 by Ashutosh Chaudhary and Ankit Basyal.

<img width="1254" height="1254" alt="ChatGPT Image Apr 26, 2026, 08_13_18 AM" src="https://github.com/user-attachments/assets/5099f063-0e72-4439-87ca-bc5535bcef2a" />

This a modern day solution to the chaotic and merciless time wasting transportation system. Kathmandu Valley has 2.5 million daily commuters. The average one-way commute takes 90 minutes- not because of the distance, but because there's no system. Buses overlap randomly. Operators cherry pick profitable routes and abandon others. No passengers ever knows the fastest combination of buses to take- it's costing people hours of their lives every single day. These aren't made up numbers. They come directly from the 2025 ESCAP (Economic and Social Commission for Asia and the Pacific).

So, we built a system in four steps. Step one- we model Kathmandu's entire bus network as a graph. Every bus stop is a node. Every route segment between stops is directed edge. Step two- each edge gets a weight: travel time plus expected wait time for the next bus. Step three- we run Dijkstra's algorithm to find the lowest-cost path across the entire network. Step four- the optimal route is drawn on an interactive Kathmandu map, following the actual roads. That's the full system.

Now, why does it matter. If our optimizer reduces transfer by just one per journey, each commuter saves 20 to 30 minutes per day. Across 500,000+ daily bus riders in Kathmandu, that is hundreds of thousands of hours returned to people every single day.
