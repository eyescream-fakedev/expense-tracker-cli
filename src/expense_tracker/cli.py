import argparse
from pathlib import Path

from expense_tracker.expenses import (
    add_expense,
    calculate_total,
    delete_expense,
    filter_by_month,
    filter_by_year,
)
from expense_tracker.storage import DatabaseManager

SCRIPT_DIR = Path(__file__).parent
DATA_FILE_PATH = SCRIPT_DIR / "expenses.json"


def list_expenses(month: int | None = None, year: int | None = None) -> None:
    """
    List all expenses for a given month and year.

    Args:
        month (int | None): The month to filter by, or None to list all months.
        year (int | None): The year to filter by, or None to list all years.
    """
    # if month and/or year is provided, filter expenses accordingly
    try:
        db_manager = DatabaseManager(DATA_FILE_PATH)
        expenses = db_manager.load_expenses()

        if year and month:
            filtered_expenses = filter_by_year(expenses, year)
            filtered_expenses = filter_by_month(filtered_expenses, month=month)
        elif month:
            filtered_expenses = filter_by_month(expenses, month=month)
        elif year:
            filtered_expenses = filter_by_year(expenses, year)
        else:
            filtered_expenses = expenses
        # print title with fixed-width column formatting
        print(f"{'ID':<5} {'Date':<12} {'Description':<25} {'Amount':>10}")
        print("-" * 45)
        for expense in filtered_expenses:
            print(
                f"{expense['id']:<5} {expense['date']:<12} {expense['description']:<25} ${expense['amount']:>8.2f}"
            )
    except ValueError as error:
        print(f"Error: {error}")
    except KeyError as error:
        print(f"Error: {error}")


def add_expense_cli(description: str, amount: float, date: str) -> None:
    """
    Add a new expense via CLI.

    Args:
        description (str): The expense description.
        amount (float): The expense amount.
        date (str): The expense date in YYYY-MM-DD format.

    """
    try:
        # Load existing expenses
        db_manager = DatabaseManager(DATA_FILE_PATH)
        expenses = db_manager.load_expenses()

        # Create new expense
        new_expense = {
            "description": description,
            "amount": amount,
            "date": date,
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


def delete_expense_cli(expense_id: int) -> None:
    """
    Delete an expense by its ID.

    Args:
        expense_id (int): The ID of the expense to delete.
    """
    try:
        db_manager = DatabaseManager(DATA_FILE_PATH)
        expenses = db_manager.load_expenses()
        updated_expenses = delete_expense(expenses, expense_id)
        db_manager.save_expenses(updated_expenses)
        print(f"Deleted expense with ID {expense_id}")
    except ValueError as error:
        print(f"Error: {error}")
    except KeyError as error:
        print(f"Error: {error}")


def show_summary(month: int | None = None, year: int | None = None) -> None:
    """
    Show the summary amount of expenses.

    Args:
        month (int | None): The month to filter by, or None to list all months.
        year (int | None): The year to filter by, or None to list all years.
    """
    try:
        db_manager = DatabaseManager(DATA_FILE_PATH)
        expenses = db_manager.load_expenses()
        if month and year:
            expenses = filter_by_year(expenses, year)
            expenses = filter_by_month(expenses, month)
        elif month:
            expenses = filter_by_month(expenses, month)
        elif year:
            expenses = filter_by_year(expenses, year)
        total = calculate_total(expenses)
        print(f"Total expenses: ${total:.2f}")
    except FileNotFoundError:
        print("No expenses found.")
    except KeyError as error:
        print(f"Error: {error}")
    except Exception as error:
        print(f"Error: {error}")


def main():
    """Expense Tracker CLI"""
    # 1. Create parser
    parser = argparse.ArgumentParser(description="Expense Tracker CLI")
    # 2. Add subcommands (list,delete,etc.)
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    # 3. Add "list" command
    list_parser = subparsers.add_parser("list", help="List all expenses")
    list_parser.add_argument("-y", "--year", type=int, help="Filter by year")
    list_parser.add_argument("-m", "--month", type=int, help="Filter by month")

    # 4. Add "add" command
    add_parser = subparsers.add_parser("add", help="Add a new expense")
    add_parser.add_argument("description", type=str, help="Expense description")
    add_parser.add_argument("amount", type=float, help="Expense amount")
    add_parser.add_argument("date", type=str, help="Expense date (YYYY-MM-DD)")

    # 5. Add "delete" command
    delete_parser = subparsers.add_parser("delete", help="Delete an expense")
    delete_parser.add_argument("expense_id", type=int, help="Expense ID to delete")

    # 6. Add "summary" command
    summary_parser = subparsers.add_parser("summary", help="Show summary expenses")
    summary_parser.add_argument("-y", "--year", type=int, help="Filter by year")
    summary_parser.add_argument("-m", "--month", type=int, help="Filter by month")

    # 7. Parse arguments
    args = parser.parse_args()
    # 8. Call the right function
    if args.command == "list":
        list_expenses(month=args.month, year=args.year)
    elif args.command == "add":
        add_expense_cli(args.description, args.amount, args.date)
    elif args.command == "delete":
        delete_expense_cli(args.expense_id)
    elif args.command == "summary":
        show_summary(args.month, args.year)
    elif args.command is None:
        parser.print_help()


if __name__ == "__main__":
    """Entry point for the Expense Tracker CLI."""
    main()
