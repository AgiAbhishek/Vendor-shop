import math
from typing import Tuple

EARTH_RADIUS_KM = 6371.0


def bounding_box(lat: float, lng: float, radius_km: float) -> Tuple[float, float, float, float]:
    # Approximate degrees per km
    lat_delta = radius_km / 111.0
    cos_lat = math.cos(math.radians(lat))
    # Avoid division by near-zero at the poles
    if abs(cos_lat) < 1e-6:
        lon_delta = radius_km / 111.0
    else:
        lon_delta = radius_km / (111.320 * cos_lat)

    return (
        lat - lat_delta,
        lat + lat_delta,
        lng - lon_delta,
        lng + lon_delta,
    )


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return EARTH_RADIUS_KM * c