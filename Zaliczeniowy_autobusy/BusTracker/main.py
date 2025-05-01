## @file
#  @brief This module runs the bus analytics process, including loading data and performing the data analysis.
#
#  This module contains functions to load bus tracking data, bus station coordinates, and to perform the analytics
#  including vehicle speed violations, violations in vicinity, and punctuality accuracy.

from Zaliczeniowy_autobusy.BusTracker.data_processing.bus_analytics import (
    print_vehicles_over_speed_limit,
    print_violations_in_vicinity,
    print_punctuality_accuracy,
)

from Zaliczeniowy_autobusy.BusTracker.data_loaders.bus_data_loader import (
    load_bus_tracking_data,
    load_bus_stations_coord,
)


## @brief Loads bus tracking data and bus stations coordinates.
#
#  This function calls two separate functions to load bus tracking data and bus station coordinates.
#  It calls `load_bus_tracking_data()` to fetch real-time bus location data and `load_bus_stations_coord()`
#  to fetch coordinates of bus stations.
def load_data():
    """
    Calls functions to load bus tracking data and bus stations coordinates.
    """
    load_bus_tracking_data()
    load_bus_stations_coord()


## @brief Analyzes the loaded bus data.
#
#  This function calls various analytics functions to assess:
#  - Vehicles that exceed the speed limit (`print_vehicles_over_speed_limit()`).
#  - Violations occurring in the vicinity of other violations (`print_violations_in_vicinity()`).
#  - Punctuality of buses based on the loaded timetable and actual arrival times (`print_punctuality_accuracy()`).
def analyse_data():
    """
    Calls functions to print vehicles over
     speed limit and violations in vicinity.
    """
    print_vehicles_over_speed_limit()
    print_violations_in_vicinity()
    print_punctuality_accuracy()


## @brief Main function to run the bus analytics process.
#
#  This function is the entry point for the analytics process. It orchestrates the loading of data
#  and triggers the data analysis.
#
#  @note The call to `load_data()` is currently commented out. When active, it will load the required data before analysis.
def main():
    """
    Main function.
    """
    # Data initiation
    # load_data()

    # Data analysis
    analyse_data()


if __name__ == "__main__":
    main()
