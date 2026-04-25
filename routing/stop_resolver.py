# routing/stop_resolver.py
import difflib
from data.stops import STOPS

# ---------------------------------------------------------------------------
# Landmark / alias map  — common names people actually say
# ---------------------------------------------------------------------------
ALIASES = {
    # Central landmarks
    "new road":           "Ratnapark",
    "newroad":            "Ratnapark",
    "rnac":               "Ratnapark",
    "nac":                "Ratnapark",
    "ratna park":         "Ratnapark",
    "ratna":              "Ratnapark",
    "bhatbhateni":        "Maharajgunj",
    "city centre":        "Ratnapark",
    "city center":        "Ratnapark",
    "durbar marg":        "Ratnapark",

    # North / Gongabu hub
    "naya buspark":       "Naya Buspark",
    "naya buspak":        "Naya Buspark",
    "naya bus park":      "Naya Buspark",
    "new buspark":        "Naya Buspark",
    "gongabu buspark":    "Naya Buspark",
    "gongabu bus park":   "Naya Buspark",
    "long route buspark": "Naya Buspark",

    # Thamel area (tourists say this constantly)
    "thamel":             "Ratnapark",
    "hotel thamel":       "Ratnapark",
    "thamel chowk":       "Ratnapark",

    # Pashupatinath / temple area
    "pashupatinath":      "Chabahil",
    "pashupati":          "Chabahil",
    "pashu":              "Chabahil",
    "gaushala":           "Chabahil",
    "gausala":            "Chabahil",

    # Patan
    "patan":              "Lagankhel",
    "patan gate":         "Patan Dhoka",
    "lagankel":           "Lagankhel",
    "lagan khel":         "Lagankhel",

    # Bhaktapur
    "bhaktapur":          "Bhaktapur Bus Park",
    "bhadgaon":           "Bhaktapur Bus Park",
    "bhaktapur bus":      "Bhaktapur Bus Park",
    "dudhpati":           "Bhaktapur Dudhpati",

    # West / Kalanki
    "kalanki chowk":      "Kalanki",
    "kalankee":           "Kalanki",
    "ring road west":     "Kalanki",

    # Airport
    "tribhuvan airport":  "Airport",
    "tia":                "Airport",
    "airport road":       "Airport",
    "tribhuvan":          "Airport",

    # Hospital / landmark clusters
    "bir hospital":       "Ratnapark",
    "teaching hospital":  "Maharajgunj",
    "norvic":             "Thapathali",
    "civil hospital":     "Baneshwor",
    "om hospital":        "Chabahil",

    # Colleges / universities
    "ku":                 "Ratnapark",     # Buses to KU Dhulikhel depart from Ratnapark
    "ioe":                "Pulchowk",
    "tu":                 "Kirtipur",
    "ioe pulchowk":       "Pulchowk",
    "st xaviers":         "Lainchaur",

    # Shopping malls
    "civil mall":         "Sundhara",
    "labim mall":         "Lagankhel",
    "sherpa mall":        "Dillibazar",

    # Misc common variants
    "koteshwar":          "Koteshwor",
    "koteshowr":          "Koteshwor",
    "koteswor":           "Koteshwor",
    "baneshwar":          "Baneshwor",
    "baneswor":           "Baneshwor",
    "tripureshowr":       "Tripureshwor",
    "tripureshwar":       "Tripureshwor",
    "chabahil":           "Chabahil",
    "chabhil":            "Chabahil",
    "maharajganj":        "Maharajgunj",
    "maharaj gunj":       "Maharajgunj",
    "budhanilkantha":     "Budhanilkantha",
    "budha nilkantha":    "Budhanilkantha",
    "jorpati":            "Jorpati",
    "sinamangal":         "Sinamangal",
    "jorpatti":           "Jorpati",
    "swayambhu":          "Swoyambhu",
    "boudha":             "Chabahil",
    "bouddha":            "Chabahil",
    "baudha":             "Chabahil",
    "boudhanath":         "Chabahil",
}

# ---------------------------------------------------------------------------
# Core resolver
# ---------------------------------------------------------------------------

def resolve_stop(user_input: str, cutoff: float = 0.5) -> dict:
    raw = user_input.strip()
    key  = raw.lower()
    stop_names = list(STOPS.keys())

    # 1. Exact match (case-insensitive)
    for stop in stop_names:
        if stop.lower() == key:
            return _result(stop, 1.0, "exact", stop_names)

    # 2. Alias / landmark map
    if key in ALIASES:
        matched = ALIASES[key]
        if matched in STOPS:
            return _result(matched, 0.95, "alias", stop_names)

    # 3. Partial alias match (user typed part of an alias phrase)
    for alias, canonical in ALIASES.items():
        if key in alias or alias in key:
            if canonical in STOPS:
                return _result(canonical, 0.85, "alias", stop_names)

    # 4. Fuzzy match against stop names
    #    Uses SequenceMatcher (built-in, no pip install needed)
    scored = []
    for stop in stop_names:
        stop_lower = stop.lower()
        # Evaluate full name and each word, taking the best score in one pass
        full_score = difflib.SequenceMatcher(None, key, stop_lower).ratio()
        word_scores = [difflib.SequenceMatcher(None, key, w).ratio() for w in stop_lower.split()]
        best_score = max([full_score] + word_scores)
        scored.append((stop, best_score))

    scored.sort(key=lambda x: x[1], reverse=True)
    best_stop, best_score = scored[0]

    if best_score >= cutoff:
        confidence = (
            "high"   if best_score >= 0.80 else
            "medium" if best_score >= 0.65 else
            "low"
        )
        return _result(best_stop, best_score, "fuzzy", stop_names, all_scored=scored)

    # 5. No match
    return {
        "matched": None,
        "confidence": "none",
        "score": 0.0,
        "candidates": scored[:3],
        "method": "none",
    }


def _result(stop, score, method, stop_names, all_scored=None):
    if all_scored is None:
        # Build scored list on demand for candidates
        all_scored = sorted(
            [(s, difflib.SequenceMatcher(None, stop.lower(), s.lower()).ratio())
             for s in stop_names],
            key=lambda x: x[1], reverse=True
        )
    # Return top 3 that aren't the primary match
    candidates = [(s, sc) for s, sc in all_scored if s != stop][:3]
    return {
        "matched": stop,
        "confidence": (
            "exact"  if method == "exact"  else
            "high"   if score  >= 0.85     else
            "medium" if score  >= 0.65     else
            "low"
        ),
        "score": round(score, 3),
        "candidates": candidates,
        "method": method,
    }


# ---------------------------------------------------------------------------
# User-friendly wrapper — what main.py and FastAPI actually call
# ---------------------------------------------------------------------------

def ask_stop(prompt_label: str, stop_names: list) -> str:

    while True:
        raw = input(f"\n{prompt_label}\n> ").strip()
        if not raw:
            continue

        # Allow picking by number
        if raw.isdigit():
            idx = int(raw) - 1
            if 0 <= idx < len(stop_names):
                return stop_names[idx]
            print(f"  Enter a number between 1 and {len(stop_names)}")
            continue

        result = resolve_stop(raw)

        if result["confidence"] in ("exact", "high"):
            matched = result["matched"]
            if result["method"] != "exact":
                print(f"  ✓ Matched: '{matched}'")
            return matched

        if result["confidence"] in ("medium", "low") and result["matched"]:
            matched = result["matched"]
            confirm = input(
                f"  Did you mean '{matched}'? (y/n): "
            ).strip().lower()
            if confirm == "y":
                return matched
            # Show candidates
            _print_candidates(result["candidates"])
            continue

        # No match — show closest options
        print(f"  Could not find '{raw}'. Closest stops:")
        _print_candidates(result["candidates"])


def _print_candidates(candidates):
    for i, (name, score) in enumerate(candidates, 1):
        bar = "█" * int(score * 10)
        print(f"    {i}. {name:30s} {bar} {score:.0%}")


# ---------------------------------------------------------------------------
# FastAPI-friendly function (returns JSON-serialisable dict)
# ---------------------------------------------------------------------------

def resolve_stop_api(user_input: str) -> dict:
    result = resolve_stop(user_input)
    if result["matched"]:
        stop_data = STOPS[result["matched"]]
        return {
            "ok": True,
            "stop": result["matched"],
            "lat": stop_data["lat"],
            "lon": stop_data["lon"],
            "zone": stop_data["zone"],
            "confidence": result["confidence"],
            "method": result["method"],
            "score": result["score"],
            "did_you_mean": [c[0] for c in result["candidates"]],
        }
    return {
        "ok": False,
        "stop": None,
        "message": f"Could not resolve '{user_input}' to any known stop.",
        "did_you_mean": [c[0] for c in result["candidates"]],
    }


# ---------------------------------------------------------------------------
# Quick test — run: python -m routing.stop_resolver
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    tests = [
        # Exact / near-exact
        "Ratnapark", "lagankhel", "KOTESHWOR",
        # Typos
        "Ratnaprk", "Lagankel", "Baneshwar", "Tripureshwar",
        # Landmarks
        "Thamel", "Pashupatinath", "new road", "airport", "teaching hospital",
        # Nepali variant spellings
        "Bauddha", "Swayambhunath", "naya buspak",
        # Partial
        "Dudhpati", "Bhaktapur", "kirtipur",
        # Garbage / total fail
        "xyzfoo", "???",
    ]

    print(f"\n{'INPUT':<25} {'MATCHED':<28} {'CONFIDENCE':<10} {'SCORE':<7} {'METHOD'}")
    print("─" * 85)
    for t in tests:
        r = resolve_stop(t)
        matched = r["matched"] or "— no match —"
        print(f"{t:<25} {matched:<28} {r['confidence']:<10} {r['score']:<7.2f} {r['method']}")