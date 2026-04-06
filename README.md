# Expense Tracker CLI

A command-line expense tracker application built with Python using TDD (Test-Driven Development).

## Features

- ✅ Add, delete, and list expenses
- ✅ Filter expenses by month, year, and **category**
- ✅ View summary totals (with optional filtering)
- ✅ **Export to CSV** (with filtering support, comma-safe)
- ✅ **Budget checking** (with filtering support, positive amount validation)
- ✅ **Recurring expenses** (automatic generation, monthly/yearly support)
- ✅ **Custom data file path** (`--data-file`)
- ✅ **User-writable default location** (`~/.expense-tracker/expenses.json`)
- ✅ **Month validation** (1-12 range)
- ✅ **Year validation** (numeric only)
- ✅ **Budget amount validation** (must be positive)
- ✅ Date validation (YYYY-MM-DD format)
- ✅ Amount validation (must be positive)
- ✅ Description validation (cannot be empty)
- ✅ **Optional categories** (free-text)
- ✅ JSON file storage (UTF-8, pretty-printed)
- ✅ **Consistent error exit codes** (for scripting/automation)
- ✅ **70 automated tests** (CLI, business logic, storage)

## Installation

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)

### Setup

1. **Navigate to the project:**
   ```bash
   cd /path/to/expense-tracker-cli
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment:**
   ```bash
   # On Linux/Mac:
   source .venv/bin/activate
   
   # On Windows:
   .venv\Scripts\activate
   ```

4. **Install dependencies (for testing only):**
   ```bash
   # The app itself has no dependencies!
   # But tests require pytest:
   pip install pytest
   ```

### Dependencies

| Package | Purpose | Required? |
|---------|---------|-----------|
| (none) | Running the app | ✅ Built-in |
| pytest | Running tests | ❌ Optional (dev only) |

## Usage

### Show Help
```bash
python -m expense_tracker.cli --help
python -m expense_tracker.cli list --help
```

### List All Expenses
```bash
python -m expense_tracker.cli list
```

### List Expenses by Month
```bash
python -m expense_tracker.cli list -m 2
python -m expense_tracker.cli list --month 2
```

### List Expenses by Year
```bash
python -m expense_tracker.cli list -y 2026
python -m expense_tracker.cli list --year 2026
```

### List Expenses by Month and Year
```bash
python -m expense_tracker.cli list -y 2026 -m 2
```

### Add a New Expense
```bash
python -m expense_tracker.cli add "Lunch" 20.00 2026-04-01
python -m expense_tracker.cli add "Lunch" 20.00 2026-04-01 --category "Food"
```

### Delete an Expense by ID
```bash
python -m expense_tracker.cli delete 1
```

### View Summary (Total Expenses)
```bash
python -m expense_tracker.cli summary
```

### View Summary with Filtering
```bash
python -m expense_tracker.cli summary -m 2
python -m expense_tracker.cli summary -y 2026
python -m expense_tracker.cli summary -y 2026 -m 2
python -m expense_tracker.cli summary --category "Food"
```

### Use Custom Data File
```bash
python -m expense_tracker.cli list --data-file /path/to/expenses.json
python -m expense_tracker.cli add "Lunch" 20 2026-04-01 --data-file ./my-data.json
```

### Export Expenses to CSV
```bash
# Export all expenses
python -m expense_tracker.cli export --output expenses.csv

# Export with filters
python -m expense_tracker.cli export --output april-food.csv --month 4 --category "Food"
python -m expense_tracker.cli export --output 2026-expenses.csv --year 2026
```

### Check Budget Status
```bash
# Check if expenses exceed budget
python -m expense_tracker.cli budget --amount 500

# Check budget for specific month
python -m expense_tracker.cli budget --amount 200 --month 4

# Check budget for specific category
python -m expense_tracker.cli budget --amount 100 --category "Food"

# Check budget for specific year and month
python -m expense_tracker.cli budget --amount 1000 --year 2026 --month 4
```

**Note:** Budget amount must be a positive number. Negative or zero values are rejected.

### Manage Recurring Expenses
```bash
# Add a recurring expense (Rent)
python -m expense_tracker.cli recurring add "Rent" 1000 --frequency monthly --start-date 2026-01-01

# List all recurring templates
python -m expense_tracker.cli recurring list

# Generate expenses that are due today
python -m expense_tracker.cli recurring generate

# Delete a recurring template (ID 1)
python -m expense_tracker.cli recurring delete 1
```

## Running Tests

```bash
# Activate virtual environment first
source .venv/bin/activate

# Run all tests
python -m pytest tests/ -v

# Run specific test files
python -m pytest tests/test_expenses.py -v
python -m pytest tests/test_storage.py -v
```

## Scripting & Automation

All CLI commands return proper exit codes:
- **Exit 0**: Success
- **Exit 1**: Error (invalid input, missing file, validation failure)

This makes the CLI safe for use in scripts and CI/CD pipelines:
```bash
# Example: Check budget in a script
python -m expense_tracker.cli budget --amount 500
if [ $? -ne 0 ]; then
    echo "Budget check failed!"
    exit 1
fi
```

## Data Storage

Expenses are stored in a JSON file located at:
```
~/.expense-tracker/expenses.json
```

### Default Location
By default, expenses are stored in a user-writable directory (`~/.expense-tracker/`).
The directory is created automatically on first use.

### Custom Data File
You can override the default location with `--data-file`:
```bash
python -m expense_tracker.cli list --data-file /path/to/custom.json
python -m expense_tracker.cli add "Lunch" 20 2026-04-01 --data-file ./my-data.json
```

### Data Format
```json
[
    {
        "id": 1,
        "description": "Lunch",
        "amount": 20.00,
        "date": "2026-04-01",
        "category": "Food"
    }
]
```

## Project Structure

```
expense-tracker-cli/
├── src/
│   └── expense_tracker/
│       ├── __init__.py
│       ├── cli.py           # CLI layer (user interface)
│       ├── expenses.py      # Business logic layer
│       └── storage.py       # Data access layer
├── tests/
│   ├── conftest.py          # Pytest configuration
│   ├── test_cli.py          # CLI layer tests
│   ├── test_expenses.py     # Business logic tests
│   └── test_storage.py      # Storage layer tests
├── .gitignore
├── LICENSE.md
├── README.md
├── requirements.txt
└── setup.py

Default data file: ~/.expense-tracker/expenses.json (created automatically)
```

## Architecture

This project follows a **3-layer architecture**:

1. **Presentation Layer (CLI)** - `cli.py`
   - Handles user input/output
   - Parses command-line arguments (with validation)
   - Displays results

2. **Business Logic Layer** - `expenses.py`
   - Validates data
   - Performs calculations
   - Implements core rules (filtering, adding, deleting)

3. **Data Access Layer** - `storage.py`
   - Reads/writes to JSON file
   - Handles file operations

## Testing

All features are developed using **Test-Driven Development (TDD)**:

```bash
# Run all tests
python -m pytest tests/ -v

# Run CLI tests only
python -m pytest tests/test_cli.py -v

# Run with coverage
python -m pytest tests/ --cov=expense_tracker
```

The test suite covers:
- CLI argument parsing and routing
- Input validation (month range, date format, amount)
- Business logic (filtering, adding, deleting)
- Storage operations (load, save, error handling)
- Edge cases (empty data, corrupted files, missing keys)

## License

MIT License
