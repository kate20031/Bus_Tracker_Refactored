## @file
#  @brief Unit tests for the `connect_to_api` function in the `api_utils` module.
#
#  This module contains unit tests for the function `connect_to_api`, which interacts with an external API to fetch data.
#  The tests include validating successful API requests and handling of exceptions in case of errors.

import unittest
from unittest.mock import patch, MagicMock
import requests
from Zaliczeniowy_autobusy.BusTracker.utils.api_utils import conect_to_api


## @brief Unit test case for the `connect_to_api` function.
#
#  This test case verifies the functionality of the `connect_to_api` function.
#  It mocks the `requests.get` call to simulate a successful response and checks that the function returns the correct records.
class TestConnectToAPI(unittest.TestCase):
    """Test cases for the connect_to_api function."""

    ## @brief Test the successful connection to the API.
    #
    #  This test mocks the `requests.get` call to simulate a successful API request and validates that the `connect_to_api`
    #  function returns the expected records.
    #
    #  @param mock_get Mocked version of `requests.get` method.
    @patch("requests.get")
    def test_connect_to_api(self, mock_get):
        """Test the connect_to_api function."""
        query_params = {"your": "query", "parameters": "here"}
        mock_records = [{"field1": "value1", "field2": "value2"}]
        mock_response = MagicMock()
        mock_response.json.return_value = {"result": mock_records}
        mock_get.return_value = mock_response

        # Calling the connect_to_api function
        records = conect_to_api(query_params)

        # Verify that requests.get was called with the correct arguments
        mock_get.assert_called_once_with(
            "https://api.um.warszawa.pl/api/action/dbtimetable_get/",
            params=query_params,
            timeout=5,
        )

        # Verify the function returns the correct records
        self.assertEqual(records, mock_records)

    ## @brief Test for handling an invalid URL and exceptions in the `connect_to_api` function.
    #
    #  This test simulates a situation where the `requests.get` call raises a `RequestException`. It checks that the
    #  `connect_to_api` function raises the correct exception.
    #
    #  @param mock_get Mocked version of `requests.get` method.
    @patch("requests.get")
    def test_connect_to_api_invalid_url(self, mock_get):
        """Test for an invalid API URL, simulating a request exception."""
        mock_get.side_effect = requests.exceptions.RequestException

        with self.assertRaises(requests.exceptions.RequestException):
            conect_to_api({"your": "query", "parameters": "here"})


## @brief Main function to run the unit tests.
#
#  This function runs the unit tests defined in the `TestConnectToAPI` class.
if __name__ == "__main__":
    unittest.main()
