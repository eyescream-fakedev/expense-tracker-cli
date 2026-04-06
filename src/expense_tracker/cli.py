import argparse
import json
import sys
from datetime import date
from pathlib import Path

from expense_tracker.expenses import (
    add_expense,
    add_recurring_expense,
    calculate_total,
    check_budget_exceeded,
    delete_expense,
    delete_recurring_expense,
    export_to_csv,
    filter_by_category,
    filter_by_month,
    filter_by_year,
    generate_due_expenses,
)
from expense_tracker.storage import DatabaseManager

DATA_DIR = Path.home() / ".expense-tracker"
DATA_FILE_PATH = DATA_DIR / "expenses.json"


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
            f"{'ID':<5} "
            f"{'Date':<12} "
            f"{'Description':<25} "
            f"{'Category':<15} {'Amount':>10}"
        )
        print("-" * 75)
        for expense in result:
            category = expense.get("category", "")
            print(
                f"{expense['id']:<5} "
                f"{expense['date']:<12} "
                f"{expense['description']:<25} "
                f"{category:<15} "
                f"${expense['amount']:>8.2f}"
            )
    except ValueError as error:
        print(f"Error: {error}")
        sys.exit(1)
    except KeyError as error:
        print(f"Error: {error}")
        sys.exit(1)
    except FileNotFoundError as error:
        print(f"Error: {error}")
        sys.exit(1)


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
        sys.exit(1)
    except KeyError as error:
        print(f"Error: {error}")
        sys.exit(1)
    except FileNotFoundError as error:
        print(f"Error: {error}")
        sys.exit(1)


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
        sys.exit(1)
    except KeyError as error:
        print(f"Error: {error}")
        sys.exit(1)
    except FileNotFoundError as error:
        print(f"Error: {error}")
        sys.exit(1)


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
        sys.exit(1)


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
        print("Error: File missing.")
        sys.exit(1)
    except KeyError as error:
        print(f"Error: {error}")
        sys.exit(1)
    except json.JSONDecodeError as error:
        print(f"Error: {error}")
        sys.exit(1)
    except (ValueError, TypeError) as error:
        print(f"Error: Invalid data {error}")
        sys.exit(1)


def budget_check_cli(
    budget_amount: float,
    month: int | None = None,
    year: int | None = None,
    category: str | None = None,
    data_file_path: Path = DATA_FILE_PATH,
) -> None:
    """
    Checks if the budget is exceeded based on the given criteria.

    Args:
        budget_amount (float): The budget amount to compare against.
        month (int | None): The month to filter expenses by.
        year (int | None): The year to filter expenses by.
        category (str | None): The category to filter expenses by.
        data_file_path (Path): The path to the data file.
    """
    try:
        db_manager = DatabaseManager(data_file_path)
        expenses = db_manager.load_expenses()
        result = expenses

        if month:
            result = filter_by_month(result, month)
        if year:
            result = filter_by_year(result, year)
        if category:
            result = filter_by_category(result, category)

        total_expenses = calculate_total(result)
        if check_budget_exceeded(result, budget_amount):
            print(
                f"Budget exceeded: spent ${total_expenses:.2f} of "
                f"${budget_amount:.2f} budget"
            )
        else:
            print(
                f"Budget OK: ${total_expenses:.2f} spent of ${budget_amount:.2f} budget"
            )

    except FileNotFoundError:
        print("Error: File missing.")
        sys.exit(1)
    except KeyError as error:
        print(f"Error: {error}")
        sys.exit(1)
    except json.JSONDecodeError as error:
        print(f"Error: {error}")
        sys.exit(1)
    except (ValueError, TypeError) as error:
        print(f"Error: Invalid data {error}")
        sys.exit(1)


def add_recurring_expense_cli(
    description: str,
    amount: float,
    frequency: str,
    start_date: str | None,
    category: str | None,
    data_file_path: Path,
) -> None:
    """
    Add a recurring expense to the database.

    Args:
        description (str): The description of the recurring expense.
        amount (float): The amount of the recurring expense.
        frequency (str): The frequency of the recurring expense (e.g., "monthly").
        start_date (str | None): The start date of the recurring expense (YYYY-MM-DD).
        category (str | None): The category of the recurring expense.
        data_file_path (Path): The path to the data file.
    """
    try:
        actual_start_date = start_date or date.today().strftime("%Y-%m-%d")
        db_manager = DatabaseManager(data_file_path)
        expenses = db_manager.load_expenses()
        expense = {
            "description": description,
            "amount": amount,
            "frequency": frequency,
            "start_date": actual_start_date,
            "category": category,
        }
        updated_recurring = add_recurring_expense(expenses, expense)
        print("Recurring expense added successfully.")
        db_manager.save_expenses(updated_recurring)
    except (ValueError, TypeError) as error:
        print(f"Error: Invalid data {error}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"Error: Data file not found at {data_file_path}")
        sys.exit(1)


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


def valid_year(value: str) -> int:
    """
    Validate and return a valid year as an integer.

    Args:
        value (str): The year value to validate.

    Returns:
        int: The validated year as an integer.
    """
    try:
        year = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid year: {value}. Must be a number")
    return year


def valid_positive_amount(value: str) -> float:
    """
    Validate and return a positive amount as a float.

    Args:
        value (str): The amount value to validate.

    Returns:
        float: The validated positive amount as a float.
    """
    try:
        amount = float(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid amount: {value}. Must be a number.")

    if amount <= 0:
        raise argparse.ArgumentTypeError(
            f"Invalid budget amount: {value}. Must be greater than 0."
        )
    return amount


def main():
    """Expense Tracker CLI"""
    DATA_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)

    # 1. Create parser
    parser = argparse.ArgumentParser(description="Expense Tracker CLI")
    # 2. Add subcommands (list,delete,etc.)
    subparsers = parser.add_subparsers(
        dest="command",
        help="Available commands",
    )
    # 3. Add "list" command
    list_parser = subparsers.add_parser(
        "list",
        help="List all expenses",
    )
    list_parser.add_argument(
        "-y",
        "--year",
        type=valid_year,
        help="Filter by year",
    )
    list_parser.add_argument(
        "-m",
        "--month",
        type=valid_month,
        help="Filter by month",
    )
    list_parser.add_argument(
        "-c",
        "--category",
        type=str,
        help="Filter by category",
    )
    list_parser.add_argument(
        "--data-file",
        type=Path,
        default=DATA_FILE_PATH,
        help="Path to expenses JSON file",
    )

    # 4. Add "add" command
    add_parser = subparsers.add_parser(
        "add",
        help="Add a new expense",
    )
    add_parser.add_argument(
        "description",
        type=str,
        help="Expense description",
    )
    add_parser.add_argument(
        "amount",
        type=float,
        help="Expense amount",
    )
    add_parser.add_argument(
        "date",
        type=str,
        help="Expense date (YYYY-MM-DD)",
    )
    add_parser.add_argument(
        "-c",
        "--category",
        type=str,
        help="Expense category",
    )
    add_parser.add_argument(
        "--data-file",
        type=Path,
        default=DATA_FILE_PATH,
        help="Path to expenses JSON file",
    )

    # 5. Add "delete" command
    delete_parser = subparsers.add_parser(
        "delete",
        help="Delete an expense",
    )
    delete_parser.add_argument(
        "expense_id",
        type=int,
        help="Expense ID to delete",
    )
    delete_parser.add_argument(
        "--data-file",
        type=Path,
        default=DATA_FILE_PATH,
        help="Path to expenses JSON file",
    )

    # 6. Add "summary" command
    summary_parser = subparsers.add_parser(
        "summary",
        help="Show summary expenses",
    )
    summary_parser.add_argument(
        "-y",
        "--year",
        type=valid_year,
        help="Filter by year",
    )
    summary_parser.add_argument(
        "-m",
        "--month",
        type=valid_month,
        help="Filter by month",
    )
    summary_parser.add_argument(
        "-c",
        "--category",
        type=str,
        help="Filter by category",
    )
    summary_parser.add_argument(
        "--data-file",
        type=Path,
        default=DATA_FILE_PATH,
        help="Path to expenses JSON file",
    )

    # 7. Add "export" command
    export_parser = subparsers.add_parser(
        "export",
        help="Export expenses to CSV",
    )
    export_parser.add_argument(
        "-o",
        "--output",
        type=Path,
        required=True,
        help="Output CSV file path",
    )
    export_parser.add_argument(
        "-y",
        "--year",
        type=valid_year,
        help="Filter by year",
    )
    export_parser.add_argument(
        "-m",
        "--month",
        type=valid_month,
        help="Filter by month",
    )
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

    # 8. Add "budget" command
    budget_parser = subparsers.add_parser(
        "budget",
        help="Check budget against expenses",
    )
    budget_parser.add_argument(
        "--amount",
        type=valid_positive_amount,
        required=True,
        help="Budget amount",
    )
    budget_parser.add_argument(
        "--month",
        type=valid_month,
        help="Filter by month",
    )
    budget_parser.add_argument(
        "--year",
        type=valid_year,
        help="Filter by year",
    )
    budget_parser.add_argument(
        "--category",
        type=str,
        help="Filter by category",
    )
    budget_parser.add_argument(
        "--data-file",
        type=Path,
        default=DATA_FILE_PATH,
        help="Path to expenses JSON file",
    )

    # 9.Add "recurring" command
    recurring_parser = subparsers.add_parser(
        "recurring",
        help="Manage recurring expenses",
    )
    # - Create sub-parsers for "recurring"
    recurring_subparsers = recurring_parser.add_subparsers(
        dest="recurring_command",
    )
    add_parser = recurring_subparsers.add_parser(
        "add",
        help="Add a recurring expense",
    )
    add_parser.add_argument(
        "description",
        type=str,
        help="Recurring expense description",
    )
    add_parser.add_argument("amount", type=float)
    add_parser.add_argument("--frequency", type=str, default="monthly")
    add_parser.add_argument("--start-date", type=str, default=None)
    add_parser.add_argument("--category", type=str, default="")
    add_parser.add_argument("--data-file", type=Path, default=DATA_FILE_PATH)

    # Add 'generate' parser
    generate_parser = recurring_subparsers.add_parser(
        "generate",
        help="Generate recurring expenses",
    )

    # Add "list" parser
    list_parser = recurring_subparsers.add_parser(
        "list",
        help="List recurring expenses",
    )

    # Add "delete" parser
    delete_parser = recurring_subparsers.add_parser(
        "delete",
        help="Delete a recurring expense",
    )
    delete_parser.add_argument(
        "id", type=int, help="ID of the recurring expense to delete"
    )

    # 10. Parse arguments
    args = parser.parse_args()
    # 11. Call the right function
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
    elif args.command == "budget":
        budget_check_cli(
            budget_amount=args.amount,
            month=args.month,
            year=args.year,
            category=args.category,
            data_file_path=args.data_file,
        )
    elif args.command == "recurring":
        if args.recurring_command == "add":
            add_recurring_expense_cli(
                description=args.description,
                amount=args.amount,
                frequency=args.frequency,
                start_date=args.start_date,
                category=args.category,
                data_file_path=args.data_file,
            )
        if args.recurring_command == "generate":
            # 1. Define paths (reuse DATA_FILE_PATH for expenses, create one for recurring)
            recurring_path = DATA_FILE_PATH.parent / "recurring.json"

            # 2. Load Data
            recurring_manager = DatabaseManager(recurring_path)
            recurring = recurring_manager.load_expenses()

            expense_manager = DatabaseManager(DATA_FILE_PATH)
            expenses = expense_manager.load_expenses()

            # 3. Generate
            generated, updated_recurring = generate_due_expenses(recurring, expenses)

            # 4. Save Results
            recurring_manager.save_expenses(updated_recurring)

            if generated:
                print(f"Generated {len(generated)} expense(s).")
                expense_manager.save_expenses(expenses + generated)
            else:
                print("No expenses due today.")
        elif args.recurring_command == "list":
            recurring_manager = DatabaseManager(
                DATA_FILE_PATH.parent / "recurring.json"
            )
            recurring = recurring_manager.load_expenses()
            if not recurring:
                print("No recurring expenses found.")
            else:
                print(
                    f"{'ID':<5} "
                    f"{'Description':<25} "
                    f"{'Amount':>10} "
                    f"{'Frequency':<10} "
                    f"{'Next Due':<12}"
                )
                print("-" * 65)
                for r in recurring:
                    print(
                        f"{r['id']:<5} "
                        f"{r['description']:<25} "
                        f"{r['amount']:>8.2f} "
                        f"{r['frequency']:<10} "
                        f"{r['next_due_date']:<12}"
                    )
        elif args.recurring_command == "delete":
            recurring_manager = DatabaseManager(
                DATA_FILE_PATH.parent / "recurring.json"
            )
            recurring = recurring_manager.load_expenses()

            # Call business logic to delete the template
            updated_recurring = delete_recurring_expense(recurring, args.id)
            recurring_manager.save_expenses(updated_recurring)
            print(f"Deleted recurring expense with ID {args.id}")

    elif args.command is None:
        parser.print_help()


if __name__ == "__main__":
    """Entry point for the Expense Tracker CLI."""
    main()
