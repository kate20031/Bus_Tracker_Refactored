## @file
#  @brief Module responsible for detecting speed violations from vehicle tracking data.
#
#  Implements logic to check if vehicles exceed a defined speed limit, and provides
#  functionality to retrieve coordinates of those violations.

from datetime import datetime

from Zaliczeniowy_autobusy.BusTracker.config.constants import DATE_FORMAT, SPEED_CONVERSION_TO_KN_H
from Zaliczeniowy_autobusy.BusTracker.data_processing.speed_calculation_strategy import SpeedCalculationStrategy
from Zaliczeniowy_autobusy.BusTracker.utils.geo_utils import haversine_distance


## @class SpeedViolationChecker
#  @brief Class to detect vehicles exceeding the speed limit.
#
#  Uses a given speed calculation strategy to determine whether vehicles are speeding.
class SpeedViolationChecker:
    ## @brief Constructor.
    #  @param max_speed The maximum allowed speed.
    #  @param strategy The strategy used to calculate speed.
    def __init__(self, max_speed, strategy: SpeedCalculationStrategy):
        self.max_speed = max_speed
        self.strategy = strategy

    ## @brief Calculates the maximum speed of a given vehicle.
    #  @param vehicle A list of location records (dicts) for one vehicle.
    #  @return The highest speed detected.
    def calculate_max_speed(self, vehicle):
        max_speed = 0
        for i in range(1, len(vehicle)):
            speed = self.strategy.calculate_speed(vehicle, i)
            if speed > max_speed:
                max_speed = speed
        return max_speed

    ## @brief Counts how many vehicles exceeded the speed limit.
    #  @param json_data Dictionary of vehicle tracking data.
    #  @return Integer count of speeding vehicles.
    def count_vehicles_over_speed_limit(self, json_data):
        max_speeds = [self.calculate_max_speed(vehicle) for vehicle in json_data.values()]
        count_grater_than_limit = sum(1 for speed in max_speeds if speed > self.max_speed)
        return count_grater_than_limit

    ## @brief Retrieves coordinates of speed violations.
    #  @param json_data Dictionary of vehicle tracking data.
    #  @return List of tuples (latitude, longitude, vehicle number) for each violation.
    def get_violation_coordinates(self, json_data):
        violations_coordinates = []
        for _, vehicle in json_data.items():
            for i in range(1, len(vehicle)):
                speed = self.calculate_speed(vehicle, i)
                if speed > self.max_speed:
                    lat = vehicle[i].get("Lat")
                    lon = vehicle[i].get("Lon")
                    vehicle_number = vehicle[i].get("VehicleNumber")
                    violations_coordinates.append((lat, lon, vehicle_number))
        return violations_coordinates

    ## @brief Calculates speed between two positions using Haversine distance.
    #  @param vehicle List of vehicle location entries (dicts).
    #  @param index Index of the second entry used for speed calculation.
    #  @return Speed in appropriate units; 0 if time difference is zero.
    def calculate_speed(self, vehicle, index):
        time_diff = (
                datetime.strptime(vehicle[index]["Time"], DATE_FORMAT)
                - datetime.strptime(vehicle[index - 1]["Time"], DATE_FORMAT)
        ).total_seconds()

        lat1, lon1 = vehicle[index - 1]["Lat"], vehicle[index - 1]["Lon"]
        lat2, lon2 = vehicle[index]["Lat"], vehicle[index]["Lon"]
        distance = haversine_distance(lat1, lon1, lat2, lon2)
        speed = distance / time_diff * SPEED_CONVERSION_TO_KN_H if time_diff > 0 else 0

        return speed
