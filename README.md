# Expense Tracker CLI

A command-line expense tracker application built with Python using TDD (Test-Driven Development).

## Features

- ✅ Add, delete, and list expenses
- ✅ Filter expenses by month, year, and **category**
- ✅ View summary totals (with optional filtering)
- ✅ **Custom data file path** (`--data-file`)
- ✅ **Month validation** (1-12 range)
- ✅ Date validation (YYYY-MM-DD format)
- ✅ Amount validation (must be positive)
- ✅ Description validation (cannot be empty)
- ✅ **Optional categories** (free-text)
- ✅ JSON file storage
- ✅ **38 automated tests** (CLI, business logic, storage)

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

## Data Storage

Expenses are stored in a JSON file located at:
```
src/expense_tracker/expenses.json
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
│       ├── storage.py       # Data access layer
│       └── expenses.json    # Data file
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
