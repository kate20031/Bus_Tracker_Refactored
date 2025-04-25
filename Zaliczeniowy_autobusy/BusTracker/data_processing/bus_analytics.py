"""
@package BusDataAnalysis
This module performs bus data analysis
by calculating the count of vehicles
over the speed limit and the count of violations in vicinity.
"""

import pandas as pd

from Zaliczeniowy_autobusy.BusTracker.config.constants import (
    BUS_OUT1_FILE,
    BUS_OUT2_FILE,
    STOPS_COORD_FILE,
    PUNCTUAL_BUSES_FILE1,
    PUNCTUAL_BUSES_FILE2,
)
from Zaliczeniowy_autobusy.BusTracker.config.constants import MAX_SPEED, MAX_DISTANCE
from Zaliczeniowy_autobusy.BusTracker.data_processing.speed_calculation_strategy import \
    HaversineSpeedCalculationStrategy
from Zaliczeniowy_autobusy.BusTracker.data_processing.speed_violation_checker import SpeedViolationChecker
from Zaliczeniowy_autobusy.BusTracker.data_processing.violation_clusterer import find_violations_places
from Zaliczeniowy_autobusy.BusTracker.utils.bus_data_utils import get_bus_data, get_data, get_violation_coordinates

# Load data at module level
bus_json1 = get_bus_data(BUS_OUT1_FILE)
bus_json2 = get_bus_data(BUS_OUT2_FILE)
stops_json = get_data(STOPS_COORD_FILE)
bus_count_data1 = len(bus_json1.items())
bus_count_data2 = len(bus_json2.items())


## @brief Prints the count of vehicles over the speed limit for two time periods.
#
#  Uses the Haversine distance strategy and predefined speed limit to calculate
#  how many vehicles exceeded the allowed speed during rush and non-rush hours.
def print_vehicles_over_speed_limit():
    strategy = HaversineSpeedCalculationStrategy()
    s = SpeedViolationChecker(MAX_SPEED, strategy)
    count1 = s.count_vehicles_over_speed_limit(bus_json1)
    count2 = s.count_vehicles_over_speed_limit(bus_json2)
    print(f"Vehicles over speed limit during non rush hours: {count1}")
    print(f"Vehicles over speed limit during rush hours: {count2}")


## @brief Prints the number of clustered speed violations based on proximity.
#
#  Counts and prints the number of violation clusters (places where many violations happen nearby)
#  separately for rush and non-rush hours, using a defined distance threshold.
def print_violations_in_vicinity():
    violations1 = get_violation_coordinates(bus_json1, MAX_SPEED)
    count1 = len(
        find_violations_places(
            violations1,
            MAX_DISTANCE,
            bus_count_data1))
    print(f"Violations places in vicinity during non rush hours: {count1}")

    violations2 = get_violation_coordinates(bus_json2, MAX_SPEED)
    count2 = len(
        find_violations_places(
            violations2,
            MAX_DISTANCE,
            bus_count_data2))
    print(f"Violations places in vicinity during rush hours: {count2}")


## @brief Prints the number of non-punctual buses based on preprocessed punctuality data.
#
#  This function reads precomputed punctuality data and outputs the number of buses
#  that did not meet the punctuality requirements for both rush and non-rush hours.
def print_punctuality_accuracy():
    df1 = pd.read_csv(PUNCTUAL_BUSES_FILE1)
    df2 = pd.read_csv(PUNCTUAL_BUSES_FILE2)

    non_puct_rush_count = df1.groupby(["Zespol", "Slupek", "Lines"]).size().shape[0]
    non_puct_nrush_count = df2.groupby(["Zespol", "Slupek", "Lines"]).size().shape[0]

    print(f"Number of non punctual buses during non rush hours: {non_puct_nrush_count}")
    print(f"Number of non punctual buses during rush hours: {non_puct_rush_count}")
