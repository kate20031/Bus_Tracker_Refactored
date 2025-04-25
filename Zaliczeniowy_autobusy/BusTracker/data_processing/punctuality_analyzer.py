## @file
#  @brief Module for analyzing punctuality of buses by comparing real-time data with the official timetable.
#
#  This module defines a class `PunctualityAnalyzer` to evaluate how closely real bus arrivals
#  match their scheduled times. It also provides a utility function to save the analysis results.

import pandas as pd

from Zaliczeniowy_autobusy.BusTracker.config.constants import MIN_TIME_DIFF, MAX_TIME_DIFF
from Zaliczeniowy_autobusy.BusTracker.data_loaders.bus_data_loader import load_timetable_data
from Zaliczeniowy_autobusy.BusTracker.utils.bus_data_utils import save_results
from Zaliczeniowy_autobusy.BusTracker.data_processing.timetable_checker import TimetableChecker
from Zaliczeniowy_autobusy.BusTracker.main import load_data


## @class PunctualityAnalyzer
#  @brief Compares real-time bus data with timetable entries to assess punctuality.
#
#  For each unique stop and line combination, the analyzer loads the timetable data
#  and compares each real-time arrival to determine if it falls within an acceptable time range.
class PunctualityAnalyzer:
    ## @brief Constructor for PunctualityAnalyzer.
    #  @param timetable_checker_cls Class used to check timetable-related logic (default: TimetableChecker).
    def __init__(self, timetable_checker_cls=TimetableChecker):
        self.timetable_checker_cls = timetable_checker_cls

    ## @brief Performs the punctuality analysis.
    #
    #  For each record in the input DataFrame, compares real-time arrival
    #  against the timetable and determines if it is punctual.
    #
    #  @param df pandas.DataFrame containing columns "Zespol", "Slupek", "Lines", and "Time".
    #  @return pandas.DataFrame with records considered punctual.
    def analyze(self, df):
        result_rows = []
        prev_slupek, prev_lines = None, None
        timetable_data = []

        for _, row in df.iterrows():
            zespol, slupek, lines, real_time = row["Zespol"], row["Slupek"], row["Lines"], row["Time"]

            if slupek != prev_slupek or lines != prev_lines:
                timetable_data = load_timetable_data(zespol, slupek, lines)

            if timetable_data:
                checker = self.timetable_checker_cls(timetable_data)
                for timetable_time in checker.filter_timetable_times(timetable_data, real_time):
                    time_diff = checker.calculate_time_diff(timetable_time, real_time)
                    if MIN_TIME_DIFF < time_diff < MAX_TIME_DIFF:
                        result_rows.append({
                            "Zespol": zespol,
                            "Slupek": slupek,
                            "Lines": lines,
                            "RealTime": real_time,
                            "TimeTable": timetable_time,
                        })

            prev_slupek, prev_lines = slupek, lines

        return pd.DataFrame(result_rows)


## @brief Entry-point function for checking punctuality accuracy and saving results.
#
#  Loads the accuracy CSV file with real-time bus data,
#  runs the punctuality analysis, and saves the filtered results to a file.
#
#  @param accuracy_csv Path to the CSV file with real-time bus tracking data.
#  @param punctual_buses_csv Output path for the CSV containing punctual bus records.
def check_punctuality_accuracy(accuracy_csv, punctual_buses_csv):
    df = load_data(accuracy_csv)
    df.sort_values(by=["Zespol", "Lines", "Slupek"], inplace=True)

    analyzer = PunctualityAnalyzer()
    results_df = analyzer.analyze(df)

    save_results(results_df, punctual_buses_csv)
