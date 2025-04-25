"""
@package BusTimetableLoader
This module loads the bus timetable data.
"""

from Zaliczeniowy_autobusy.BusTracker.config.constants import API_KEY
from Zaliczeniowy_autobusy.BusTracker.utils.api_utils import conect_to_api


def load_bus_timetable_data(bus_stop_id, bus_stop_nr, line):
    """
    @brief Fetches bus timetable data for a given stop and line.

    This function connects to the Warsaw public transport API and retrieves
    the timetable for the specified bus stop and line. The data is returned
    in JSON format.

    @param bus_stop_id ID of the bus stop group ("zespol").
    @param bus_stop_nr Number of the specific stop ("slupek") within the group.
    @param line Bus line number (e.g., "105", "503").

    @return JSON object containing timetable data from the API.
    """
    id_1 = "e923fa0e-d96c-43f9-ae6e-60518c9f3238"

    query_params = {
        "id": id_1,
        "apikey": API_KEY,
        "busstopId": bus_stop_id,
        "busstopNr": str(bus_stop_nr),
        "line": line,
    }

    return conect_to_api(query_params)
