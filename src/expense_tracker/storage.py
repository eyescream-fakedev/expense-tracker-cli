"""A module for handling the data."""

import json
from pathlib import Path


class DatabaseManager:
    """
    DatabaseManager class handles read,save,update and delete data.

    Properties:
        self.data_file_path: Path - file path of data
    """

    def __init__(self, data_file_path: Path) -> None:
        self.data_file_path: Path = data_file_path

    def load_expenses(self) -> list[dict]:
        """
        Load expenses from JSON file.

        Returns empty list if file doesn't exist.

        Raises:
            TypeError: If the data is not a list
            ValueError: If any item in the list is not a dict
        """
        if not self.data_file_path.exists():
            return []

        with open(self.data_file_path, "r") as file:
            data = json.load(file)

        if not isinstance(data, list):
            raise TypeError(f"Expected list, got {type(data).__name__}")

        for i, item in enumerate(data):
            if not isinstance(item, dict):
                raise ValueError(
                    f"Expected dict, got {type(item).__name__} at index {i}"
                )

        return data

    def save_expenses(self, expenses: list[dict]) -> None:
        """Save expenses to JSON file (overwritten existing file.)"""

        with open(self.data_file_path, "w") as file:
            json.dump(expenses, file)
