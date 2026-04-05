"""Test cases for the expenses module."""

import pytest

import expense_tracker.expenses as expense


def test_calculate_total_sums_all_amounts():
    """Test that calculate_total returns the sum of all expense amounts."""
    # Arrange
    # - Create a list of expense dicts
    # - What data do I need? (Just the 'amount' key matter for this test function)
    expenses = [
        {"amount": 10.0},
        {"amount": 20.0},
        {"amount": 30.0},
    ]
    # Act
    result = expense.calculate_total(expenses)
    # Assert
    assert result == 60.0


def test_filter_by_month_returns_expenses_from_specific_month():
    """Test that filter_by_month returns expenses from a specific month."""
    # Arrange
    # - Create a list of expense dicts with a 'amount' and 'date' key, the format is "year-month-day"
    expenses = [
        {"amount": 10, "date": "2026-02-01"},
        {"amount": 20, "date": "2026-02-14"},
        {"amount": 30, "date": "2026-03-05"},
    ]

    # Act
    # - Filter by month
    result = expense.filter_by_month(expenses, month=2)

    # Assert
    # - Assert that the result contains only expenses from the specified month
    assert len(result) == 2
    assert result[0]["amount"] == 10
    assert result[1]["amount"] == 20


def test_filter_by_month_with_missing_date_key():
    """Test that filter_by_month raises a KeyError when the 'date' key is missing from an expense."""
    # Arrange
    expenses = [
        {"amount": 10, "description": "Groceries"},
        {"amount": 20, "description": "Dinner"},
    ]

    # Act & Assert
    with pytest.raises(KeyError):
        expense.filter_by_month(expenses, month=2)


def test_filter_by_year_from_specific_year():
    """Test that filter_by_year returns the correct expenses for a given year."""
    # Arrange
    expenses = [
        {"amount": 10, "description": "Groceries", "date": "2026-02-01"},
        {"amount": 20, "description": "Dinner", "date": "2026-02-14"},
        {"amount": 30, "description": "Lunch", "date": "2026-02-28"},
        {"amount": 40, "description": "Snacks", "date": "2027-03-01"},
    ]

    # Act
    result = expense.filter_by_year(expenses, year=2026)

    # Assert
    assert len(result) == 3


def test_filter_by_year_not_numeric_raises_error():
    """Test that filter_by_year raises a ValueError when the year is not numeric."""
    # Arrange
    expenses = [
        {"amount": 10, "description": "Groceries", "date": "2026-02-01"},
        {"amount": 20, "description": "Dinner", "date": "2026-02-14"},
        {"amount": 30, "description": "Lunch", "date": "2026-02-28"},
        {"amount": 40, "description": "Snacks", "date": "2027-03-01"},
    ]

    # Act & Assert
    with pytest.raises(ValueError):
        expense.filter_by_year(expenses, year="2026")  # pyright: ignore[reportArgumentType]


def test_add_expense_adds_to_the_expenses_list():
    """Test that add_expense adds a new expense to the expenses list."""
    # Arrange
    # - Create a list of expense dictionaries with a 'description', 'amount', and 'date' key

    expenses = [
        {"description": "Groceries", "amount": 100.0, "date": "2026-02-01"},
        {"description": "Dinner", "amount": 50.0, "date": "2026-02-14"},
    ]

    new_expense = {
        "description": "Lunch",
        "amount": 30.0,
        "date": "2026-02-28",
    }

    # Act
    # - Call add_expense with the current expenses and new expense
    updated_expenses = expense.add_expense(
        expenses=expenses,
        new_expense=new_expense,
    )

    # Assert
    # - Assert that the updated expenses list contains the new expense
    assert len(updated_expenses) == len(expenses) + 1


def test_add_expense_rejects_negative_amount():
    """
    Test that adding an expense with a negative amount raises a ValueError.
    """
    # Arrange: Create expense with negative amount
    # - Create a list of expense dictionaries with a 'description', 'amount', and 'date' key
    # - Create a new expense with a negative amount
    expenses = [
        {"description": "Groceries", "amount": 100.0, "date": "2026-02-01"},
        {"description": "Dinner", "amount": 50.0, "date": "2026-02-14"},
    ]

    new_expense = {
        "description": "Lunch",
        "amount": -30.0,
        "date": "2026-02-28",
    }

    # Act & Assert: Should raise ValueError
    with pytest.raises(ValueError):
        expense.add_expense(expenses, new_expense)


def test_add_expense_rejects_empty_description():
    """Test that adding an expense with an empty description raises a ValueError."""
    expenses = [
        {"description": "Groceries", "amount": 100.0, "date": "2026-02-01"},
        {"description": "Dinner", "amount": 50.0, "date": "2026-02-14"},
    ]

    new_expense = {
        "description": "",
        "amount": 30.0,
        "date": "2026-02-28",
    }

    with pytest.raises(ValueError):
        expense.add_expense(expenses, new_expense)


def test_add_expense_rejects_zero_amount():
    """Test that adding an expense with a zero amount raises a ValueError."""
    expenses = [
        {"description": "Groceries", "amount": 100.0, "date": "2026-02-01"},
        {"description": "Dinner", "amount": 50.0, "date": "2026-02-14"},
    ]

    new_expense = {
        "description": "Lunch",
        "amount": 0.0,
        "date": "2026-02-28",
    }

    with pytest.raises(ValueError):
        expense.add_expense(expenses, new_expense)


def test_add_expense_missing_key():
    """Test that adding an expense with a missing key raises a KeyError."""
    expenses = [
        {"description": "Groceries", "amount": 100.0, "date": "2026-02-01"},
        {"description": "Dinner", "amount": 50.0, "date": "2026-02-14"},
    ]

    new_expense = {
        "description": "Lunch",
        "amount": 30.0,
    }

    with pytest.raises(KeyError):
        expense.add_expense(expenses, new_expense)


def test_delete_expense_removes_expense_by_id():
    """Test that delete_expense removes the expense with the specified ID from the list."""
    # Arrange
    expenses = [
        {"id": 1, "description": "Groceries", "amount": 100.0, "date": "2026-02-01"},
        {"id": 2, "description": "Dinner", "amount": 50.0, "date": "2026-02-14"},
        {"id": 3, "description": "Lunch", "amount": 30.0, "date": "2026-02-28"},
    ]
    # Act
    result = expense.delete_expense(expenses, 1)
    # Assert
    # - Result should be a list with one item (the remaining expense)
    # - The remaining expense should have the correct ID
    assert len(result) == 2
    assert result[0]["id"] != 1
    assert len(expenses) == 3


def test_delete_expense_raises_error_when_id_not_found():
    """Test that delete_expense raises a ValueError when the expense ID is not found."""
    # Arrange
    expenses = [
        {"id": 1, "description": "Groceries", "amount": 100.0, "date": "2026-02-01"},
        {"id": 2, "description": "Dinner", "amount": 50.0, "date": "2026-02-14"},
        {"id": 3, "description": "Lunch", "amount": 30.0, "date": "2026-02-28"},
    ]

    # Act & Assert
    with pytest.raises(ValueError):
        expense.delete_expense(expenses, expense_id=4)


def test_delete_expense_raises_error_when_expenses_empty():
    """Test that delete_expense raises a ValueError when the expenses list is empty."""
    # Arrange
    expenses = []
    # Act & Assert
    with pytest.raises(ValueError):
        expense.delete_expense(expenses, 1)


def test_is_valid_date_returns_true_for_valid_date():
    """Test that is_valid_date returns True for a valid date string."""
    # Arrange
    valid_date = "2026-02-01"
    # Act
    result = expense.is_valid_date(valid_date)
    # Assert
    assert result is True


def test_is_valid_date_returns_false_for_invalid_date():
    """Test that is_valid_date returns False for an invalid date string."""
    # Arrange
    invalid_date = "2026-02-31"
    # Act
    result = expense.is_valid_date(invalid_date)
    # Assert
    assert result is False


def test_is_valid_data_returns_false_for_wrong_format():
    """Test that is_valid_date returns False for a date string with wrong format."""

    assert expense.is_valid_date("2026/02/01") is False  # Slashes
    assert expense.is_valid_date("02-01-2026") is False  # Day first
    assert expense.is_valid_date("March 1, 2026") is False  # Text


def test_add_expense_with_category():
    """Test that add_expense correctly adds an expense with a category."""
    # Arrange
    expenses = []
    new_expense = {
        "description": "Groceries",
        "amount": 50.00,
        "date": "2026-02-01",
        "category": "Food",
    }

    # Act
    result = expense.add_expense(expenses, new_expense)
    # Assert
    assert len(result) == 1
    assert result[0]["category"] == "Food"


def test_add_expense_without_category():
    """Test that add_expense correctly adds an expense without a category."""
    # Arrange
    expenses = []
    new_expense = {
        "description": "Groceries",
        "amount": 50.00,
        "date": "2026-02-01",
    }
    # Act
    result = expense.add_expense(expenses, new_expense)

    # Assert
    assert len(result) == 1
    assert "category" not in result[0]


def test_filter_by_category_returns_matching_expenses():
    """Test that filter_by_category returns matching expenses by category."""
    # Arrange
    # - Create a list of 3-4 expenses with different 'categories'
    expenses = [
        {
            "description": "Groceries",
            "amount": 50.00,
            "date": "2026-02-01",
            "category": "Food",
        },
        {
            "description": "Transport",
            "amount": 20.00,
            "date": "2026-02-02",
            "category": "Transport",
        },
        {
            "description": "Entertainment",
            "amount": 10.00,
            "date": "2026-02-03",
            "category": "Entertainment",
        },
        {
            "description": "Snacks",
            "amount": 15.00,
            "date": "2026-02-04",
            "category": "Food",
        },
    ]
    # Act
    result = expense.filter_by_category(expenses, "Food")

    # Assert
    assert len(result) == 2
    for item in result:
        assert item.get("category") == "Food"


def test_filter_by_category_with_no_match():
    """Test that filter_by_category returns an empty list when no match is found."""
    # Arrange
    expenses = [
        {
            "description": "Groceries",
            "amount": 50.00,
            "date": "2026-02-01",
            "category": "Food",
        },
        {
            "description": "Transport",
            "amount": 20.00,
            "date": "2026-02-02",
            "category": "Transport",
        },
        {
            "description": "Entertainment",
            "amount": 10.00,
            "date": "2026-02-03",
            "category": "Entertainment",
        },
        {
            "description": "Snacks",
            "amount": 15.00,
            "date": "2026-02-04",
            "category": "Food",
        },
    ]

    # Act
    result = expense.filter_by_category(expenses, "Utility")

    # Assert
    assert len(result) == 0


def test_add_expense_allows_less_than_one():
    # Arrange
    expenses = []
    new_expenses = {
        "description": "Coffee",
        "amount": 0.50,
        "date": "2026-04-02",
    }
    # Act
    result = expense.add_expense(expenses, new_expenses)
    # Assert
    assert len(result) == 1
    assert result[0]["amount"] == 0.50


def test_check_budget_exceeded_returns_true_when_over():
    """Test that check_budget_exceeded returns True when the budget is exceeded."""
    # Arrange
    expenses = [
        {"amount": 60},
        {"amount": 50},
    ]
    budget_amount = 100

    # Act
    result = expense.check_budget_exceeded(expenses, budget_amount)
    # Assert
    assert result is True


def test_check_budget_exceeded_return_false_when_under():
    """Test that check_budget_exceeded returns False when the budget is not exceeded."""
    # Arrange
    expenses = [
        {"amount": 50},
        {"amount": 30},
    ]
    budget_amount = 100
    # Act
    result = expense.check_budget_exceeded(expenses, budget_amount)
    # Assert
    assert result is False


def test_check_budget_exceeded_returns_false_when_exact():
    """Test that check_budget_exceeded returns False when the budget is exactly met."""
    # Arrange
    expenses = [
        {"amount": 50},
        {"amount": 50},
    ]
    budget_amount = 100
    # Act
    result = expense.check_budget_exceeded(expenses, budget_amount)
    # Assert
    assert result is False
