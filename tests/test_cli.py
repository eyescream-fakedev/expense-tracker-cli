"""Test the CLI module."""

import pytest

from expense_tracker.cli import main


def test_add_expense_with_category_cli(monkeypatch: pytest.MonkeyPatch):
    """Test adding an expense with a category via the CLI."""
    # Arrange
    # - Create a list to capture calls: calls = []
    # - Create spy function:def spy_add_expense_cli(desc, date,category=None):
    calls = []

    def spy_add_expense_cli(desc, amount, date, category=None):
        calls.append(
            {
                "description": desc,
                "amount": amount,
                "date": date,
                "category": category,
            }
        )

    monkeypatch.setattr("expense_tracker.cli.add_expense_cli", spy_add_expense_cli)
    monkeypatch.setattr(
        "sys.argv",
        ["expense_tracker", "add", "Lunch", "25.0", "2026-04-02", "--category", "Food"],
    )

    # Act
    # - Call main() (it will use mocked sys.argv and mocked add_expense_cli)
    main()

    # Assert
    assert len(calls) == 1
    assert calls[0] == {
        "description": "Lunch",
        "amount": 25.0,
        "date": "2026-04-02",
        "category": "Food",
    }


def test_list_expenses_with_category_filter(monkeypatch: pytest.MonkeyPatch):
    """Test list_expenses as a CLI command with a category filter."""
    # Arrange

    call_args = {}

    def spy_list_expenses_cli(month=None, year=None, category=None):
        call_args["month"] = month
        call_args["year"] = year
        call_args["category"] = category

    monkeypatch.setattr("expense_tracker.cli.list_expenses", spy_list_expenses_cli)
    monkeypatch.setattr("sys.argv", ["expense_tracker", "list", "--category", "Food"])

    # Act
    main()

    # Assert
    assert call_args["category"] == "Food"
    assert call_args["month"] is None
    assert call_args["year"] is None


def test_sumary_with_category(monkeypatch: pytest.MonkeyPatch):
    # Arrange
    call_args = {}

    def spy_show_summary(month, year, category):
        call_args["month"] = month
        call_args["year"] = year
        call_args["category"] = category

    monkeypatch.setattr("expense_tracker.cli.show_summary", spy_show_summary)
    monkeypatch.setattr(
        "sys.argv", ["expense_tracker", "summary", "--category", "Food"]
    )

    # Act
    main()
    # Assert
    assert call_args["category"] == "Food"
    assert call_args["month"] is None
    assert call_args["year"] is None
