"""
@package BusTrackerLoader
This is a module for loading bus tracking
data and bus stations' coordinates.
"""

import time
from datetime import datetime

import pandas as pd
import requests

from Zaliczeniowy_autobusy.BusTracker.config.constants import (
    BUS_TRACKER_API_RESOURCE_ID,
    API_KEY,
    BUS_TRACKER_API_URL,
    BUS_OUT1_FILE,
    EARLY_HOURS,
    LATE_HOURS,
    BUS_OUT2_FILE,
    BUS_STATION_API_PARAMS,
    DATE_FORMAT,
)

from Zaliczeniowy_autobusy.BusTracker.utils.api_utils import conect_to_api
from Zaliczeniowy_autobusy.BusTracker.utils.bus_data_utils import process_data


def load_bus_tracking_data():
    """
    @brief Periodically loads real-time bus tracking data from the API.

    This function runs up to one hour and queries the API every 60 seconds
    to fetch real-time bus location data. Based on the time of day, it stores
    the results in either `BUS_OUT1_FILE` or `BUS_OUT2_FILE`.

    @note Uses constants EARLY_HOURS and LATE_HOURS to determine output destination.
    """
    current_time = datetime.now()
    start_time = time.time()

    while True:
        if time.time() - start_time > 3600:
            break

        query_params = {
            "resource_id": BUS_TRACKER_API_RESOURCE_ID,
            "type": 1,
            "apikey": API_KEY,
        }

        r = requests.get(BUS_TRACKER_API_URL, params=query_params, timeout=5)

        if current_time.hour in EARLY_HOURS:
            output_file_path = BUS_OUT1_FILE
        elif current_time.hour in LATE_HOURS:
            output_file_path = BUS_OUT2_FILE
        else:
            return
        process_data(r, output_file_path)

        time.sleep(60)


def load_bus_stations_coord():
    """
    @brief Loads bus station coordinates from the Warsaw public transport API.

    The result is processed and saved into a CSV file called `bus_station_output.csv`.

    @note Uses predefined parameters from BUS_STATION_API_PARAMS.
    """
    output_file_path = "bus_station_output.csv"
    r = requests.get(
        "https://api.um.warszawa.pl/api/action/dbstore_get/",
        params=BUS_STATION_API_PARAMS,
        timeout=5,
    )

    process_data(r, output_file_path)


def load_bus_timetable_data(busstop_id, busstop_nr, line):
    """
    @brief Retrieves a specific timetable entry from the API for a given stop and line.

    @param busstop_id Identifier of the bus stop group ("zespol").
    @param busstop_nr Identifier of the specific stop within the group ("slupek").
    @param line Bus line number (e.g., "503").

    @return JSON response with the timetable data.
    """
    api_key = "44c76d0d-4ca7-456a-a694-3b4dd63dd2d5"

    query_params = {
        "id": "e923fa0e-d96c-43f9-ae6e-60518c9f3238",
        "apikey": api_key,
        "busstopId": busstop_id,
        "busstopNr": busstop_nr,
        "line": line,
    }

    return conect_to_api(query_params)


def load_data(file_path):
    """
    @brief Loads bus data from a CSV file and returns a DataFrame.

    @param file_path Path to the CSV file containing processed bus data.
    @return pandas.DataFrame Parsed data with date parsing applied to the 'Time' column.
    """
    return pd.read_csv(
        file_path,
        parse_dates=["Time"],
        date_parser=lambda x: datetime.strptime(x, DATE_FORMAT),
    )


def load_timetable_data(zespol, slupek, lines):
    """
    @brief Wrapper function to load timetable data using logical stop identifiers.

    @param zespol Stop group identifier.
    @param slupek Specific stop number within the group.
    @param lines Bus line number(s) to query.

    @return JSON response containing timetable information.
    """
    return load_bus_timetable_data(zespol, slupek, lines)
