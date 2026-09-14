import json
import os


class DataManager:
    # Save data to a JSON file
    def save_data(self, filename, data):
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)

    # Load data from a JSON file
    def load_data(self, filename):
        if not os.path.exists(filename):
            return []

        try:
            with open(filename, "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, OSError):
            return []