import csv


## @class CSVLoader
#  @brief Class for loading CSV data and converting it into Python dictionaries.
#
#  The CSVLoader class provides functionality to read CSV files where each row is
#  expected to contain a single string representing a dictionary.
class CSVLoader:
    ## @brief Initializes the CSVLoader with optional encoding and delimiter.
    #  @param encoding Encoding of the CSV file (default: "utf-8").
    #  @param delimiter Delimiter used in the CSV file (default: ",").
    def __init__(self, encoding="utf-8", delimiter=","):
        self.encoding = encoding
        self.delimiter = delimiter

    ## @brief Loads a CSV file and returns its rows as a list of dictionaries.
    #
    #  Assumes each row in the CSV contains a string dictionary.
    #
    #  @param file_path Path to the CSV file.
    #  @return List of dictionaries parsed from the CSV file.
    def load_as_dicts(self, file_path):
        with open(file_path, newline="", encoding=self.encoding) as csvfile:
            reader = csv.reader(csvfile, delimiter=self.delimiter)
            next(reader, None)  # Skip CSV header
            return [convert_to_dict(row[0]) for row in reader]


## @brief Converts a string representation of a dictionary into an actual dictionary.
#
#  This function uses eval(), which assumes the string is safe and correctly formatted.
#
#  @param str_dict A string representing a Python dictionary.
#  @return A Python dictionary object parsed from the string.
def convert_to_dict(str_dict):
    return eval(str_dict)
