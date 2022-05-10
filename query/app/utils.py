import math


def get_metric_distance(lat_i: float, long_i: float, lat_j: float, long_j: float) -> float:
    """Get an approximation of the metric distance between two points in the surface of the earth
    using the Haversine formula

    Args:
        lat_i (float): Latitude of the first point
        long_i (float): Longitude of the first point
        lat_j (float): Latitude of the second point
        long_j (float): Longitude of the second point

    Returns:
        float: Distance in meters between the two points
    """
    r_km = 6378.137  # Radius of earth in KM
    delta_lat = lat_j * math.pi / 180 - lat_i * math.pi / 180
    delta_lon = long_j * math.pi / 180 - long_i * math.pi / 180
    a = math.sin(delta_lat / 2) * math.sin(delta_lat / 2) + math.cos(
        lat_i * math.pi / 180
    ) * math.cos(lat_j * math.pi / 180) * math.sin(delta_lon / 2) * math.sin(delta_lon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return r_km * c * 1000
