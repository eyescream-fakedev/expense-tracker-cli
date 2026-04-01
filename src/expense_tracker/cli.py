import argparse
from pathlib import Path

from expense_tracker.expenses import add_expense, calculate_total, delete_expense
from expense_tracker.storage import DatabaseManager

SCRIPT_DIR = Path(__file__).parent
DATA_FILE_PATH = SCRIPT_DIR / "expenses.json"


def list_expenses() -> None:
    """List all expenses."""
    db_manager = DatabaseManager(DATA_FILE_PATH)
    expenses = db_manager.load_expenses()
    if not expenses:
        print("No expense found")
        return
    print(f"{'ID':<5} {'Date':<12} {'Description':<25} {'Amount':>10}")
    print("-" * 55)  # Separator line
    # Expenses
    for expense in expenses:
        print(
            f"{expense['id']:<5} "
            f"{expense['date']:<12} "
            f"{expense['description']:<25} "
            f"${float(expense['amount']):>8.2f}"
        )


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


def show_summary() -> None:
    """Show the summary amount of expenses."""
    db_manager = DatabaseManager(DATA_FILE_PATH)
    expenses = db_manager.load_expenses()
    total = calculate_total(expenses)
    print(f"Total expenses: {total}")


def main():
    """Expense Tracker CLI"""
    # 1. Create parser
    parser = argparse.ArgumentParser(description="Expense Tracker CLI")
    # 2. Add subcommands (list,delete,etc.)
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    # 3. Add "list" command
    subparsers.add_parser("list", help="List all expenses")

    # 4. Add "add" command
    add_parser = subparsers.add_parser("add", help="Add a new expense")
    add_parser.add_argument("description", type=str, help="Expense description")
    add_parser.add_argument("amount", type=float, help="Expense amount")
    add_parser.add_argument("date", type=str, help="Expense date (YYYY-MM-DD)")

    # 5. Add "delete" command
    delete_parser = subparsers.add_parser("delete", help="Delete an expense")
    delete_parser.add_argument("expense_id", type=int, help="Expense ID to delete")

    # 6. Add "summary" command
    subparsers.add_parser("summary", help="Show summary expenses")

    # 7. Parse arguments
    args = parser.parse_args()
    # 8. Call the right function
    if args.command == "list":
        list_expenses()
    elif args.command == "add":
        add_expense_cli(args.description, args.amount, args.date)
    elif args.command == "delete":
        delete_expense_cli(args.expense_id)
    elif args.command == "summary":
        show_summary()
    elif args.command is None:
        parser.print_help()


if __name__ == "__main__":
    """Entry point for the Expense Tracker CLI."""
    main()
