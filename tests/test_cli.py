"""Test the CLI module."""

import pytest

from expense_tracker.cli import main, show_summary


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
    """Test show_summary as a CLI command with a category filter."""
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


def test_delete_expense_routes_correctly(monkeypatch: pytest.MonkeyPatch):
    """Test delete_expense as a CLI command with an expense ID."""
    # Arrange
    call_args = {}

    def spy_delete_expense_cli(expense_id):
        call_args["expense_id"] = expense_id

    monkeypatch.setattr(
        "expense_tracker.cli.delete_expense_cli",
        spy_delete_expense_cli,
    )
    monkeypatch.setattr("sys.argv", ["expense_tracker", "delete", "5"])
    # Act
    main()
    # Assert
    assert call_args["expense_id"] == 5


def test_no_command_prints_help(capsys, monkeypatch: pytest.MonkeyPatch):
    """Test that no command prints the help message."""
    # Arrange
    monkeypatch.setattr("sys.argv", ["expense_tracker"])
    # Act
    main()
    # Assert
    captured = capsys.readouterr()
    assert "Expense Tracker CLI" in captured.out


def test_list_expenses_rejects_invalid_month(capsys, monkeypatch: pytest.MonkeyPatch):
    """Verify CLI handles invalid month values gracefully."""
    # Arrange
    monkeypatch.setattr("sys.argv", ["expense_tracker", "list", "--month", "99"])

    # Act & Assert
    with pytest.raises(SystemExit):
        main()

    captured = capsys.readouterr()
    assert "error" in captured.err.lower()


def test_list_expenses_accepts_valid_month_boundary(
    capsys, monkeypatch: pytest.MonkeyPatch
):
    """Verify CLI accepts valid month boundary values (1-12)."""
    # Arrange
    call_args = {}

    def spy_list_expenses(month=None, year=None, category=None):
        call_args["month"] = month
        call_args["year"] = year
        call_args["category"] = category

    monkeypatch.setattr("expense_tracker.cli.list_expenses", spy_list_expenses)
    monkeypatch.setattr("sys.argv", ["expense_tracker", "list", "--month", "12"])
    # Act
    main()
    # Assert
    assert call_args["month"] == 12


def test_list_expenses_rejects_month_zero(capsys, monkeypatch: pytest.MonkeyPatch):
    """Verify CLI rejects month zero."""
    # Arrange
    monkeypatch.setattr("sys.argv", ["expense_tracker", "list", "--month", "0"])
    # Act & Assert
    with pytest.raises(SystemExit):
        main()

    captured = capsys.readouterr()
    assert "error" in captured.err.lower()


def test_add_expense_rejects_invalid_date_format(
    capsys, monkeypatch: pytest.MonkeyPatch
):
    """Verify CLI rejects invalid date format."""
    # Arrange

    monkeypatch.setattr(
        "sys.argv", ["expense_tracker", "add", "Lunch", "25", "2026/04/02"]
    )

    # Act and Assert
    main()
    captured = capsys.readouterr()
    assert "error" in captured.out.lower()


def test_show_summary_raises_on_unexpected_error(monkeypatch: pytest.MonkeyPatch):
    # Arrange
    def raise_type_error():
        raise AttributeError("Unexpected error")

    monkeypatch.setattr(
        "expense_tracker.cli.DatabaseManager.load_expenses",
        lambda self: raise_type_error(),
    )

    # Act & Assert
    with pytest.raises(AttributeError):
        show_summary()
