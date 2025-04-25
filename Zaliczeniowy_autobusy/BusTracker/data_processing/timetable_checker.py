## @file
#  @brief Module for checking and comparing bus timetable entries with real-time data.
#
#  This module contains the `TimetableChecker` class used for filtering timetable times
#  based on a given real time and calculating the time difference between them.

from datetime import datetime

from Zaliczeniowy_autobusy.BusTracker.config.constants import TIME_FORMAT


## @class TimetableChecker
#  @brief Class to filter and calculate time differences between timetable entries and real-time data.
#
#  Provides methods to filter timetable times that are within an acceptable range from the real-time entry
#  and to calculate the absolute time difference between timetable and real-time entries.
class TimetableChecker:
    ## @brief Filters timetable entries based on real time.
    #
    #  Filters timetable times that are within 1 hour difference from the real time.
    #  If the timetable time is close to real time (within 1 hour), it will be returned.
    #
    #  @param timetable_data List of timetable entries (dicts) containing scheduled times.
    #  @param real_time The real-time entry to compare against.
    #  @return List of filtered timetable times that are close to the real time.
    @staticmethod
    def filter_timetable_times(timetable_data, real_time):
        timetable_times = [
            datetime.strptime(
                "00" + entry["values"][5]["value"][2:]
                if entry["values"][5]["value"].startswith("24")
                else entry["values"][5]["value"],
                TIME_FORMAT,
            ).time()
            for entry in timetable_data
        ]
        return [
            time_entry
            for time_entry in timetable_times
            if abs(real_time.hour - time_entry.hour) <= 1
        ]

    ## @brief Calculates the absolute time difference between a timetable entry and real-time.
    #
    #  Computes the absolute difference in seconds between a given timetable time and real time.
    #
    #  @param timetable_time The scheduled time from the timetable.
    #  @param real_time The real-time entry to compare against.
    #  @return The absolute difference in seconds between the two times.
    @staticmethod
    def calculate_time_diff(timetable_time, real_time):
        time_entry = datetime.combine(datetime.min, timetable_time)
        real_time_time = real_time.to_pydatetime().time()
        time_entry = time_entry.time()

        return abs(
            (
                datetime.combine(datetime.min, time_entry)
                - datetime.combine(datetime.min, real_time_time)
            ).total_seconds()
        )
