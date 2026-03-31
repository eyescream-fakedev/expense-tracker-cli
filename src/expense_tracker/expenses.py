"""Business logic for expense operations."""


def calculate_total(expenses: list[dict]) -> float:
    """
    Calculate the total amount of expenses.

    Args:
        expenses (list[dict]): A list of expense dictionaries.

    Returns:
        float: The total amount of expenses.
    """
    return sum(expense["amount"] for expense in expenses)


def filter_by_month(expenses: list[dict], year: int, month: int) -> list[dict]:
    """
    Filter expenses by a specific month.

    Args:
        expenses (list[dict]): A list of expense dictionaries.
        year (int): The year to filter by.
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

    return [
        expense
        for expense in expenses
        if expense["date"].startswith(f"{year}-{month:02d}-")
    ]


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
    # - description must not be empty
    # - amount must be greater than 0
    required_keys = ["description", "amount", "date"]
    for key in required_keys:
        if key not in new_expense:
            raise KeyError(f"Missing '{key}' key in expense")
    if not new_expense["description"].strip():
        raise ValueError("Expense description must not be empty")

    if new_expense["amount"] < 1:
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
