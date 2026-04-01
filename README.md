# Expense Tracker CLI

A command-line expense tracker application built with Python using TDD (Test-Driven Development).

## Features

- ✅ Add, delete, and list expenses
- ✅ Filter expenses by month and year
- ✅ View summary totals (with optional filtering)
- ✅ Date validation (YYYY-MM-DD format)
- ✅ Amount validation (must be positive)
- ✅ Description validation (cannot be empty)
- ✅ JSON file storage

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
        "date": "2026-04-01"
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
│   ├── test_expenses.py     # Business logic tests
│   └── test_storage.py      # Storage layer tests
├── .gitignore
├── README.md
└── expenses.json
```

## Architecture

This project follows a **3-layer architecture**:

1. **Presentation Layer (CLI)** - `cli.py`
   - Handles user input/output
   - Parses command-line arguments
   - Displays results

2. **Business Logic Layer** - `expenses.py`
   - Validates data
   - Performs calculations
   - Implements core rules

3. **Data Access Layer** - `storage.py`
   - Reads/writes to JSON file
   - Handles file operations

## License

MIT License
