## @file
#  @brief Unit tests for the bus speed violation checking functionality.
#
#  This module contains tests for functions related to detecting speed violations in bus data,
#  such as calculating speed, detecting violations based on GPS coordinates, and handling edge cases like invalid coordinates.

import os
import unittest

import pandas as pd

from Zaliczeniowy_autobusy.BusTracker.config.constants import MAX_SPEED
from Zaliczeniowy_autobusy.BusTracker.data_processing.speed_calculation_strategy import \
    HaversineSpeedCalculationStrategy
from Zaliczeniowy_autobusy.BusTracker.data_processing.speed_violation_checker import SpeedViolationChecker


## @brief Unit test case for speed violation checking functions.
#
#  This test case includes tests for detecting speed violations in bus data, including handling invalid coordinates
#  and multiple violations in the data. It uses a `SpeedViolationChecker` and `HaversineSpeedCalculationStrategy`
#  to process and check for violations based on GPS data.
class Test_Speed_Violation(unittest.TestCase):
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
        strategy = HaversineSpeedCalculationStrategy()
        self.speed_violation_checker = SpeedViolationChecker(max_speed=MAX_SPEED, strategy=strategy)

    ## @brief Clean up any resources or data created during the tests.
    #
    #  This method is called after each test method is executed. It removes any files or resources created during tests.
    def tearDown(self):
        """Clean up any resources or data created during the tests."""
        if os.path.exists(self.test_output_file):
            os.remove(self.test_output_file)

    ## @brief Test for invalid GPS coordinates.
    #
    #  This test validates that the system correctly handles invalid GPS coordinates (outside valid ranges).
    #  It ensures that no violations are detected when the coordinates are invalid.
    def test_get_violation_coordinates_invalid_gps(self):
        """Test for invalid GPS coordinates."""
        json_data = {
            "vehicle1": [
                {"Time": "2022-01-01 12:00:00", "Lat": 1000, "Lon": 2000},  # Invalid coordinates
                {"Time": "2022-01-01 12:01:00", "Lat": 1000, "Lon": 2000},  # Invalid coordinates
            ],
            "vehicle2": [
                {"Time": "2022-01-01 12:00:00", "Lat": 52.2296756, "Lon": 21.0122287},  # Valid coordinates
                {"Time": "2022-01-01 12:01:00", "Lat": 52.2296756, "Lon": 21.0122287},  # Valid coordinates
            ]
        }

        violations_coordinates = self.speed_violation_checker.get_violation_coordinates(json_data)
        # Assert that no violations are detected for invalid coordinates.
        self.assertEqual(violations_coordinates, [])

    ## @brief Test for multiple violations in the data.
    #
    #  This test checks for multiple speed violations in the bus data. It simulates a scenario where multiple data points
    #  exceed the speed limit, ensuring that the system correctly detects all the violations.
    def test_get_violation_coordinates_multiple_violations(self):
        """Test for multiple violations in the data."""
        json_data = {
            "vehicle1": [
                {"Time": "2022-01-01 12:00:00", "Lat": 0, "Lon": 0},
                {"Time": "2022-01-01 12:01:00", "Lat": 0.008994, "Lon": 0},
                {"Time": "2022-01-01 12:02:00", "Lat": 0.017988, "Lon": 0},
            ],
            "vehicle2": [
                {"Time": "2022-01-01 12:00:00", "Lat": 0, "Lon": 0},
                {"Time": "2022-01-01 12:01:00", "Lat": 0, "Lon": 0.001},
            ],
        }
        violations_coordinates = self.speed_violation_checker.get_violation_coordinates(json_data)
        expected_coordinates = [
            (0.008994, 0, None),
            (0.017988, 0, None),
        ]
        # Assert that the system correctly detects all the violations.
        self.assertEqual(violations_coordinates, expected_coordinates)


## @brief Main function to run the unit tests.
#
#  This function runs the unit tests defined in the `Test_Speed_Violation` class when the script is executed directly.
if __name__ == "__main__":
    unittest.main()
