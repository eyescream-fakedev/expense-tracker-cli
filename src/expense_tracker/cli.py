import argparse
import json
from pathlib import Path

from expense_tracker.expenses import (
    add_expense,
    calculate_total,
    delete_expense,
    export_to_csv,
    filter_by_category,
    filter_by_month,
    filter_by_year,
)
from expense_tracker.storage import DatabaseManager

SCRIPT_DIR = Path(__file__).parent
DATA_FILE_PATH = SCRIPT_DIR / "expenses.json"


def list_expenses(
    month: int | None = None,
    year: int | None = None,
    category: str | None = None,
    data_file_path: Path = DATA_FILE_PATH,
) -> None:
    """
    List all expenses for a given month and year.

    Args:
        month (int | None): The month to filter by, or None to list all months.
        year (int | None): The year to filter by, or None to list all years.
        category (str | None): The category to filter by, or None to list all categories.
    """
    # if month and/or year is provided, filter expenses accordingly
    try:
        db_manager = DatabaseManager(data_file_path)
        expenses = db_manager.load_expenses()
        result = expenses

        if year:
            result = filter_by_year(result, year)
        if month:
            result = filter_by_month(result, month)
        if category:
            result = filter_by_category(result, category)

        # print title with fixed-width column formatting
        print(
            f"{'ID':<5} {'Date':<12} {'Description':<25} {'Category':<15} {'Amount':>10}"
        )
        print("-" * 60)
        for expense in result:
            category = expense.get("category", "")
            print(
                f"{expense['id']:<5} {expense['date']:<12} {expense['description']:<25} {category:<15} ${expense['amount']:>8.2f}"
            )
    except ValueError as error:
        print(f"Error: {error}")
    except KeyError as error:
        print(f"Error: {error}")
    except FileNotFoundError as error:
        print(f"Error: {error}")


def add_expense_cli(
    description: str,
    amount: float,
    date: str,
    category: str | None,
    data_file_path: Path = DATA_FILE_PATH,
) -> None:
    """
    Add a new expense via CLI.

    Args:
        description (str): The expense description.
        amount (float): The expense amount.
        date (str): The expense date in YYYY-MM-DD format.
        category (str | None): The expense category.

    """
    try:
        # Load existing expenses
        db_manager = DatabaseManager(data_file_path)
        expenses = db_manager.load_expenses()

        # Create new expense
        new_expense = {
            "description": description,
            "amount": amount,
            "date": date,
            "category": category,
        }

        # Use business logic to add expense
        updated_expenses = add_expense(expenses, new_expense)

        # Save back
        db_manager.save_expenses(updated_expenses)
        # Print Success
        print(f"Added expense: {description} - ${amount:.2f}")
    except ValueError as error:
        print(f"Error: {error}")
    except KeyError as error:
        print(f"Error: {error}")
    except FileNotFoundError as error:
        print(f"Error: {error}")


def delete_expense_cli(
    expense_id: int,
    data_file_path: Path = DATA_FILE_PATH,
) -> None:
    """
    Delete an expense by its ID.

    Args:
        expense_id (int): The ID of the expense to delete.
    """
    try:
        db_manager = DatabaseManager(data_file_path)
        expenses = db_manager.load_expenses()
        updated_expenses = delete_expense(expenses, expense_id)
        db_manager.save_expenses(updated_expenses)
        print(f"Deleted expense with ID {expense_id}")
    except ValueError as error:
        print(f"Error: {error}")
    except KeyError as error:
        print(f"Error: {error}")
    except FileNotFoundError as error:
        print(f"Error: {error}")


def export_expenses_cli(
    output: Path,
    month: int | None = None,
    year: int | None = None,
    category: str | None = None,
    data_file_path: Path = DATA_FILE_PATH,
) -> None:
    """
    Export expenses to a CSV file.

    Args:
        output (Path): The path to the output CSV file.
        month (int | None): The month to filter by, or None to list all months.
        year (int | None): The year to filter by, or None to list all years.
        category (str | None): The category to filter by, or None to list all categories.
    """
    try:
        db_manager = DatabaseManager(data_file_path)
        expenses = db_manager.load_expenses()
        result = expenses

        if year:
            result = filter_by_year(result, year)
        if month:
            result = filter_by_month(result, month)
        if category:
            result = filter_by_category(result, category)

        export_to_csv(result, output)
        print(f"Exported expenses to {output}")
    except FileNotFoundError as error:
        print(f"Error: {error}")


def show_summary(
    month: int | None = None,
    year: int | None = None,
    category: str | None = None,
    data_file_path: Path = DATA_FILE_PATH,
) -> None:
    """
    Show the summary amount of expenses.

    Args:
        month (int | None): The month to filter by, or None to list all months.
        year (int | None): The year to filter by, or None to list all years.
        category (str | None): The category to filter by, or None to list all categories.
    """
    try:
        db_manager = DatabaseManager(data_file_path)
        expenses = db_manager.load_expenses()
        result = expenses

        if year:
            result = filter_by_year(result, year)
        if month:
            result = filter_by_month(result, month)
        if category:
            result = filter_by_category(result, category)

        total = calculate_total(result)
        print(f"Total expenses: ${total:.2f}")
    except FileNotFoundError:
        print("File missing.")
    except KeyError as error:
        print(f"Error: {error}")
    except json.JSONDecodeError as error:
        print(f"Error: {error}")
    except (ValueError, TypeError) as error:
        print(f"Error: Invalid data {error}")


def valid_month(value: str) -> int:
    """
    Validate and return a valid month as an integer (1-12).

    Args:
        value (str): The month value to validate.

    Returns:
        int: The validated month as an integer.

    Raises:
        argparse.ArgumentTypeError: If the value is not a valid month.
    """
    try:
        month = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid month: {value}. Must be a number")

    if month < 1 or month > 12:
        raise argparse.ArgumentTypeError(
            f"Invalid month: {value}. Must be between 1 and 12."
        )

    return month


def main():
    """Expense Tracker CLI"""
    # 1. Create parser
    parser = argparse.ArgumentParser(description="Expense Tracker CLI")
    # 2. Add subcommands (list,delete,etc.)
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    # 3. Add "list" command
    list_parser = subparsers.add_parser("list", help="List all expenses")
    list_parser.add_argument("-y", "--year", type=int, help="Filter by year")
    list_parser.add_argument("-m", "--month", type=valid_month, help="Filter by month")
    list_parser.add_argument("-c", "--category", type=str, help="Filter by category")
    list_parser.add_argument(
        "--data-file",
        type=Path,
        default=DATA_FILE_PATH,
        help="Path to expenses JSON file",
    )

    # 4. Add "add" command
    add_parser = subparsers.add_parser("add", help="Add a new expense")
    add_parser.add_argument("description", type=str, help="Expense description")
    add_parser.add_argument("amount", type=float, help="Expense amount")
    add_parser.add_argument("date", type=str, help="Expense date (YYYY-MM-DD)")
    add_parser.add_argument("-c", "--category", type=str, help="Expense category")
    add_parser.add_argument(
        "--data-file",
        type=Path,
        default=DATA_FILE_PATH,
        help="Path to expenses JSON file",
    )

    # 5. Add "delete" command
    delete_parser = subparsers.add_parser("delete", help="Delete an expense")
    delete_parser.add_argument("expense_id", type=int, help="Expense ID to delete")
    delete_parser.add_argument(
        "--data-file",
        type=Path,
        default=DATA_FILE_PATH,
        help="Path to expenses JSON file",
    )

    # 6. Add "summary" command
    summary_parser = subparsers.add_parser("summary", help="Show summary expenses")
    summary_parser.add_argument("-y", "--year", type=int, help="Filter by year")
    summary_parser.add_argument(
        "-m", "--month", type=valid_month, help="Filter by month"
    )
    summary_parser.add_argument("-c", "--category", type=str, help="Filter by category")
    summary_parser.add_argument(
        "--data-file",
        type=Path,
        default=DATA_FILE_PATH,
        help="Path to expenses JSON file",
    )

    # 7. Add "export" command
    export_parser = subparsers.add_parser("export", help="Export expenses to CSV")
    export_parser.add_argument(
        "-o", "--output", type=Path, required=True, help="Output CSV file path"
    )
    export_parser.add_argument("-y", "--year", type=int, help="Filter by year")
    export_parser.add_argument("-m", "--month", type=int, help="Filter by month")
    export_parser.add_argument(
        "-c",
        "--category",
        type=str,
        help="Filter by category",
    )
    export_parser.add_argument(
        "--data-file",
        type=Path,
        default=DATA_FILE_PATH,
        help="Path to expenses JSON file",
    )

    # 8. Parse arguments
    args = parser.parse_args()
    # 9. Call the right function
    if args.command == "list":
        list_expenses(
            month=args.month,
            year=args.year,
            category=args.category,
            data_file_path=args.data_file,
        )
    elif args.command == "add":
        add_expense_cli(
            args.description,
            args.amount,
            args.date,
            args.category,
            data_file_path=args.data_file,
        )
    elif args.command == "delete":
        delete_expense_cli(
            args.expense_id,
            data_file_path=args.data_file,
        )
    elif args.command == "summary":
        show_summary(
            args.month,
            args.year,
            args.category,
            data_file_path=args.data_file,
        )
    elif args.command == "export":
        export_expenses_cli(
            output=args.output,
            month=args.month,
            year=args.year,
            category=args.category,
            data_file_path=args.data_file,
        )
    elif args.command is None:
        parser.print_help()


if __name__ == "__main__":
    """Entry point for the Expense Tracker CLI."""
    main()
