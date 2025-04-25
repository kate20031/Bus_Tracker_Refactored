## @file
#  @brief This module contains functions for loading and processing vehicle accuracy data
#         related to bus stop locations and punctuality.
#
#  The functions in this module find bus stops for specific coordinates, calculate distance between them,
#  and determine whether a bus is at the correct stop at the expected time.

import pandas as pd

from Zaliczeniowy_autobusy.BusTracker.utils.geo_utils import haversine_distance


## @brief Finds a bus stop based on geographical coordinates.
#
#  This function checks each stop in the provided stop data and calculates the distance
#  between the input coordinates and each stop's coordinates. If the distance is less than or equal to 1 meter,
#  it returns the matching bus stop's `zespol` (team) and `slupek` (pole).
#
#  @param lat Latitude of the vehicle's current location.
#  @param lon Longitude of the vehicle's current location.
#  @param stops_data List of bus stops data that includes geographical coordinates.
#  @return A tuple containing the `zespol` (team) and `slupek` (pole) if a matching stop is found; otherwise, `None, None`.
def find_stop(lat, lon, stops_data):
    """
    This function takes in latitude, longitude, and stop data.
    It then finds and returns the stop matching the input coordinates.
    """
    stop_lon, stop_lat, zespol, slupek = None, None, None, None
    for stop in stops_data:
        for item in stop["values"]:
            if item["key"] == "szer_geo":
                stop_lat = float(item.get("value"))
            elif item["key"] == "dlug_geo":
                stop_lon = float(item.get("value"))
            elif item["key"] == "zespol":
                zespol = item.get("value")
            elif item["key"] == "slupek":
                slupek = item.get("value")
        # Calculate the distance from the vehicle's location to the stop
        distance = haversine_distance(lat, lon, stop_lat, stop_lon)

        # If the distance is within 1 meter, return the stop's team and pole
        if distance <= 1:
            return zespol, slupek

    return None, None


## @brief Loads vehicle accuracy data by matching vehicles to bus stops.
#
#  This function iterates through the provided vehicle data and finds the closest bus stop for each vehicle's
#  geographical coordinates. It then adds the stop information (`zespol`, `slupek`) to the vehicle's data.
#
#  @param vehicle_json List of vehicle data, including the vehicle's geographical coordinates.
#  @param stops_data List of bus stops data, including the stops' coordinates.
#  @param new_json_data A list where the updated vehicle data with bus stop information will be appended.
def load_vehicle_accuracy(vehicle_json, stops_data, new_json_data):
    """
    This function loads vehicle accuracy data by finding
    stops for specific coordinates
    and updating new_json_data with these findings.
    """
    for i in range(1, len(vehicle_json)):
        lat = vehicle_json[i].get("Lat")
        lon = vehicle_json[i].get("Lon")

        # Find the closest stop for the current vehicle's coordinates
        zespol, slupek = find_stop(lat, lon, stops_data)

        # If a stop is found, add the stop information to the vehicle data
        if zespol is not None:
            vehicle_json[i]["Zespol"] = zespol
            vehicle_json[i]["Slupek"] = slupek
            new_json_data.append(vehicle_json[i])


## @brief Loads punctuality accuracy data and writes it to a CSV file.
#
#  This function processes bus data and calculates punctuality accuracy by finding the closest bus stop for each vehicle.
#  The resulting data is saved in a CSV file.
#
#  @param bus_data A dictionary of vehicle data, where each entry represents a specific vehicle's data.
#  @param stops_data List of bus stops data, including the stops' coordinates.
#  @param bus_data_output Path to the CSV file where the resulting accuracy data will be written.
#  @return The processed vehicle data with added accuracy information.
def load_punctuality_accuracy(bus_data, stops_data, bus_data_output):
    """
    This function loads punctuality accuracy data.
    It creates a new data frame with
    the vehicle accuracy data calculated for all vehicles in bus_data
    and writes it to a CSV file.
    """
    new_json_data = []

    # Process each vehicle's data and append accuracy information
    for _, vehicle in bus_data.items():
        load_vehicle_accuracy(vehicle, stops_data, new_json_data)

    df = pd.json_normalize(new_json_data)
    df.to_csv(bus_data_output, index=False)

    return new_json_data
