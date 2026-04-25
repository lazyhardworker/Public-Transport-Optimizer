import random

# Simple mock of real-time traffic/delay data
LIVE_DELAYS = {
    "Kalanki": 10,
    "Koteshwor": 15,
    "Chabahil": 8,
    "Thapathali": 12,
    "Tripureshwor": 7
}

# Traffic on specific road segments between stops
LIVE_EDGE_DELAYS = {
    ("Kalanki", "Balkhu"): 20,
    ("Koteshwor", "Baneshwor"): 25,
}

# The higher this factor, the more aggressively the system avoids traffic.
# A factor of 2.0 means a 5-minute delay feels like a 10-minute penalty.
TRAFFIC_AVOIDANCE_FACTOR = 2.0

def get_edge_weight(stop_a, stop_b, base_weight, avoidance_factor=TRAFFIC_AVOIDANCE_FACTOR):
    """
    Calculates a "cost" weight for Dijkstra. 
    By multiplying delays, we discourage the algorithm from picking high-traffic paths.
    """
    # 1. Node-based delays (congestion at major intersections)
    delay_a = LIVE_DELAYS.get(stop_a, 0)
    delay_b = LIVE_DELAYS.get(stop_b, 0)
    node_delay = (delay_a + delay_b) / 2

    # 2. Edge-based delays (specific congested road segments)
    # We check both directions in case the graph is bi-directional
    edge_delay = LIVE_EDGE_DELAYS.get((stop_a, stop_b), 0) or \
                 LIVE_EDGE_DELAYS.get((stop_b, stop_a), 0)
    
    # 3. Calculate perceived cost
    # Total weight = base_time + (perceived_traffic_penalty * avoidance_factor)
    penalty = (node_delay + edge_delay) * avoidance_factor
    
    return base_weight + penalty