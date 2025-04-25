## @file
#  @brief Defines abstract and concrete strategies for calculating vehicle speed.
#
#  Contains the base class for speed calculation strategies and a concrete implementation
#  using the Haversine formula to compute distance-based speed.

from abc import ABC, abstractmethod
from datetime import datetime

from Zaliczeniowy_autobusy.BusTracker.config.constants import DATE_FORMAT, SPEED_CONVERSION
from Zaliczeniowy_autobusy.BusTracker.utils.geo_utils import haversine_distance


## @class SpeedCalculationStrategy
#  @brief Abstract base class for speed calculation strategies.
#
#  Any custom strategy must implement the `calculate_speed` method.
class SpeedCalculationStrategy(ABC):
    ## @brief Calculates speed for a vehicle at a specific index.
    #
    #  @param vehicle A list of location records (dicts) for a single vehicle.
    #  @param index Index of the current record in the list.
    #  @return Speed at the given index.
    @abstractmethod
    def calculate_speed(self, vehicle, index):
        pass


## @class HaversineSpeedCalculationStrategy
#  @brief Concrete implementation of SpeedCalculationStrategy using the Haversine formula.
#
#  Calculates distance between two geographic coordinates and converts the result
#  into speed using a time delta between two records.
class HaversineSpeedCalculationStrategy(SpeedCalculationStrategy):
    ## @brief Calculates speed using the Haversine formula.
    #
    #  Computes distance between two consecutive points and divides by the time difference,
    #  applying a conversion factor to obtain the speed in desired units (e.g., km/h).
    #
    #  @param vehicle List of dictionaries with keys "Lat", "Lon", and "Time".
    #  @param index Index of the current data point.
    #  @return Calculated speed (float); 0 if time difference is zero.
    def calculate_speed(self, vehicle, index):
        time_diff = (
                datetime.strptime(vehicle[index]["Time"], DATE_FORMAT)
                - datetime.strptime(vehicle[index - 1]["Time"], DATE_FORMAT)
        ).total_seconds()

        lat1, lon1 = vehicle[index - 1]["Lat"], vehicle[index - 1]["Lon"]
        lat2, lon2 = vehicle[index]["Lat"], vehicle[index]["Lon"]
        distance = haversine_distance(lat1, lon1, lat2, lon2)
        speed = distance / time_diff * SPEED_CONVERSION if time_diff > 0 else 0

        return speed
