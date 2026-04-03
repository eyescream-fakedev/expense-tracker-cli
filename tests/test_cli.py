"""Test the CLI module."""

import pytest

from expense_tracker.cli import main


def test_add_expense_with_category_cli(monkeypatch: pytest.MonkeyPatch):
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
