## @file
#  @brief This module contains the implementation of the Haversine formula to calculate the distance
#         between two geographical coordinates.
#
#  The Haversine formula is used to calculate the shortest distance between two points on the surface of a sphere
#  (in this case, the Earth). It is commonly used in geolocation services.

from cmath import asin, cos, sin, sqrt
from math import radians

from Zaliczeniowy_autobusy.BusTracker.config.constants import KM_TO_M_CONVERSION, EARTH_RADIUS


## @brief Calculates the Haversine distance between two geographical coordinates.
#
#  This function uses the Haversine formula to calculate the distance between two points
#  on the Earth specified by their latitude and longitude coordinates. The result is returned in meters.
#
#  @param lat1 The latitude of the first point, in degrees.
#  @param lon1 The longitude of the first point, in degrees.
#  @param lat2 The latitude of the second point, in degrees.
#  @param lon2 The longitude of the second point, in degrees.
#  @return The distance between the two points in meters.
def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculates the Haversine distance between two geographical coordinates.
    """
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Differences in coordinates
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Haversine formula
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))

    # Calculate the distance in meters
    distance = EARTH_RADIUS * c * KM_TO_M_CONVERSION

    # Return the distance as an integer
    return int(distance.real)
