## @file
#  @brief This module provides a utility function to connect to the API and fetch data.
#
#  This function sends an HTTP GET request to the API and retrieves the response in JSON format.
#  The data is parsed and returned as a list of records.

import requests


## @brief Connects to the bus timetable API and fetches data.
#
#  This function sends a GET request to the API endpoint and retrieves the data in JSON format.
#  It uses the provided `query_params` to customize the request. The returned data is extracted
#  from the response and returned as a list of records.
#
#  @param query_params A dictionary containing the query parameters to send in the GET request.
#                       These parameters are used to filter and customize the API response.
#  @return A list of records fetched from the API. Each record corresponds to an item in the "result"
#          section of the API response.
def conect_to_api(query_params):
    """
    Sends a GET request to the bus timetable API and returns the parsed records.

    @param query_params: Dictionary containing the parameters for the GET request.
    @return: A list of records from the API response.
    """
    r = requests.get(
        "https://api.um.warszawa.pl/api/action/dbtimetable_get/",
        params=query_params,
        timeout=5,
    )

    data = r.json()
    records = data["result"]

    return records
