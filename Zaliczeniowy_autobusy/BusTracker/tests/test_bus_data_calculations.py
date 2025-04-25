## @file
#  @brief Unit tests for the functions related to bus data calculations.
#
#  This module contains tests for the functions responsible for calculating bus data, such as speed calculation,
#  extracting violation coordinates, and saving results. These tests cover different aspects of data processing
#  and error handling for bus data calculations.

import os
import unittest
from unittest.mock import patch, MagicMock

import pandas as pd
from Zaliczeniowy_autobusy.BusTracker.data_loaders.cvs_loader import convert_to_dict
from Zaliczeniowy_autobusy.BusTracker.utils.bus_data_utils import process_data
from Zaliczeniowy_autobusy.BusTracker.utils.geo_utils import haversine_distance
from Zaliczeniowy_autobusy.BusTracker.utils.bus_data_utils import save_results


## @brief Unit test case for bus data calculation functions.
#
#  This test case includes various tests for functions used to calculate bus data such as speed, violation coordinates,
#  and result saving.
class TestBusDataCalculations(unittest.TestCase):
    """Test cases for functions in the bus_data_calculations module."""

    ## @brief Set up any necessary data or configuration for the tests.
    #
    #  This method is called before each test method is executed. It initializes necessary test data and configurations.
    def setUp(self):
        """Set up any necessary data or configuration for your tests."""
        self.test_output_file = "test_output.csv"
        self.test_results_df = pd.DataFrame(
            {"Column1": [1, 2, 3], "Column2": ["A", "B", "C"]}
        )

    ## @brief Clean up any resources or data created during the tests.
    #
    #  This method is called after each test method is executed. It removes any files or resources created during tests.
    def tearDown(self):
        """Clean up any resources or data created during the tests."""
        if os.path.exists(self.test_output_file):
            os.remove(self.test_output_file)

    ## @brief Test the haversine_distance function.
    #
    #  This test validates the correctness of the `haversine_distance` function by calculating the distance between two
    #  geographical points (Warsaw and Rome) and comparing it with the expected result.
    def test_haversine_distance(self):
        """Test the haversine_distance function."""
        lat1, lon1 = 52.2296756, 21.0122287  # Warsaw
        lat2, lon2 = 41.8919300, 12.5113300  # Rome
        distance = haversine_distance(lat1, lon1, lat2, lon2)

        # Assert that the calculated distance is as expected (in meters).
        self.assertEqual(distance, 1315510)

    ## @brief Test the process_data function with invalid data.
    #
    #  This test simulates the case where the `process_data` function receives invalid data and ensures that no file
    #  is written when the response indicates an error.
    def test_process_data_invalid(self):
        """Test the process_data function with invalid data."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"result": "Błędna metoda lub parametry wywołania"}
        output_file_path = "test_output.csv"

        with patch("builtins.open", unittest.mock.mock_open()) as mock_file:
            process_data(mock_response, output_file_path)

            # Verify that no file was written when the response is invalid.
            mock_file.assert_not_called()

    ## @brief Test the convert_to_dict function.
    #
    #  This test ensures that the `convert_to_dict` function correctly converts a string representation of a dictionary
    #  to an actual dictionary.
    def test_convert_to_dict(self):
        """Test the convert_to_dict function."""
        str_dict = "{'key1': 'value1', 'key2': 'value2'}"
        result = convert_to_dict(str_dict)

        # Assert that the conversion returns the expected dictionary.
        self.assertEqual(result, {"key1": "value1", "key2": "value2"})

    ## @brief Test for saving results to an invalid file path.
    #
    #  This test checks that the `save_results` function raises an error when trying to save results to a file with
    #  an invalid file path.
    def test_save_results_invalid_file(self):
        """Test for saving results to an invalid file path."""
        invalid_output_file = "/invalid/path/test_output.csv"
        with self.assertRaises(OSError):
            save_results(self.test_results_df, invalid_output_file)

    ## @brief Test for saving results to a valid file path.
    #
    #  This test verifies that the `save_results` function correctly saves the data frame to a valid file path and
    #  the file is created with the expected content.
    def test_save_results_valid_file(self):
        """Test for saving results to a valid file path."""
        save_results(self.test_results_df, self.test_output_file)

        # Check if the file was created and contains the expected data
        self.assertTrue(os.path.exists(self.test_output_file))
        saved_df = pd.read_csv(self.test_output_file)
        pd.testing.assert_frame_equal(saved_df, self.test_results_df)

    ## @brief Test for overwriting existing result file.
    #
    #  This test checks that when `save_results` is called with an existing file, the file is overwritten with the
    #  new data.
    def test_save_results_overwrite(self):
        """Test for overwriting existing result file."""
        save_results(self.test_results_df, self.test_output_file)

        saved_df = pd.read_csv(self.test_output_file)
        pd.testing.assert_frame_equal(self.test_results_df, saved_df)

        new_df = pd.DataFrame({"Column1": [4, 5, 6], "Column2": ["D", "E", "F"]})
        save_results(new_df, self.test_output_file)

        # Verify the file contains the new data (i.e., it was overwritten)
        saved_df = pd.read_csv(self.test_output_file)
        pd.testing.assert_frame_equal(new_df, saved_df)


## @brief Main function to run the unit tests.
#
#  This function runs the unit tests defined in the `TestBusDataCalculations` class when the script is executed directly.
if __name__ == "__main__":
    unittest.main()
