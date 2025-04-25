## @file
#  @brief This module contains functions for loading, processing, and saving bus data,
#         including data from CSV files and API responses.
#
#  It provides functionality to:
#    - Get violation coordinates based on bus data.
#    - Parse and format bus data from CSV files.
#    - Process API responses and save the results.
#    - Save results to a CSV file.

import csv
from datetime import datetime
from itertools import groupby

from Zaliczeniowy_autobusy.BusTracker.config.constants import CSV_ENCODING, CSV_DELIMITER, DATE_FORMAT, EARLY_HOURS, \
    LATE_HOURS, BUS_OUT1_FILE, BUS_OUT2_FILE
from Zaliczeniowy_autobusy.BusTracker.data_loaders.cvs_loader import CSVLoader, convert_to_dict
from Zaliczeniowy_autobusy.BusTracker.data_processing.speed_violation_factory import SpeedViolationCheckerFactory


## @brief Returns list of coordinates of violations that exceed the max speed.
#
#  This function checks the vehicle data and returns the coordinates where the vehicles
#  exceeded the specified max speed.
#
#  @param json_data The vehicle data in JSON format.
#  @param max_speed The maximum speed limit.
#  @return List of coordinates where the speed violations occurred.
def get_violation_coordinates(json_data, max_speed):
    """
    Returns list of the coordinates of violations that exceed max speed.
    """
    speed_checker = SpeedViolationCheckerFactory.create_speed_violation_checker(50.0, "haversine")
    coords = speed_checker.get_violation_coordinates(json_data)
    return coords


## @brief Parses and formats bus data from a CSV file.
#
#  This function reads the bus data from the specified CSV file, converts the time
#  to a datetime object, and filters the data based on the bus operation time.
#  It groups the data by VehicleNumber and returns the grouped data.
#
#  @param file_path The path to the CSV file containing bus data.
#  @return A dictionary where the keys are vehicle numbers and the values are lists
#          of records for that vehicle.
def get_bus_data(file_path):
    """
    Parse and format the data in the file.
    Returns the grouped json data.
    """
    json_data = []

    with open(file_path, newline="", encoding=CSV_ENCODING) as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=CSV_DELIMITER)

        next(csv_reader, None)
        for row in csv_reader:
            data_str = row[0]
            data_dict = convert_to_dict(data_str)
            time_str = data_dict["Time"]
            try:
                d = datetime.strptime(time_str, DATE_FORMAT)
            except ValueError:
                continue

            early_run = d.hour in EARLY_HOURS and d.day == 18
            rush_hours_run = d.hour in LATE_HOURS and d.day == 18

            if file_path == BUS_OUT1_FILE and early_run:
                json_data.append(data_dict)
            elif file_path == BUS_OUT2_FILE and rush_hours_run:
                json_data.append(data_dict)

    sorted_json_data = sorted(
        json_data, key=lambda x: (
            x["VehicleNumber"], x["Time"]))
    grouped_json_data = {
        key: list(group)
        for key, group in groupby(sorted_json_data, key=lambda x: x["VehicleNumber"])
    }

    return grouped_json_data


## @brief Reads a CSV file and converts it into a list of dictionaries.
#
#  This function loads the data from a CSV file using the CSVLoader class, which converts
#  each row of the file into a dictionary.
#
#  @param file_path The path to the CSV file.
#  @return A list of dictionaries where each dictionary represents a row from the CSV file.
def get_data(file_path):
    """
    Reads a CSV file and converts it into a list of dictionaries.
    """
    csv_loader = CSVLoader(encoding=CSV_ENCODING, delimiter=CSV_DELIMITER)
    json_data = csv_loader.load_as_dicts(file_path)

    return json_data


## @brief Processes the API response and appends the result to a CSV file.
#
#  This function takes the API response, parses the JSON data, and writes the records
#  to the specified output CSV file.
#
#  @param response The API response containing the records.
#  @param output_file_path The path to the output CSV file where the records will be saved.
def process_data(response, output_file_path):
    """
    Processes the response and writes the records to the CSV file.
    """
    data = response.json()
    records = data["result"]

    if records != "Błędna metoda lub parametry wywołania":
        with open(output_file_path, "a", newline="") as file:
            writer = csv.writer(file)
            for record in records:
                writer.writerow([record])


## @brief Saves the results DataFrame to a CSV file.
#
#  This function takes a Pandas DataFrame and saves it to the specified output CSV file.
#
#  @param results_df The Pandas DataFrame containing the results to be saved.
#  @param output_file The path to the output CSV file where the results will be stored.
def save_results(results_df, output_file):
    """
    This function saves the resulting DataFrame
    'results_df' into the 'output_file' CSV file.
    """
    results_df.to_csv(output_file, index=False)
