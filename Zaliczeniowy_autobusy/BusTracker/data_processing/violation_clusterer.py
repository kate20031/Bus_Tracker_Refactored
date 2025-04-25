## @file
#  @brief Module for finding locations with multiple speed violations.
#
#  This module contains a function to group violations based on geographical proximity and the number of occurrences.

from Zaliczeniowy_autobusy.BusTracker.utils.geo_utils import haversine_distance
from Zaliczeniowy_autobusy.BusTracker.config.constants import BUS_COUNT_THRESHOLD


## @brief Finds clusters of violation locations based on a maximum distance threshold.
#
#  Groups violation coordinates into clusters if they are within the maximum distance from each other.
#  After clustering, it filters out groups with insufficient bus violations based on a predefined threshold.
#
#  @param coordinates List of violation coordinates (lat, lon, vehicle number).
#  @param max_dist The maximum distance (in meters) between two violation points for them to be considered in the same cluster.
#  @param bus_count The total number of buses used to compute a threshold for cluster size.
#  @return A list of clusters where each cluster contains violation points that are geographically close to each other.
def find_violations_places(coordinates, max_dist, bus_count):
    violations_places = []
    result = []

    for value in coordinates:
        found = False
        for cluster in violations_places:
            for point in cluster:
                if haversine_distance(point[0], point[1], value[0], value[1]) <= max_dist:
                    cluster.append(value)
                    found = True
                    break
        if not found:
            violations_places.append([value])

    for cluster in violations_places:
        if len(cluster) > bus_count * BUS_COUNT_THRESHOLD:
            result.append(cluster)

    return result
