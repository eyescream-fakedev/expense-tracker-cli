"""Test the CLI module."""

from pathlib import Path

import pytest

from expense_tracker.cli import DATA_FILE_PATH, main, show_summary
from expense_tracker.expenses import export_to_csv

# from expense_tracker.storage import DatabaseManager


def test_add_expense_with_category_cli(monkeypatch: pytest.MonkeyPatch):
    """Test adding an expense with a category via the CLI."""
    # Arrange
    # - Create a list to capture calls: calls = []
    # - Create spy function:def spy_add_expense_cli(desc, date,category=None):
    calls = []

    def spy_add_expense_cli(desc, amount, date, category=None, data_file_path=None):
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

    def spy_list_expenses_cli(
        month=None, year=None, category=None, data_file_path=None
    ):
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


def test_summary_with_category(monkeypatch: pytest.MonkeyPatch):
    """Test show_summary as a CLI command with a category filter."""
    # Arrange
    call_args = {}

    def spy_show_summary(month, year, category, data_file_path=None):
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

    def spy_delete_expense_cli(expense_id, data_file_path=None):
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

    def spy_list_expenses(month=None, year=None, category=None, data_file_path=None):
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
    """Verify CLI raises on unexpected error."""

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


def test_list_expenses_uses_custom_data_file(monkeypatch: pytest.MonkeyPatch):
    """Verify CLI uses custom data file when specified."""
    # Arrange
    call_args = {}
    # original_init = DatabaseManager.__init__

    def spy_init(self, data_file_path: str):
        call_args["data_file_path"] = data_file_path

    monkeypatch.setattr("expense_tracker.cli.DatabaseManager.__init__", spy_init)
    monkeypatch.setattr(
        "expense_tracker.cli.DatabaseManager.load_expenses", lambda self: []
    )
    monkeypatch.setattr(
        "sys.argv", ["expense_tracker", "list", "--data-file", "/tmp/test.json"]
    )
    # Act
    main()
    # Assert
    assert call_args["data_file_path"] == Path("/tmp/test.json")


def test_list_expenses_shows_category_column(capsys, monkeypatch: pytest.MonkeyPatch):
    """Verify list output includes category column."""
    # Arrange
    expense = [
        {
            "id": 1,
            "description": "Test expense",
            "amount": 100.00,
            "category": "Test category",
            "date": "2026-04-03",
        }
    ]

    def spy_load_expenses(self):
        return expense

    monkeypatch.setattr(
        "expense_tracker.cli.DatabaseManager.load_expenses", spy_load_expenses
    )
    monkeypatch.setattr("sys.argv", ["expense_tracker", "list"])
    # Act
    main()
    # Assert
    captured = capsys.readouterr()
    assert "Test category" in captured.out


def test_list_expenses_handles_missing_file_gracefully(
    capsys, monkeypatch: pytest.MonkeyPatch
):
    """Verify list command gracefully handles a missing data file."""

    # Arrange
    def raise_file_not_found(self):
        raise FileNotFoundError("No such file")

    monkeypatch.setattr(
        "expense_tracker.cli.DatabaseManager.load_expenses", raise_file_not_found
    )

    monkeypatch.setattr("sys.argv", ["expense_tracker", "list"])
    # Act & Assert
    with pytest.raises(SystemExit) as exc_info:
        main()

    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert "error" in captured.out.lower()


def test_export_to_csv_creates_file_with_expenses():
    """Verify export_to_csv creates a CSV file with the correct content."""
    # Arrange
    expenses = [
        {
            "id": 1,
            "description": "Test expense",
            "amount": 100.00,
            "category": "Test category",
            "date": "2026-04-03",
        },
        {
            "id": 2,
            "description": "Another expense",
            "amount": 50.00,
            "category": "Another category",
            "date": "2026-04-04",
        },
    ]

    output_path = Path("/tmp/test_export.csv")
    # Act
    export_to_csv(expenses, output_path)
    # Assert
    assert output_path.exists()
    content = output_path.read_text()
    lines = content.strip().split("\n")
    assert len(lines) == 3  # header + 2 expenses
    assert lines[0] == "id,date,description,category,amount"
    assert "Test expense" in lines[1]
    assert "Another expense" in lines[2]


def test_export_command_creates_csv_file(monkeypatch: pytest.MonkeyPatch):
    """Verify export command creates a CSV file with the correct content."""
    # Arrange
    monkeypatch.setattr(
        "sys.argv", ["expense_tracker", "export", "--output", "/tmp/test_export.csv"]
    )
    monkeypatch.setattr(
        "expense_tracker.cli.DatabaseManager.load_expenses", lambda self: []
    )
    # Act
    main()
    # Assert
    output_path = Path("/tmp/test_export.csv")
    assert output_path.exists()
    content = output_path.read_text()
    lines = content.strip().split("\n")
    assert len(lines) == 1  # only header
    assert lines[0] == "id,date,description,category,amount"


def test_budget_check_shows_exceeded_warning(capsys, monkeypatch: pytest.MonkeyPatch):
    """Verify budget check shows an exceeded warning when expenses exceed the budget."""
    # Arrange
    expenses = [{"amount": 50.00}, {"amount": 50}, {"amount": 50}]
    monkeypatch.setattr(
        "expense_tracker.cli.DatabaseManager.load_expenses", lambda self: expenses
    )
    monkeypatch.setattr("sys.argv", ["expense_tracker", "budget", "--amount", "100"])
    # Act
    main()
    # Assert
    captured = capsys.readouterr()
    assert "Budget exceeded" in captured.out


def test_budget_check_shows_ok_message(capsys, monkeypatch: pytest.MonkeyPatch):
    """Verify budget check shows an OK message when expenses are within the budget."""
    # Arrange
    expenses = [{"amount": 50.00}, {"amount": 50}]
    monkeypatch.setattr(
        "expense_tracker.cli.DatabaseManager.load_expenses", lambda self: expenses
    )
    monkeypatch.setattr("sys.argv", ["expense_tracker", "budget", "--amount", "100"])
    # Act
    main()
    # Assert
    captured = capsys.readouterr()
    assert "Budget OK" in captured.out


def test_budget_check_with_month_filter(capsys, monkeypatch: pytest.MonkeyPatch):
    """Verify budget check with month filter shows an OK message when expenses are within the budget for the given month."""
    # Arrange
    expenses = [
        {"amount": 200, "date": "2026-01-15"},
        {"amount": 30, "date": "2026-02-10"},
    ]
    monkeypatch.setattr(
        "expense_tracker.cli.DatabaseManager.load_expenses", lambda self: expenses
    )
    monkeypatch.setattr(
        "sys.argv", ["expense_tracker", "budget", "--amount", "100", "--month", "2"]
    )
    # Act
    main()
    # Assert
    captured = capsys.readouterr()
    assert "Budget OK" in captured.out


def test_budget_check_with_empty_expenses(capsys, monkeypatch: pytest.MonkeyPatch):
    """Verify budget check with empty expenses shows an OK message with zero spend."""
    # Arrange
    monkeypatch.setattr(
        "expense_tracker.cli.DatabaseManager.load_expenses", lambda self: []
    )
    monkeypatch.setattr("sys.argv", ["expense_tracker", "budget", "--amount", "100"])
    # Act
    main()
    # Assert
    captured = capsys.readouterr()
    assert "Budget OK" in captured.out
    assert "$0.00 spent" in captured.out


def test_budget_check_handles_missing_file(capsys, monkeypatch: pytest.MonkeyPatch):
    """Verify budget check handles missing file gracefully."""

    # Arrange
    def raise_file_not_found(self):
        raise FileNotFoundError("No such file")

    # Monkeypatch load_expenses to raise FileNotFoundError
    monkeypatch.setattr(
        "expense_tracker.cli.DatabaseManager.load_expenses", raise_file_not_found
    )
    monkeypatch.setattr("sys.argv", ["expense_tracker", "budget", "--amount", "100"])
    # Act & Assert
    with pytest.raises(SystemExit) as exc_info:
        main()

    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert "File missing" in captured.out


def test_budget_check_with_category_filter(capsys, monkeypatch: pytest.MonkeyPatch):
    """Verify budget check with category filter works correctly."""
    # Arrange
    expenses = [
        {"category": "Food", "amount": 200.0},
        {"category": "Transport", "amount": 30.0},
    ]
    monkeypatch.setattr(
        "expense_tracker.cli.DatabaseManager.load_expenses", lambda self: expenses
    )
    monkeypatch.setattr(
        "sys.argv",
        ["expense_tracker", "budget", "--amount", "100", "--category", "Transport"],
    )
    # Act
    main()
    # Assert
    captured = capsys.readouterr()
    assert "Budget OK" in captured.out
    assert "$30.00 spent" in captured.out


def test_default_data_file_path_is_user_writable():
    """Verify the default data file path is user-writable."""
    # Assert
    assert ".expense-tracker" in str(DATA_FILE_PATH)
    assert str(Path.home()) in str(DATA_FILE_PATH)


def test_budget_check_exits_with_error_on_missing_file(monkeypatch: pytest.MonkeyPatch):
    """Verify the budget check exits with an error when the file is missing."""

    # Arrange
    def raise_file_not_found(self):
        raise FileNotFoundError("No such file")

    monkeypatch.setattr(
        "expense_tracker.cli.DatabaseManager.load_expenses", raise_file_not_found
    )

    monkeypatch.setattr("sys.argv", ["expense_tracker", "budget", "--amount", "100"])

    # Act & Assert
    with pytest.raises(SystemExit) as exc_info:
        main()

    assert exc_info.value.code == 1


def test_export_rejects_invalid_month(capsys, monkeypatch: pytest.MonkeyPatch):
    """Verify the export command rejects an invalid month."""
    # Arrange
    monkeypatch.setattr(
        "sys.argv",
        ["expense_tracker", "export", "--output", "/tmp/test.csv", "--month", "99"],
    )
    # Act & Assert
    with pytest.raises(SystemExit):
        main()

    captured = capsys.readouterr()
    assert "error" in captured.err.lower()


def test_export_rejects_invalid_year(capsys, monkeypatch: pytest.MonkeyPatch):
    """Verify the export command rejects an invalid year."""
    # Arrange
    monkeypatch.setattr(
        "sys.argv",
        ["expense_tracker", "export", "--output", "/tmp/test.csv", "--year", "abc"],
    )
    # Act & Assert
    with pytest.raises(SystemExit):
        main()
    captured = capsys.readouterr()
    assert "error" in captured.err.lower()


def test_budget_reject_invalid_month(capsys, monkeypatch: pytest.MonkeyPatch):
    # Arrange
    monkeypatch.setattr(
        "sys.argv", ["expense_tracker", "budget", "--amount", "100", "--month", "13"]
    )
    # Act & Assert
    with pytest.raises(SystemExit):
        main()
    captured = capsys.readouterr()
    assert "error" in captured.err.lower()
