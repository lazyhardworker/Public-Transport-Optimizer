# Real Kathmandu neighborhoods as bus stops
# Coordinates are actual GPS positions
STOPS = {
     # --- Original stops (your dataset) ---
    "Ratnapark":            {"lat": 27.7041, "lon": 85.3145, "zone": "central"},
    "Kalanki":              {"lat": 27.6933, "lon": 85.2818, "zone": "west"},
    "Koteshwor":            {"lat": 27.6833, "lon": 85.3500, "zone": "east"},
    "Gongabu":              {"lat": 27.7333, "lon": 85.3167, "zone": "north"},
    "Lagankhel":            {"lat": 27.6667, "lon": 85.3167, "zone": "south"},
    "Chabahil":             {"lat": 27.7167, "lon": 85.3500, "zone": "northeast"},
    "Balaju":               {"lat": 27.7333, "lon": 85.2967, "zone": "northwest"},
    "Tripureshwor":         {"lat": 27.6980, "lon": 85.3100, "zone": "central"},
    "Baneshwor":            {"lat": 27.6933, "lon": 85.3400, "zone": "east"},
    "Maharajgunj":          {"lat": 27.7333, "lon": 85.3333, "zone": "north"},
    "Patan Dhoka":          {"lat": 27.6667, "lon": 85.3167, "zone": "south"},
    "Bhaktapur Bus Park":   {"lat": 27.6711, "lon": 85.4298, "zone": "far_east"},

    # --- New stops added from ESCAP 2025 study ---
    "Kirtipur":             {"lat": 27.6778, "lon": 85.2792, "zone": "southwest"},
    "Balkhu":               {"lat": 27.6867, "lon": 85.2950, "zone": "southwest"},
    "Kalimati":             {"lat": 27.6967, "lon": 85.2983, "zone": "west"},
    "Naya Buspark":         {"lat": 27.7400, "lon": 85.3200, "zone": "north"},   # Gongabu area
    "Thapathali":           {"lat": 27.6950, "lon": 85.3233, "zone": "central"},
    "Ekantakuna":           {"lat": 27.6600, "lon": 85.3033, "zone": "south"},
    "Jawalakhel":           {"lat": 27.6717, "lon": 85.3100, "zone": "south"},
    "Satdobato":            {"lat": 27.6533, "lon": 85.3217, "zone": "far_south"},
    "Mahalaxmisthan":       {"lat": 27.6633, "lon": 85.3100, "zone": "south"},
    "Hattiban":             {"lat": 27.6617, "lon": 85.3167, "zone": "south"},
    "Teku":                 {"lat": 27.6967, "lon": 85.3033, "zone": "central"},
    "Swoyambhu":            {"lat": 27.7150, "lon": 85.2900, "zone": "northwest"},
    "Dallu":                {"lat": 27.7167, "lon": 85.3000, "zone": "northwest"},
    "Nayabazar":            {"lat": 27.7133, "lon": 85.3033, "zone": "northwest"},
    "Ichangu":              {"lat": 27.7233, "lon": 85.2617, "zone": "far_northwest"},
    "Karakhanachok":        {"lat": 27.7183, "lon": 85.2717, "zone": "northwest"},
    "Dillibazar":           {"lat": 27.7083, "lon": 85.3317, "zone": "northeast"},
    "Bagbazar":             {"lat": 27.7067, "lon": 85.3233, "zone": "central"},
    "Putalisadak":          {"lat": 27.7000, "lon": 85.3267, "zone": "central"},
    "Hattisar":             {"lat": 27.7067, "lon": 85.3350, "zone": "northeast"},
    "Maitidevi":            {"lat": 27.7000, "lon": 85.3383, "zone": "east"},
    "Sinamangal":           {"lat": 27.6967, "lon": 85.3583, "zone": "east"},
    "Airport":              {"lat": 27.6967, "lon": 85.3600, "zone": "east"},
    "Pepsikola":            {"lat": 27.6900, "lon": 85.3667, "zone": "east"},
    "Mulpani":              {"lat": 27.6933, "lon": 85.3900, "zone": "far_east"},
    "Thimi":                {"lat": 27.6867, "lon": 85.3817, "zone": "far_east"},
    "Sallaghari":           {"lat": 27.6867, "lon": 85.4017, "zone": "far_east"},
    "Bhaktapur Dudhpati":   {"lat": 27.6717, "lon": 85.4233, "zone": "far_east"},
    "Bode":                 {"lat": 27.6933, "lon": 85.3817, "zone": "far_east"},
    "Jorpati":              {"lat": 27.7267, "lon": 85.3617, "zone": "northeast"},
    "Sundarijal":           {"lat": 27.7533, "lon": 85.3900, "zone": "far_northeast"},
    "Gokarna":              {"lat": 27.7367, "lon": 85.3717, "zone": "northeast"},
    "Kapan":                {"lat": 27.7267, "lon": 85.3433, "zone": "north"},
    "Budhanilkantha":       {"lat": 27.7717, "lon": 85.3617, "zone": "far_north"},
    "Tokha":                {"lat": 27.7533, "lon": 85.3367, "zone": "north"},
    "Samakhusi":            {"lat": 27.7367, "lon": 85.3100, "zone": "north"},
    "Basundhara":           {"lat": 27.7483, "lon": 85.3317, "zone": "north"},
    "Bansbari":             {"lat": 27.7400, "lon": 85.3317, "zone": "north"},
    "Lainchaur":            {"lat": 27.7167, "lon": 85.3167, "zone": "central"},
    "Kavresthali":          {"lat": 27.7617, "lon": 85.4133, "zone": "far_northeast"},
    "Thankot":              {"lat": 27.6950, "lon": 85.2417, "zone": "far_west"},
    "Dakshinkali":          {"lat": 27.6117, "lon": 85.2700, "zone": "far_southwest"},
    "Godawari":             {"lat": 27.6050, "lon": 85.3417, "zone": "far_south"},
    "Sunakothi":            {"lat": 27.6383, "lon": 85.3200, "zone": "far_south"},
    "Bungmati":             {"lat": 27.6383, "lon": 85.3067, "zone": "far_south"},
    "Khokana":              {"lat": 27.6467, "lon": 85.2967, "zone": "far_south"},
    "Chapagaun":            {"lat": 27.6183, "lon": 85.3250, "zone": "far_south"},
    "Lele":                 {"lat": 27.5867, "lon": 85.3317, "zone": "far_south"},
    "Farsidol":             {"lat": 27.6317, "lon": 85.2883, "zone": "far_south"},
    "Lamatar":              {"lat": 27.6450, "lon": 85.3683, "zone": "far_south"},
    "Narayanthan":          {"lat": 27.7133, "lon": 85.3083, "zone": "central"},
    "Ramkot":               {"lat": 27.7133, "lon": 85.2683, "zone": "northwest"},
    "Sitapaila":            {"lat": 27.7150, "lon": 85.2800, "zone": "northwest"},
    "Pandeychhap":          {"lat": 27.6683, "lon": 85.3167, "zone": "south"},
    "Taudaha":              {"lat": 27.6650, "lon": 85.3017, "zone": "south"},
    "Panga":                {"lat": 27.6717, "lon": 85.2783, "zone": "southwest"},
    "Goldhunge":            {"lat": 27.7483, "lon": 85.2717, "zone": "far_northwest"},
    "Ranipauwa":            {"lat": 27.7867, "lon": 85.2833, "zone": "far_northwest"},
    "Kakani":               {"lat": 27.8217, "lon": 85.3133, "zone": "far_north"},
    "Tinpiple":             {"lat": 27.7683, "lon": 85.3617, "zone": "far_north"},
    "Shankhamul":           {"lat": 27.6817, "lon": 85.3333, "zone": "east"},
    "Jamal":                {"lat": 27.7083, "lon": 85.3183, "zone": "central"},
    "Singhadurbar":         {"lat": 27.6983, "lon": 85.3183, "zone": "central"},
    "Kupandole":            {"lat": 27.6867, "lon": 85.3133, "zone": "south"},
    "Pulchowk":             {"lat": 27.6817, "lon": 85.3183, "zone": "south"},
    "Changunarayan":        {"lat": 27.7133, "lon": 85.4483, "zone": "far_east"},
    "Duwakot":              {"lat": 27.6917, "lon": 85.4067, "zone": "far_east"},
    "Gwarko":               {"lat": 27.6633, "lon": 85.3383, "zone": "southeast"},
    "Sankhamul":            {"lat": 27.6817, "lon": 85.3333, "zone": "east"},
    "Harisiddhi":           {"lat": 27.6483, "lon": 85.3500, "zone": "far_south"},
    "Thaiba":               {"lat": 27.6417, "lon": 85.3617, "zone": "far_south"},
    "Khumaltar":            {"lat": 27.6533, "lon": 85.3333, "zone": "far_south"},
    "Langol":               {"lat": 27.6717, "lon": 85.2867, "zone": "southwest"},
    "Chovar":               {"lat": 27.6633, "lon": 85.2883, "zone": "southwest"},
    "Matatirtha":           {"lat": 27.6883, "lon": 85.2650, "zone": "far_west"},
    "Machhegaun":           {"lat": 27.7017, "lon": 85.2767, "zone": "northwest"},
    "Satungal":             {"lat": 27.6950, "lon": 85.2683, "zone": "far_west"},
    "Jitpur Phedi":         {"lat": 27.7400, "lon": 85.2317, "zone": "far_west"},
    "Nagdhunga":            {"lat": 27.7200, "lon": 85.2367, "zone": "far_west"},
    "Bajrabarahi":          {"lat": 27.6467, "lon": 85.3267, "zone": "far_south"},
    "Hahar Mahadev":        {"lat": 27.6717, "lon": 85.3700, "zone": "east"},
    "Jadibuti":             {"lat": 27.6850, "lon": 85.3617, "zone": "east"},
    "Balkumari":            {"lat": 27.6700, "lon": 85.3500, "zone": "east"},
    "Tikathali":            {"lat": 27.6583, "lon": 85.3567, "zone": "far_east"},
    "Anamnagar":            {"lat": 27.7017, "lon": 85.3283, "zone": "central"},
    "Ghantaghar":           {"lat": 27.7033, "lon": 85.3150, "zone": "central"},
    "Bhrikutimandap":       {"lat": 27.7000, "lon": 85.3183, "zone": "central"},
    "Maitighar":            {"lat": 27.6967, "lon": 85.3250, "zone": "central"},
    "Babarmahal":           {"lat": 27.6983, "lon": 85.3267, "zone": "central"},
    "Lubhu":                {"lat": 27.6483, "lon": 85.3600, "zone": "far_south"},
    "Imadol":               {"lat": 27.6617, "lon": 85.3367, "zone": "southeast"},
    "Kamalbinayak":         {"lat": 27.6783, "lon": 85.4267, "zone": "far_east"},
    "Sankhu":               {"lat": 27.7417, "lon": 85.4333, "zone": "far_northeast"},
    "Nagarkot":             {"lat": 27.7133, "lon": 85.5167, "zone": "far_east"},
    "Sukedhara":            {"lat": 27.7417, "lon": 85.3350, "zone": "north"},
    "Bhangal":              {"lat": 27.7350, "lon": 85.3483, "zone": "north"},
    "Milanchowk":           {"lat": 27.6950, "lon": 85.3267, "zone": "central"},  # near Maitighar
    "Kalopul":              {"lat": 27.7050, "lon": 85.3367, "zone": "northeast"},
    "Balkot":               {"lat": 27.6900, "lon": 85.3567, "zone": "east"},
    "Biruwa Kaushaltar":    {"lat": 27.6750, "lon": 85.3650, "zone": "east"},
    "Sanagaun":             {"lat": 27.6567, "lon": 85.3417, "zone": "southeast"},
    "Shankhadevi":          {"lat": 27.6533, "lon": 85.3567, "zone": "far_south"},
}

# Routes: each is a list of stops in order, with travel time (minutes) per segment
ROUTES = {
    "Route 1 - Ring Road West": {
        "stops": ["Kalanki", "Balaju", "Gongabu", "Maharajgunj", "Chabahil"],
        "times": [8, 10, 7, 9],
        "frequency_min": 15,
        "route_length_km": 10.2,
        "vehicle_type": "minibus",
        "fare_npr": 27,
    },
    "Route 2 - Central Corridor": {
        "stops": ["Kalanki", "Tripureshwor", "Ratnapark", "Baneshwor", "Koteshwor"],
        "times": [12, 6, 8, 10],
        "frequency_min": 10,
        "route_length_km": 11.0,
        "vehicle_type": "minibus",
        "fare_npr": 27,
    },
    "Route 3 - North South": {
        "stops": ["Gongabu", "Ratnapark", "Tripureshwor", "Lagankhel", "Patan Dhoka"],
        "times": [10, 5, 8, 6],
        "frequency_min": 20,
        "route_length_km": 12.3,
        "vehicle_type": "bus",
        "fare_npr": 31,
    },
    "Route 4 - East Express": {
        "stops": ["Ratnapark", "Chabahil", "Bhaktapur Bus Park"],
        "times": [12, 25],
        "frequency_min": 30,
        "route_length_km": 16.5,
        "vehicle_type": "bus",
        "fare_npr": 35,
    },
    "Route 5 - Baneshwor Link": {
        "stops": ["Tripureshwor", "Baneshwor", "Chabahil", "Maharajgunj"],
        "times": [7, 10, 8],
        "frequency_min": 15,
        "route_length_km": 8.5,
        "vehicle_type": "minibus",
        "fare_npr": 27,
    },

    # -----------------------------------------------------------------------
    # NEW ROUTES — from ESCAP 2025 study (Tables 6 & 7, Annex-I)
    # Route lengths from Annex-I trip survey; times estimated at ~18 km/h avg.
    # -----------------------------------------------------------------------

    # Kirtipur area routes (heavily studied in the report)
    "Route 6 - Kirtipur to Ratnapark via Balkhu Kalimati": {
        "stops": ["Kirtipur", "Balkhu", "Kalimati", "Teku", "Tripureshwor", "Ratnapark"],
        "times": [8, 7, 5, 4, 5],
        "frequency_min": 20,
        "route_length_km": 8.0,   # from Annex-I: ~8.0 km
        "vehicle_type": "bus",
        "fare_npr": 27,
    },
    "Route 7 - Kirtipur to Lagankhel via Balkhu Mahalaxmisthan": {
        "stops": ["Kirtipur", "Balkhu", "Mahalaxmisthan", "Jawalakhel", "Lagankhel"],
        "times": [8, 7, 6, 5],
        "frequency_min": 25,
        "route_length_km": 7.6,   # from Annex-I
        "vehicle_type": "bus",
        "fare_npr": 27,
    },
    "Route 8 - Panga Kirtipur to Ratnapark": {
        "stops": ["Panga", "Kirtipur", "Balkhu", "Kalimati", "Tripureshwor", "Ratnapark"],
        "times": [5, 8, 7, 5, 5],
        "frequency_min": 25,
        "route_length_km": 6.35,  # from Annex-I
        "vehicle_type": "bus",
        "fare_npr": 27,
    },
    "Route 9 - Pandeychhap Taudaha Balkhu Kalimati Ratnapark": {
        "stops": ["Pandeychhap", "Taudaha", "Balkhu", "Kalimati", "Tripureshwor", "Ratnapark"],
        "times": [5, 7, 7, 5, 5],
        "frequency_min": 25,
        "route_length_km": 9.46,  # from Annex-I
        "vehicle_type": "minibus",
        "fare_npr": 27,
    },

    # Gongabu (Naya Buspark) routes
    "Route 10 - Gongabu Naya Buspark to Lagankhel": {
        "stops": ["Naya Buspark", "Gongabu", "Lainchaur", "Ratnapark", "Thapathali",
                  "Tripureshwor", "Jawalakhel", "Lagankhel"],
        "times": [3, 8, 5, 5, 4, 8, 5],
        "frequency_min": 15,
        "route_length_km": 12.25,  # from Annex-I
        "vehicle_type": "bus",
        "fare_npr": 31,
    },
    "Route 11 - Gongabu Naya Buspark to Bhaktapur Bansbari": {
        "stops": ["Naya Buspark", "Gongabu", "Chabahil", "Koteshwor", "Bhaktapur Bus Park"],
        "times": [3, 12, 15, 20],
        "frequency_min": 30,
        "route_length_km": 22.5,
        "vehicle_type": "bus",
        "fare_npr": 41,
    },
    "Route 12 - Gongabu Buspark to Ratnapark": {
        "stops": ["Naya Buspark", "Gongabu", "Lainchaur", "Ratnapark"],
        "times": [3, 8, 8],
        "frequency_min": 15,
        "route_length_km": 7.26,  # from Annex-I
        "vehicle_type": "minibus",
        "fare_npr": 27,
    },

    # Budhanilkantha & North routes
    "Route 13 - Budhanilkantha to Koteshwor": {
        "stops": ["Budhanilkantha", "Tokha", "Samakhusi", "Gongabu", "Chabahil", "Koteshwor"],
        "times": [10, 8, 7, 10, 12],
        "frequency_min": 20,
        "route_length_km": 17.5,
        "vehicle_type": "bus",
        "fare_npr": 35,
    },
    "Route 14 - Lagankhel to Budhanilkantha": {
        "stops": ["Lagankhel", "Thapathali", "Ratnapark", "Lainchaur", "Kapan",
                  "Bansbari", "Tokha", "Budhanilkantha"],
        "times": [8, 5, 8, 10, 7, 8, 10],
        "frequency_min": 25,
        "route_length_km": 24.5,
        "vehicle_type": "bus",
        "fare_npr": 41,
    },

    # Kalanki corridor routes
    "Route 15 - Kalanki to Koteshwor Chyamasingh": {
        "stops": ["Kalanki", "Tripureshwor", "Ratnapark", "Baneshwor", "Koteshwor"],
        "times": [12, 5, 8, 10],
        "frequency_min": 20,
        "route_length_km": 11.2,
        "vehicle_type": "bus",
        "fare_npr": 31,
    },
    "Route 16 - Matatirtha Kalanki Tripureshwor Ratnapark": {
        "stops": ["Matatirtha", "Satungal", "Kalanki", "Kalimati", "Tripureshwor", "Ratnapark"],
        "times": [10, 8, 7, 5, 5],
        "frequency_min": 20,
        "route_length_km": 12.0,
        "vehicle_type": "minibus",
        "fare_npr": 31,
    },
    "Route 17 - Balkot Koteshwor Tripureshwor Kalanki": {
        "stops": ["Balkot", "Biruwa Kaushaltar", "Hahar Mahadev", "Jadibuti", "Koteshwor", "Baneshwor",
                  "Maitighar", "Tripureshwor", "Kalanki"],
        "times": [5, 5, 7, 8, 6, 5, 4, 15],
        "frequency_min": 20,
        "route_length_km": 15.0,
        "vehicle_type": "bus",
        "fare_npr": 35,
    },
    "Route 18 - Mulpani Baneshwor Kalanki Thankot": {
        "stops": ["Mulpani", "Thimi", "Koteshwor", "Baneshwor", "Maitighar",
                  "Tripureshwor", "Kalanki", "Thankot"],
        "times": [12, 10, 8, 5, 4, 12, 18],
        "frequency_min": 30,
        "route_length_km": 26.0,
        "vehicle_type": "bus",
        "fare_npr": 41,
    },

    # Bhaktapur area routes
    "Route 19 - Bhaktapur Dudhpati Koteshwor Naya Buspark": {
        "stops": ["Bhaktapur Dudhpati", "Sallaghari", "Thimi", "Koteshwor", "Chabahil",
                  "Gongabu", "Naya Buspark"],
        "times": [10, 8, 15, 12, 10, 3],
        "frequency_min": 25,
        "route_length_km": 20.5,
        "vehicle_type": "bus",
        "fare_npr": 41,
    },
    "Route 20 - Bhaktapur Lagankhel": {
        "stops": ["Bhaktapur Dudhpati", "Sallaghari", "Thimi", "Koteshwor", "Baneshwor",
                  "Maitighar", "Jawalakhel", "Lagankhel"],
        "times": [10, 8, 15, 8, 5, 8, 5],
        "frequency_min": 25,
        "route_length_km": 22.0,
        "vehicle_type": "bus",
        "fare_npr": 41,
    },
    "Route 21 - Thimi Baneshwor Ratnapark": {
        "stops": ["Thimi", "Koteshwor", "Baneshwor", "Maitighar", "Ratnapark"],
        "times": [15, 8, 5, 4],
        "frequency_min": 20,
        "route_length_km": 8.58,  # from Annex-I
        "vehicle_type": "minibus",
        "fare_npr": 27,
    },
    "Route 22 - Duwakot Sallaghari Thimi Koteshwor Bagbazar": {
        "stops": ["Duwakot", "Sallaghari", "Thimi", "Koteshwor", "Baneshwor", "Bagbazar"],
        "times": [7, 8, 15, 8, 6],
        "frequency_min": 30,
        "route_length_km": 17.0,
        "vehicle_type": "bus",
        "fare_npr": 35,
    },

    # Lagankhel feeder / south routes
    "Route 23 - Lagankhel to Dakshinkali": {
        "stops": ["Lagankhel", "Ekantakuna", "Bungmati", "Khokana", "Dakshinkali"],
        "times": [7, 10, 8, 15],
        "frequency_min": 30,
        "route_length_km": 16.5,
        "vehicle_type": "microbus",
        "fare_npr": 35,
    },
    "Route 24 - Lagankhel to Godawari": {
        "stops": ["Lagankhel", "Jawalakhel", "Ekantakuna", "Sunakothi", "Godawari"],
        "times": [6, 7, 10, 8],
        "frequency_min": 25,
        "route_length_km": 12.5,
        "vehicle_type": "microbus",
        "fare_npr": 31,
    },
    "Route 25 - Lagankhel to Bungamati": {
        "stops": ["Lagankhel", "Jawalakhel", "Ekantakuna", "Bungmati"],
        "times": [6, 7, 10],
        "frequency_min": 30,
        "route_length_km": 7.5,
        "vehicle_type": "microbus",
        "fare_npr": 27,
    },
    "Route 26 - Lagankhel Satdobato Chapagaun Lele": {
        "stops": ["Lagankhel", "Jawalakhel", "Ekantakuna", "Satdobato", "Chapagaun", "Lele"],
        "times": [6, 7, 8, 10, 12],
        "frequency_min": 30,
        "route_length_km": 18.0,
        "vehicle_type": "bus",
        "fare_npr": 35,
    },
    "Route 27 - Farsidol to Lagankhel": {
        "stops": ["Farsidol", "Bungmati", "Ekantakuna", "Jawalakhel", "Lagankhel"],
        "times": [12, 10, 7, 6],
        "frequency_min": 30,
        "route_length_km": 10.6,  # from Annex-I avg
        "vehicle_type": "bus",
        "fare_npr": 27,
    },
    "Route 28 - Bajrabarahi to Lagankhel": {
        "stops": ["Bajrabarahi", "Ekantakuna", "Jawalakhel", "Lagankhel"],
        "times": [12, 7, 6],
        "frequency_min": 30,
        "route_length_km": 8.79,  # from Annex-I
        "vehicle_type": "microbus",
        "fare_npr": 27,
    },
    "Route 29 - Hattiban Lagankhel Thapathali Ratnapark": {
        "stops": ["Hattiban", "Lagankhel", "Kupandole", "Pulchowk", "Thapathali", "Ratnapark"],
        "times": [5, 6, 5, 5, 6],
        "frequency_min": 20,
        "route_length_km": 9.0,
        "vehicle_type": "minibus",
        "fare_npr": 27,
    },
    "Route 30 - Jamal to Lamatar": {
        "stops": ["Jamal", "Ratnapark", "Thapathali", "Jawalakhel", "Lagankhel",
                  "Satdobato", "Lamatar"],
        "times": [3, 6, 6, 6, 7, 15],
        "frequency_min": 20,
        "route_length_km": 13.36,  # from Annex-I
        "vehicle_type": "minibus",
        "fare_npr": 32,
    },

    # Gokarna / Northeast routes
    "Route 31 - Gokarna Chabahil Dillibazar Ratnapark": {
        "stops": ["Gokarna", "Jorpati", "Chabahil", "Dillibazar", "Bagbazar", "Ratnapark"],
        "times": [12, 8, 8, 5, 5],
        "frequency_min": 20,
        "route_length_km": 13.0,
        "vehicle_type": "bus",
        "fare_npr": 32,
    },
    "Route 32 - Gokarna Chabahil Maharajgunj Balaju Kalanki": {
        "stops": ["Gokarna", "Jorpati", "Chabahil", "Maharajgunj", "Balaju", "Kalanki"],
        "times": [12, 8, 7, 10, 15],
        "frequency_min": 20,
        "route_length_km": 18.0,
        "vehicle_type": "bus",
        "fare_npr": 35,
    },
    "Route 33 - Sundarijal Jorpati Chabahil Bagbazar Ratnapark": {
        "stops": ["Sundarijal", "Jorpati", "Chabahil", "Gausala", "Bagbazar", "Ratnapark"],
        "times": [20, 8, 7, 5, 5],
        "frequency_min": 30,
        "route_length_km": 20.0,
        "vehicle_type": "bus",
        "fare_npr": 41,
    },

    # Swoyambhu / Northwest routes
    "Route 34 - Ichangu Swoyambhu Dallu Nayabazar Ratnapark": {
        "stops": ["Ichangu", "Karakhanachok", "Swoyambhu", "Dallu", "Nayabazar", "Ratnapark"],
        "times": [8, 8, 6, 5, 6],
        "frequency_min": 20,
        "route_length_km": 11.0,
        "vehicle_type": "microbus",
        "fare_npr": 27,
    },
    "Route 35 - Ramkot Sitapaila Swoyambhu Ratnapark": {
        "stops": ["Ramkot", "Sitapaila", "Swoyambhu", "Dallu", "Nayabazar", "Ratnapark"],
        "times": [6, 8, 6, 5, 6],
        "frequency_min": 20,
        "route_length_km": 10.68,  # from Annex-I
        "vehicle_type": "microbus",
        "fare_npr": 27,
    },
    "Route 36 - Nagdhunga Kalanki Ratnapark": {
        "stops": ["Nagdhunga", "Thankot", "Kalanki", "Kalimati", "Tripureshwor", "Ratnapark"],
        "times": [15, 15, 7, 5, 5],
        "frequency_min": 20,
        "route_length_km": 18.0,
        "vehicle_type": "bus",
        "fare_npr": 35,
    },

    # Tokha & North routes
    "Route 37 - Tokha Sangla Bhatkeko Pul Ratnapark": {
        "stops": ["Tokha", "Samakhusi", "Gongabu", "Balaju", "Ratnapark"],
        "times": [8, 7, 10, 12],
        "frequency_min": 20,
        "route_length_km": 11.0,
        "vehicle_type": "minibus",
        "fare_npr": 27,
    },

    # NAC (Ratnapark) hub routes
    "Route 38 - Ratnapark to Narayanthan": {
        "stops": ["Ratnapark", "Lainchaur", "Narayanthan"],
        "times": [5, 5],
        "frequency_min": 15,
        "route_length_km": 9.82,  # from Annex-I
        "vehicle_type": "bus",
        "fare_npr": 27,
    },
    "Route 39 - NAC Baneshwor Airport Chabahil Gongabu Naya Buspark": {
        "stops": ["Ratnapark", "Bagbazar", "Putalisadak", "Hattisar", "Maitidevi",
                  "Baneshwor", "Airport", "Chabahil", "Maharajgunj", "Gongabu", "Naya Buspark"],
        "times": [4, 4, 5, 4, 5, 5, 8, 7, 5, 3],
        "frequency_min": 15,
        "route_length_km": 14.5,
        "vehicle_type": "bus",
        "fare_npr": 32,
    },
    "Route 40 - Ratnapark to Mulpani": {
        "stops": ["Ratnapark", "Bagbazar", "Baneshwor", "Sinamangal", "Airport", "Pepsikola", "Mulpani"],
        "times": [5, 8, 6, 5, 7, 8],
        "frequency_min": 20,
        "route_length_km": 16.5,
        "vehicle_type": "bus",
        "fare_npr": 35,
    },
    "Route 41 - NAC to Gagalphedi": {
        "stops": ["Ratnapark", "Lainchaur", "Maharajgunj", "Kapan", "Sukedhara", "Jorpati"],
        "times": [5, 7, 8, 7, 10],
        "frequency_min": 20,
        "route_length_km": 12.5,
        "vehicle_type": "minibus",
        "fare_npr": 31,
    },
    "Route 42 - Ratnapark to Sankhu": {
        "stops": ["Ratnapark", "Chabahil", "Jorpati", "Gokarna", "Kavresthali", "Sankhu"],
        "times": [10, 8, 10, 12, 15],
        "frequency_min": 30,
        "route_length_km": 24.0,
        "vehicle_type": "bus",
        "fare_npr": 41,
    },
    "Route 43 - Kavresthali to Ratnapark": {
        "stops": ["Kavresthali", "Gokarna", "Jorpati", "Chabahil", "Bagbazar", "Ratnapark"],
        "times": [12, 10, 8, 7, 5],
        "frequency_min": 25,
        "route_length_km": 12.77,  # from Annex-I
        "vehicle_type": "bus",
        "fare_npr": 32,
    },

    # Thankot / Corridor West
    "Route 44 - Thankot Tripureshwor Ratnapark Baneshwor Airport": {
        "stops": ["Thankot", "Kalanki", "Kalimati", "Tripureshwor", "Ratnapark",
                  "Bagbazar", "Baneshwor", "Airport"],
        "times": [18, 7, 5, 5, 4, 8, 5],
        "frequency_min": 20,
        "route_length_km": 18.5,
        "vehicle_type": "bus",
        "fare_npr": 35,
    },

    # Ring Road Circulation
    "Route 45 - Ring Road Circulation": {
        "stops": ["Kalanki", "Balkhu", "Jawalakhel", "Lagankhel", "Koteshwor",
                  "Baneshwor", "Chabahil", "Maharajgunj", "Balaju", "Kalanki"],
        "times": [7, 8, 5, 12, 8, 10, 7, 10, 8],
        "frequency_min": 20,
        "route_length_km": 26.79,  # from Annex-I
        "vehicle_type": "bus",
        "fare_npr": 41,
    },

    # Lagankhel cross-town
    "Route 46 - Lagankhel Koteshwor Bhaktapur Dudhpati": {
        "stops": ["Lagankhel", "Mahalaxmisthan", "Gwarko", "Koteshwor", "Thimi",
                  "Sallaghari", "Bhaktapur Dudhpati"],
        "times": [6, 8, 10, 10, 8, 10],
        "frequency_min": 25,
        "route_length_km": 18.5,
        "vehicle_type": "bus",
        "fare_npr": 35,
    },
    "Route 47 - Lagankhel Baneshwor Koteshwor Satdobato Lagankhel": {
        "stops": ["Lagankhel", "Maitighar", "Baneshwor", "Koteshwor", "Balkumari",
                  "Satdobato", "Lagankhel"],
        "times": [5, 8, 10, 8, 7, 8],
        "frequency_min": 20,
        "route_length_km": 13.14,  # from Annex-I
        "vehicle_type": "bus",
        "fare_npr": 32,
    },

    # Kalopul / East Cross
    "Route 48 - Sankhamul Baneshwor Anamnagar Putalisadak Ratnapark": {
        "stops": ["Shankhamul", "Gwarko", "Maitighar", "Baneshwor", "Anamnagar",
                  "Putalisadak", "Bhrikutimandap", "Ratnapark"],
        "times": [7, 5, 5, 4, 4, 3, 3],
        "frequency_min": 15,
        "route_length_km": 7.5,
        "vehicle_type": "minibus",
        "fare_npr": 27,
    },

    # Thapathali / Jamal cross-routes
    "Route 49 - Jamal Tripureshwor Satdobato Tikabhairav Lele": {
        "stops": ["Jamal", "Tripureshwor", "Thapathali", "Jawalakhel", "Ekantakuna",
                  "Satdobato", "Lele"],
        "times": [5, 5, 6, 7, 8, 12],
        "frequency_min": 25,
        "route_length_km": 15.5,
        "vehicle_type": "bus",
        "fare_npr": 35,
    },

    # Jitpur Phedi route (far west)
    "Route 50 - Jitpur Phedi to Ratnapark": {
        "stops": ["Jitpur Phedi", "Nagdhunga", "Kalanki", "Kalimati", "Tripureshwor", "Ratnapark"],
        "times": [20, 15, 7, 5, 5],
        "frequency_min": 30,
        "route_length_km": 22.0,
        "vehicle_type": "bus",
        "fare_npr": 41,
    },

    # Bungmati and Bhaisepati routes (south)
    "Route 51 - Bungmati Bhaisepati Ekantakuna Kupandole Ratnapark": {
        "stops": ["Bungmati", "Khokana", "Ekantakuna", "Jawalakhel", "Kupandole",
                  "Thapathali", "Ratnapark"],
        "times": [10, 8, 7, 6, 5, 6],
        "frequency_min": 25,
        "route_length_km": 12.5,
        "vehicle_type": "bus",
        "fare_npr": 31,
    },

    # Dahachowk West
    "Route 52 - Dahachowk Kalanki Ratnapark": {
        "stops": ["Matatirtha", "Satungal", "Kalanki", "Kalimati", "Teku", "Ratnapark"],
        "times": [8, 8, 7, 5, 5],
        "frequency_min": 20,
        "route_length_km": 11.0,
        "vehicle_type": "minibus",
        "fare_npr": 27,
    },

    # Kalopul - Tempo routes
    "Route 53 - Ratnapark to Kapan": {
        "stops": ["Ratnapark", "Dillibazar", "Kalopul", "Hattisar", "Maharajgunj", "Kapan"],
        "times": [5, 6, 5, 7, 8],
        "frequency_min": 15,
        "route_length_km": 8.5,
        "vehicle_type": "tempo",
        "fare_npr": 27,
    },
    "Route 54 - Ratnapark Tempopark to Sinamangal": {
        "stops": ["Ratnapark", "Bagbazar", "Anamnagar", "Sinamangal"],
        "times": [4, 4, 6],
        "frequency_min": 10,
        "route_length_km": 5.5,
        "vehicle_type": "tempo",
        "fare_npr": 20,
    },

    # Goldhunga far northwest
    "Route 55 - NAC Goldhunga": {
        "stops": ["Ratnapark", "Lainchaur", "Balaju", "Goldhunge"],
        "times": [5, 10, 15],
        "frequency_min": 25,
        "route_length_km": 10.5,
        "vehicle_type": "minibus",
        "fare_npr": 27,
    },

    # Changunarayan
    "Route 56 - Ratnapark Bagbazar to Changunarayan Temple": {
        "stops": ["Ratnapark", "Bagbazar", "Baneshwor", "Koteshwor", "Thimi", "Changunarayan"],
        "times": [4, 8, 10, 8, 15],
        "frequency_min": 30,
        "route_length_km": 22.5,
        "vehicle_type": "bus",
        "fare_npr": 41,
    },

    # Bode Mulpani East
    "Route 57 - Bode Mulpani Chabahil Samakhusi Gongabu": {
        "stops": ["Bode", "Mulpani", "Sinamangal", "Chabahil", "Maharajgunj",
                  "Samakhusi", "Gongabu"],
        "times": [8, 10, 8, 7, 7, 5],
        "frequency_min": 25,
        "route_length_km": 18.5,
        "vehicle_type": "bus",
        "fare_npr": 35,
    },

    # Naya Buspark (Gongabu) - NayaBuspark hub routes
    "Route 58 - Naya Buspark Gongabu Lainchaur Ghantaghar Putalisadak Sinamangal": {
        "stops": ["Naya Buspark", "Gongabu", "Balaju", "Lainchaur", "Ghantaghar",
                  "Putalisadak", "Hattisar", "Maitidevi", "Baneshwor", "Sinamangal"],
        "times": [3, 8, 5, 4, 4, 4, 4, 5, 7],
        "frequency_min": 15,
        "route_length_km": 16.5,
        "vehicle_type": "bus",
        "fare_npr": 35,
    },

    # Harisiddhi / Thaiba south routes
    "Route 59 - Lagankhel Satdobato Harisiddhi Thaiba Tikathali": {
        "stops": ["Lagankhel", "Mahalaxmisthan", "Ekantakuna", "Satdobato",
                  "Harisiddhi", "Thaiba", "Tikathali"],
        "times": [6, 6, 8, 8, 8, 8],
        "frequency_min": 25,
        "route_length_km": 14.5,
        "vehicle_type": "minibus",
        "fare_npr": 32,
    },

    # Sanagaun Koteshwor
    "Route 60 - Sanagaun Koteshwor Baneshwor Ratnapark": {
        "stops": ["Sanagaun", "Gwarko", "Koteshwor", "Baneshwor", "Maitighar", "Ratnapark"],
        "times": [8, 10, 8, 5, 5],
        "frequency_min": 20,
        "route_length_km": 13.0,
        "vehicle_type": "bus",
        "fare_npr": 32,
    },
    "Route 9 - Return": {
        "stops": ["Ratnapark", "Tripureshwor", "Kalimati", "Balkhu", "Taudaha", "Pandeychhap"],
        "times": [5, 5, 7, 7, 5],
        "frequency_min": 25,
        "route_length_km": 9.46,
        "vehicle_type": "minibus",
        "fare_npr": 27,
    },
    "Route 44 - Return": {
        "stops": ["Airport", "Baneshwor", "Bagbazar", "Ratnapark", "Tripureshwor", "Kalimati", "Kalanki", "Thankot"],
        "times": [5, 8, 4, 5, 5, 7, 18],
        "frequency_min": 20,
        "route_length_km": 18.5,
        "vehicle_type": "bus",
        "fare_npr": 35,
    },
    "Route 14 - Return": {
        "stops": ["Budhanilkantha", "Tokha", "Bansbari", "Kapan", "Lainchaur", "Ratnapark", "Thapathali", "Lagankhel"],
        "times": [10, 8, 7, 10, 8, 5, 8],
        "frequency_min": 25,
        "route_length_km": 24.5,
        "vehicle_type": "bus",
        "fare_npr": 41,
    },
    "Route 17 - Return": {
        "stops": ["Kalanki", "Tripureshwor", "Maitighar", "Baneshwor", "Koteshwor", "Jadibuti", "Hahar Mahadev", "Biruwa Kaushaltar", "Balkot"],
        "times": [15, 4, 5, 6, 8, 7, 5, 5],
        "frequency_min": 20,
        "route_length_km": 15.0,
        "vehicle_type": "bus",
        "fare_npr": 35,
    },
}