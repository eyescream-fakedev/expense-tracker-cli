"""Business logic for expense operations."""

from datetime import datetime


def calculate_total(expenses: list[dict]) -> float:
    """
    Calculate the total amount of expenses.

    Args:
        expenses (list[dict]): A list of expense dictionaries.

    Returns:
        float: The total amount of expenses.
    """
    return sum(expense["amount"] for expense in expenses)


def filter_by_month(expenses: list[dict], month: int) -> list[dict]:
    """
    Filter expenses by a specific month.

    Args:
        expenses (list[dict]): A list of expense dictionaries.
        month (int): The month to filter by.

    Returns:
        list[dict]: A list of expenses from the specified month.
    """
    # Validation: empty list and missing 'date' key
    # - empty list should return an empty list
    # - missing 'date' key should raise a KeyError
    for expense in expenses:
        if "date" not in expense:
            raise KeyError("Missing 'date' key in expense")

    filtered_expenses = []
    for expense in expenses:
        dt = datetime.strptime(expense["date"], "%Y-%m-%d")
        if dt.month == month:
            filtered_expenses.append(expense)
    return filtered_expenses


def filter_by_year(expenses: list[dict], year: int) -> list[dict]:
    """
    Filter expenses by a specific year.

    Args:
        expenses (list[dict]): A list of expense dictionaries.
        year (int): The year to filter by.

    Returns:
        list[dict]: A list of expenses from the specified year.
    """
    if not isinstance(year, int):
        raise ValueError("Year must be an integer")

    filtered_expenses = []
    for expense in expenses:
        dt = datetime.strptime(expense["date"], "%Y-%m-%d")
        if dt.year == year:
            filtered_expenses.append(expense)
    return filtered_expenses


def add_expense(expenses: list[dict], new_expense: dict) -> list[dict]:
    """
    Add a new expense to the list of expenses.

    Args:
        expenses (list[dict]): A list of expense dictionaries.
        new_expense (dict): The new expense to add.

    Returns:
        list[dict]: The updated list of expenses with the new expense added.
    """
    # Validation:
    # - required keys must be present
    required_keys = ["description", "amount", "date"]
    for key in required_keys:
        if key not in new_expense:
            raise KeyError(f"Missing '{key}' key in expense")
    # - Check date format and value
    if not is_valid_date(new_expense["date"]):
        raise ValueError("Date must be in YYYY-MM-DD format")
    if not new_expense["description"].strip():
        raise ValueError("Expense description must not be empty")
    # - Check amount is less than 1
    if new_expense["amount"] <= 0:
        raise ValueError("Expense amount must be greater than 0")

    new_expense_copy = new_expense.copy()
    new_expense_copy["id"] = _generate_next_id(expenses)
    return expenses + [new_expense_copy]


def delete_expense(expenses: list[dict], expense_id: int) -> list[dict]:
    """
    Delete an expense from the list of expenses.

    Args:
        expenses (list[dict]): A list of expense dictionaries.
        expense_id (int): The ID of the expense to delete.

    Returns:
        list[dict]: The updated list of expenses with the specified expense removed.
    """
    expenses_copy = expenses.copy()

    for expense in expenses_copy:
        if expense["id"] == expense_id:
            expenses_copy.remove(expense)
            return expenses_copy
    raise ValueError(f"Expense with ID {expense_id} not found")


def is_valid_date(date: str) -> bool:
    """
    Check if the date string is in the format "YYYY-MM-DD" and the year, month, and day are valid numbers.

    Args:
        date (str): The date string to check.

    Returns:
        bool: True if the date is valid, False otherwise.
    """
    try:
        datetime.strptime(date, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def filter_by_category(expenses: list[dict], category: str) -> list[dict]:
    """
    Filter expenses by category.

    Args:
        expenses (list[dict]): A list of expense dictionaries.
        category (str): The category to filter by.

    Returns:
        list[dict]: A list of expenses that match the specified category.
    """
    result = []
    for expense in expenses:
        if expense.get("category") == category:
            result.append(expense)
    return result


def _generate_next_id(expenses: list[dict]) -> int:
    """
    Generate the next ID for a new expense.

    Args:
        expenses (list[dict]): A list of expense dictionaries.

    Returns:
        int: The next available ID for a new expense.
    """
    max_id = max((e.get("id", 0) for e in expenses), default=0)
    return max_id + 1
