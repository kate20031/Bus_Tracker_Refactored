import csv
import ast

## @class CSVLoader
#  @brief Class for loading CSV data and converting stringified dictionaries into Python dictionaries.
#
#  The CSVLoader class reads a CSV file where each row contains a string representation
#  of a Python dictionary and returns a list of actual dictionaries.
class CSVLoader:
    ## @brief Constructor for CSVLoader.
    #  @param encoding The encoding used to open the CSV file (default: "utf-8").
    #  @param delimiter The delimiter used in the CSV file (default: ",").
    def __init__(self, encoding="utf-8", delimiter=","):
        self.encoding = encoding
        self.delimiter = delimiter

    ## @brief Loads a CSV file and returns its content as a list of dictionaries.
    #
    #  Assumes that each row (excluding the header) contains a single stringified dictionary.
    #
    #  @param file_path Path to the CSV file.
    #  @return A list of dictionaries parsed from the stringified data in the CSV.
    def load_as_dicts(self, file_path):
        with open(file_path, newline="", encoding=self.encoding) as csvfile:
            reader = csv.reader(csvfile, delimiter=self.delimiter)
            next(reader, None)  # Skip CSV header
            return [convert_to_dict(row[0]) for row in reader]


## @brief Safely converts a string representation of a dictionary into an actual dictionary.
#
#  This function uses ast.literal_eval to safely parse Python literals.
#
#  @param str_dict A string representing a Python dictionary.
#  @return A dictionary object parsed from the string.
#  @throws ValueError if the input string is not a valid dictionary.
def convert_to_dict(str_dict):
    try:
        return ast.literal_eval(str_dict)
    except (ValueError, SyntaxError) as e:
        raise ValueError(f"Invalid dictionary string: {str_dict}") from e
