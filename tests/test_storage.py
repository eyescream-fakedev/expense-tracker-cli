import json
import os
import sys
from pathlib import Path

import pytest

src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))
from expense_tracker.storage import DatabaseManager  # noqa: E402


def test_load_expenses_returns_empty_list_when_file_does_not_exist(tmp_path):
    """Load expenses returns an empty list when the file does not exist."""
    # Arrange
    # - Remove the file if it exists
    # - Create storage instance
    data_file_path = tmp_path / "test_expenses.json"
    db_manager = DatabaseManager(data_file_path)

    # Act
    # - Call load_expenses()
    result = db_manager.load_expenses()

    # Assert
    # - Result should be an empty list []
    # - File should still not exists (no side effects)
    assert isinstance(result, list)
    assert len(result) == 0
    assert not data_file_path.exists()


def test_save_expenses_creates_file_with_data(tmp_path):
    """Saving expenses creates the file with correct JSON structure."""
    # Arrange
    data_file_path = tmp_path / "test_expenses.json"
    db_manager = DatabaseManager(data_file_path)
    test_expenses = [
        {
            "id": 1,
            "description": "Lunch",
            "amount": 20.0,
            "date": "2024-08-06",
        }
    ]

    # Act
    db_manager.save_expenses(test_expenses)

    # Assert
    assert data_file_path.exists()
    # Read and parse the file

    with open(data_file_path, "r") as file:
        saved_data = json.load(file)

    # Verify content matches
    assert saved_data == test_expenses


def test_load_expenses_reads_from_existing_file(tmp_path):
    """Loading expenses from an existing file returns the correct data."""
    # Arrange
    data_file_path = tmp_path / "test_expenses.json"
    db_manager = DatabaseManager(data_file_path)
    expected_expenses = [
        {
            "id": 1,
            "description": "Lunch",
            "amount": 20.0,
            "date": "2024-08-06",
        },
        {
            "id": 2,
            "description": "Dinner",
            "amount": 10.0,
            "date": "2024-08-06",
        },
    ]
    # Pre-create the file with data
    with open(data_file_path, "w") as file:
        json.dump(expected_expenses, file)

    # Act
    result = db_manager.load_expenses()

    # Assert
    assert result == expected_expenses


def test_save_expenses_overwrites_existing_file(tmp_path):
    """Saving expenses overwrites the existing file with updated data."""
    # Arrange
    data_file_path = tmp_path / "test_expenses.json"
    db_manager = DatabaseManager(data_file_path)
    initial_expenses = [
        {
            "id": 1,
            "description": "Lunch",
            "amount": 20.0,
            "date": "2024-08-06",
        }
    ]
    updated_expenses = [
        {
            "id": 1,
            "description": "Dinner",
            "amount": 10.0,
            "date": "2024-08-06",
        }
    ]
    # Pre-create the file with initial data
    with open(data_file_path, "w") as file:
        json.dump(initial_expenses, file)

    # Act
    db_manager.save_expenses(updated_expenses)

    # Assert
    with open(data_file_path, "r") as file:
        saved_data = json.load(file)
    assert saved_data == updated_expenses
    assert saved_data != initial_expenses


def test_load_expenses_handles_corrupted_json(tmp_path):
    """Loading expenses from a file with invalid JSON raises JSONDecodeError."""
    # Arrange
    # Create a file with corrupted JSON
    data_file_path = tmp_path / "test_expenses.json"
    db_manager = DatabaseManager(data_file_path)

    # Write corrupted JSON to file
    with open(data_file_path, "w") as file:
        file.write("{'broken':}")

    with pytest.raises(json.JSONDecodeError):
        # Act & Assert - should raise JSONDecodeError
        db_manager.load_expenses()


def test_load_expenses_handles_wrong_format(tmp_path):
    """Loading expenses from a file with wrong format JSON."""
    # Arrange
    data_file_path = tmp_path / "test_expenses.json"
    db_manager = DatabaseManager(data_file_path)

    # Write with valid JSON but wrong structure (example: a wrapper object instead of a plaint list)
    with open(data_file_path, "w") as file:
        file.write(
            '{"expenses": [{"id": 1, "description": "Lunch", "amount": 20.0, "date": "2024-08-06"}]}'
        )

    # Act & Assert: Should raise ValueError (because the type is correct - it's a list but the structure is wrong)
    with pytest.raises(TypeError):
        db_manager.load_expenses()


def test_load_expenses_raises_permission_error_when_no_read_access(tmp_path):
    """Test that loading expenses raises PermissionError when the file is not readable."""
    # Arrange
    # - Create a file with some data
    # - Remove read permission using os.chmod()
    data_file_path = tmp_path / "test_expenses.json"
    db_manager = DatabaseManager(data_file_path)

    with open(data_file_path, "w") as file:
        file.write(
            '[{"id": 1, "description": "Lunch", "amount": 20.0, "date": "2024-08-06"}]'
        )
    os.chmod(data_file_path, 0o000)  # Remove read permission

    # Act & Assert: Should raise PermissionError (because the file is not readable)
    try:
        with pytest.raises(PermissionError):
            db_manager.load_expenses()
    finally:
        os.chmod(data_file_path, 0o644)  # Restore read permission
