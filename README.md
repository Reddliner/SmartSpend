# SmartSpend — Personal Finance Analysis Dashboard

## 1. Project Overview

SmartSpend is a personal finance analysis dashboard developed using Python. It helps users record, manage, analyze, and visualize their expenses so they can better understand their spending habits and manage monthly budgets.

The application provides an interactive dashboard, transaction management, budget tracking, financial insights, and CSV import/export functionality.

## 2. Problem Statement

Managing personal finances can be difficult when expenses are recorded manually without proper categorization or analysis. Users may struggle to identify their largest spending categories, track monthly expenditure, and stay within budget.

SmartSpend addresses this problem by providing a simple, interactive application that organizes expense records and converts them into useful summaries, charts, and budget insights.

## 3. Project Objectives

- Record and manage daily expenses.
- Categorize transactions for easier analysis.
- Calculate total and average expenditure.
- Visualize spending by category and over time.
- Create and monitor monthly budgets.
- Generate financial insights from transaction data.
- Import and export expense records using CSV files.
- Provide a user-friendly interface accessible through a web browser.

## 4. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| Streamlit | Interactive web interface |
| Pandas | Data processing and analysis |
| Matplotlib | Charts and visualizations |
| CSV | Local data storage and data exchange |
| Unittest | Automated testing |

## 5. Main Features

### Dashboard
- Displays total expenses, transaction count, average expense, and top spending category.
- Shows category-based charts and spending trends.
- Displays category and monthly summaries.
- Lists recent transactions.

### Transaction Management
- Add new expense records.
- Edit existing transactions.
- Delete transactions.
- Filter records by category and date.
- Import expense data from CSV files.
- Export transaction records to CSV.
- Validate imported and manually entered data.
- Use permanent transaction IDs to identify individual records.

### Budget Management
- Set a budget for a selected month.
- Calculate monthly expenditure and remaining budget.
- Display budget utilization.
- Warn when spending reaches 80% of the budget or exceeds it.

### Financial Insights
- Identify the largest spending category.
- Summarize current-month spending.
- Calculate average spending per active day.
- Compare recent months with available data.
- Highlight budget utilization and spending concentration.

## 6. Project Structure

```text
SmartSpend/
├── app.py
├── analysis.py
├── budget.py
├── budget_manager.py
├── charts.py
├── data_manager.py
├── requirements.txt
├── README.md
├── sample_expenses.csv
├── data/
│   ├── expenses.csv
│   └── budgets.csv
├── pages/
│   ├── 2_Transactions.py
│   ├── 3_Budgets.py
│   └── 4_Insights.py
└── tests/
    └── test_analysis.py
```

The `.venv` directory contains the local Python environment and should not be included when transferring the project to another computer.

## 7. Installation and Setup

### Requirements

- Python 3.10 or later is recommended.
- pip, Python's package installer.
- A modern web browser.

### macOS Setup

Open Terminal and navigate to the project directory:

```bash
cd ~/Projects/SmartSpend
```

Create a virtual environment if one does not already exist:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

### Windows Setup

Open PowerShell and navigate to the project directory. Adjust the path if the project is stored elsewhere.

```powershell
cd "$HOME\Projects\SmartSpend"
```

Create a virtual environment:

```powershell
py -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation because of its execution policy, you can use Command Prompt instead:

```bat
.venv\Scripts\activate.bat
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

If Python is not installed or the `py` command is unavailable, install Python first and ensure it is available from the command line.

## 8. Running the Application

From the project directory, with the virtual environment activated, run:

```bash
python -m streamlit run app.py
```

Streamlit will display a local URL, usually:

```text
http://localhost:8501
```

Open the URL in your browser. Use the sidebar to navigate between Dashboard, Transactions, Budgets, and Insights.

Stop the application with `Ctrl+C` in the terminal.

## 9. Data Storage

SmartSpend stores expense records and monthly budgets in CSV files inside the `data/` directory.

- `data/expenses.csv` stores transaction records.
- `data/budgets.csv` stores monthly budget settings.
- `sample_expenses.csv` provides example data for demonstration or testing.

The application uses file paths relative to the project directory, helping it run on both macOS and Windows.

**Important:** Back up existing CSV files before making schema changes or replacing project data. Keep personal transaction data private.

## 10. Testing

Run the automated analysis tests from the project root:

```bash
python -m unittest discover -s tests -v
```

Manually verify the following application features:

1. Dashboard metrics match the saved expense records.
2. Charts and summaries display correctly.
3. New expenses remain saved after restarting the application.
4. Category and date filters work correctly.
5. Editing a transaction preserves its permanent ID.
6. Deleting a transaction removes the correct record.
7. CSV imports validate the data and skip duplicate transactions.
8. CSV exports produce a usable file.
9. Monthly budgets persist and display the correct warnings.
10. Financial insights update when the underlying data changes.
11. All four application pages load without errors.

## 11. Methodology

The project follows a modular development approach:

1. **Data collection:** Capture transaction dates, categories, descriptions, and amounts.
2. **Data validation:** Check required fields and ensure amounts are valid and positive.
3. **Data storage:** Store transaction and budget information in CSV files.
4. **Data processing:** Use Pandas to aggregate and analyze expenditure.
5. **Visualization:** Generate charts using Matplotlib.
6. **Budget analysis:** Compare monthly expenditure with the selected budget.
7. **Insight generation:** Convert analytical results into understandable financial observations.
8. **Interface development:** Present functionality through a multipage Streamlit application.
9. **Testing:** Use automated unit tests and manual feature checks.

## 12. Limitations and Future Enhancements

Current limitations include local CSV-based storage, single-user usage, and the absence of automatic bank transaction synchronization.

Possible future enhancements include:

- User authentication and multiple user profiles.
- Database-backed storage.
- Recurring expense tracking.
- More advanced financial forecasting.
- Additional reports and downloadable summaries.
- Improved mobile-friendly interface design.

## 13. Conclusion

SmartSpend demonstrates how Python, data analysis, and interactive visualization can be combined to build a practical personal finance application. It helps users organize expenses, understand spending patterns, monitor budgets, and make more informed financial decisions.
