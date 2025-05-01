"""
This is a module for defining various constants used throughout the project.
"""

CSV_DELIMITER = ","
CSV_ENCODING = "utf-8"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
TIME_FORMAT = "%H:%M:%S"
EARTH_RADIUS_KM = 6371
SPEED_CONVERSION_TO_KN_H = 3.6
KM_TO_M_CONVERSION = 1000
MAX_SPEED_KM_H = 50
MIN_TIME_DIFF_S = 59
MAX_TIME_DIFF_S = 500
BUS_COUNT_THRESHOLD = 0.2
MAX_DISTANCE_M = 3000
BUS_OUT1_FILE = "Zaliczeniowy_autobusy/BusTracker/output/bus_coord_output1.csv"
BUS_OUT2_FILE = "Zaliczeniowy_autobusy/BusTracker/output/bus_coord_output2.csv"
# BUS_PUNCTUALITY_OUT1 = "output/bus_punctuality_accuracy1.json"
# BUS_PUNCTUALITY_OUT2 = "output/bus_punctuality_accuracy2.json"
STOPS_COORD_FILE = "Zaliczeniowy_autobusy/BusTracker/output/bus_station_coord_output.csv"
ACCURACY_FILE1 = "Zaliczeniowy_autobusy/BusTracker/output/bus_punctuality_accuracy1.csv"
ACCURACY_FILE2 = "Zaliczeniowy_autobusy/BusTracker/output/bus_punctuality_accuracy2.csv"
PUNCTUAL_BUSES_FILE1 = "Zaliczeniowy_autobusy/BusTracker/output/punctual_buses1.csv"
PUNCTUAL_BUSES_FILE2 = "Zaliczeniowy_autobusy/BusTracker/output/punctual_buses2.csv"
API_KEY = "44c76d0d-4ca7-456a-a694-3b4dd63dd2d5"
EARLY_HOURS = {11, 12}
LATE_HOURS = {17, 18}

BUS_TRACKER_API_URL = "https://api.um.warszawa.pl/api/action/busestrams_get/"
BUS_TRACKER_API_RESOURCE_ID = "f2e5503e-927d-4ad3-9500-4ab9e55deb59"

BUS_STATION_API_URL = "https://api.um.warszawa.pl/api/action/dbstore_get/"
BUS_STATION_API_RESOURCE_ID = "1c08a38c-ae09-46d2-8926-4f9d25cb0630"

BUS_TIMETABLE_API_RESOURCE_ID = "e923fa0e-d96c-43f9-ae6e-60518c9f3238"


BUS_TRACKER_API_PARAMS = {
    "resource_id": BUS_TRACKER_API_RESOURCE_ID,
    "apikey": API_KEY,
    "type": 1,
}

BUS_STATION_API_PARAMS = {
    "resource_id": BUS_STATION_API_RESOURCE_ID,
    "apikey": API_KEY,
}

BUS_TIMETABLE_API_PARAMS = {
    "id": BUS_TIMETABLE_API_RESOURCE_ID,
    "apikey": API_KEY,
}

