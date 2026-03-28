import math
from .models import PoliceStation


def haversine_km(lat1, lon1, lat2, lon2):
    """Return the great-circle distance in kilometres between two points."""
    R = 6371  # Earth's radius in km
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def find_nearest_station(user_lat, user_lon):
    stations = PoliceStation.objects.all()

    nearest = None
    min_dist = float('inf')

    for station in stations:
        dist = haversine_km(user_lat, user_lon, station.latitude, station.longitude)
        if dist < min_dist:
            min_dist = dist
            nearest = station

    return nearest, round(min_dist, 2)
