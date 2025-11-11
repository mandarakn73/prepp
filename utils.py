# utils.py
import os
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from random import randint

BANGALORE_COORD = (12.9716, 77.5946)
geolocator = Nominatim(user_agent="prep_predict") if True else None  # set False to disable geopy

def safe_distance(location_name):
    """Return distance from Bangalore or 'N/A' if geopy fails or disabled."""
    if geolocator is None or not location_name or pd.isna(location_name):
        return "N/A"
    try:
        loc = geolocator.geocode(location_name, timeout=10)
        if loc:
            return round(geodesic(BANGALORE_COORD, (loc.latitude, loc.longitude)).km, 1)
        return "N/A"
    except Exception:
        return "N/A"

def offline_summary(college_row, student_rank):
    dist = safe_distance(college_row.get("Location", ""))
    # Basic rule-based summary
    summary = (
        f"{college_row.get('College','Unknown')} - {college_row.get('Branch','')}\n"
        f"Location: {college_row.get('Location','Unknown')} | Distance: {dist} km\n"
        f"Rank considered: {student_rank}\n\n"
        f"- Placement: Moderate to Good (refer campus reports)\n"
        f"- Hostel: Usually available; fees vary\n"
        f"- Pros: Established program, active placements\n"
        f"- Cons: Competitive intake, limited seats in top branches\n"
    )
    # Simple rule-based score (higher ChanceScore → higher score)
    score = randint(6,9)
    return summary, score
