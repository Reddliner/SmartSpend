
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
BUDGET_FILE = DATA_DIR / "budgets.csv"

COLUMNS = ["year", "month", "amount"]


def initialize_budgets():
    """Create budget storage if it does not exist."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if not BUDGET_FILE.exists():
        pd.DataFrame(columns=COLUMNS).to_csv(
            BUDGET_FILE, index=False
        )


def load_budgets():
    """Load saved monthly budgets."""
    initialize_budgets()

    df = pd.read_csv(BUDGET_FILE)

    if df.empty:
        return pd.DataFrame(columns=COLUMNS)

    df = df[COLUMNS].copy()
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    df["month"] = pd.to_numeric(df["month"], errors="coerce")
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

    df = df.dropna(subset=COLUMNS)
    df = df[
        df["year"].between(1900, 2200)
        & df["month"].between(1, 12)
        & (df["amount"] > 0)
    ]

    df["year"] = df["year"].astype(int)
    df["month"] = df["month"].astype(int)

    # If a file contains duplicate month entries, use the last one.
    return (
        df.drop_duplicates(["year", "month"], keep="last")
        .reset_index(drop=True)
    )


def save_budget(year, month, amount):
    """Save or update a budget for a particular month."""
    year = int(year)
    month = int(month)
    amount = float(amount)

    if not 1900 <= year <= 2200:
        raise ValueError("Please enter a valid year.")

    if not 1 <= month <= 12:
        raise ValueError("Month must be between 1 and 12.")

    if not pd.notna(amount) or amount <= 0:
        raise ValueError("Budget must be greater than zero.")

    budgets = load_budgets()

    budgets = budgets[
        ~(
            (budgets["year"] == year)
            & (budgets["month"] == month)
        )
    ]

    budgets = pd.concat(
        [
            budgets,
            pd.DataFrame(
                [{"year": year, "month": month, "amount": amount}]
            ),
        ],
        ignore_index=True,
    )

    budgets.sort_values(["year", "month"]).to_csv(
        BUDGET_FILE, index=False
    )


def get_budget(year, month):
    """Return the saved budget, or None if it is not set."""
    budgets = load_budgets()

    match = budgets[
        (budgets["year"] == int(year))
        & (budgets["month"] == int(month))
    ]

    if match.empty:
        return None

    return float(match.iloc[-1]["amount"])
