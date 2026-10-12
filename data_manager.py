
from pathlib import Path
from uuid import uuid4

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
EXPENSE_FILE = DATA_DIR / "expenses.csv"

COLUMNS = ["id", "date", "category", "description", "amount"]
TRANSACTION_COLUMNS = ["date", "category", "description", "amount"]


def _new_id():
    """Generate a permanent unique transaction identifier."""
    return str(uuid4())


def initialize_storage():
    """Create storage or migrate an existing CSV to include IDs."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if not EXPENSE_FILE.exists():
        pd.DataFrame(columns=COLUMNS).to_csv(
            EXPENSE_FILE, index=False
        )
        return

    df = pd.read_csv(EXPENSE_FILE)

    if df.empty and not set(TRANSACTION_COLUMNS).issubset(df.columns):
        pd.DataFrame(columns=COLUMNS).to_csv(
            EXPENSE_FILE, index=False
        )
        return

    for column in TRANSACTION_COLUMNS:
        if column not in df.columns:
            df[column] = pd.NA

    if "id" not in df.columns:
        df["id"] = pd.NA

    ids = df["id"].astype("string").str.strip()
    missing_ids = ids.isna() | ids.eq("")
    ids.loc[missing_ids] = [
        _new_id() for _ in range(int(missing_ids.sum()))
    ]

    # Repair duplicate IDs while preserving the first occurrence.
    duplicate_ids = ids.duplicated(keep="first")
    ids.loc[duplicate_ids] = [
        _new_id() for _ in range(int(duplicate_ids.sum()))
    ]

    df["id"] = ids
    df[COLUMNS].to_csv(EXPENSE_FILE, index=False)


def validate_expenses(df):
    """Validate transaction fields and normalize their format."""
    missing = set(TRANSACTION_COLUMNS) - set(df.columns)

    if missing:
        raise ValueError(
            "Missing required columns: "
            + ", ".join(sorted(missing))
        )

    df = df[TRANSACTION_COLUMNS].copy()

    df["date"] = pd.to_datetime(
        df["date"], errors="coerce"
    )
    df["category"] = (
        df["category"].astype("string").str.strip()
    )
    df["description"] = (
        df["description"].astype("string").str.strip()
    )
    df["amount"] = pd.to_numeric(
        df["amount"], errors="coerce"
    )

    invalid = (
        df["date"].isna()
        | df["category"].isna()
        | df["category"].eq("")
        | df["description"].isna()
        | df["description"].eq("")
        | df["amount"].isna()
        | (df["amount"] <= 0)
    )

    if invalid.any():
        raise ValueError(
            f"{int(invalid.sum())} row(s) contain invalid "
            "dates, categories, descriptions, or amounts."
        )

    df["date"] = df["date"].dt.strftime("%Y-%m-%d")
    return df.reset_index(drop=True)


def load_expenses():
    """Load valid saved transactions with permanent IDs."""
    initialize_storage()
    df = pd.read_csv(EXPENSE_FILE, dtype={"id": "string"})

    if df.empty:
        return pd.DataFrame(columns=COLUMNS)

    df = df[COLUMNS].copy()

    ids = df["id"].astype("string").str.strip()
    missing_ids = ids.isna() | ids.eq("")

    if missing_ids.any():
        ids.loc[missing_ids] = [
            _new_id() for _ in range(int(missing_ids.sum()))
        ]

    df["id"] = ids
    df["date"] = pd.to_datetime(
        df["date"], errors="coerce"
    )
    df["category"] = (
        df["category"].astype("string").str.strip()
    )
    df["description"] = (
        df["description"].astype("string").str.strip()
    )
    df["amount"] = pd.to_numeric(
        df["amount"], errors="coerce"
    )

    invalid = (
        df["date"].isna()
        | df["category"].isna()
        | df["category"].eq("")
        | df["description"].isna()
        | df["description"].eq("")
        | df["amount"].isna()
        | (df["amount"] <= 0)
    )

    df = df.loc[~invalid].copy()
    df["date"] = df["date"].dt.strftime("%Y-%m-%d")

    return df.reset_index(drop=True)


def add_expense(date, category, description, amount):
    """Validate and save a new transaction."""
    new_expense = validate_expenses(
        pd.DataFrame([{
            "date": date,
            "category": category,
            "description": description,
            "amount": amount,
        }])
    )

    initialize_storage()
    new_expense.insert(0, "id", _new_id())

    new_expense[COLUMNS].to_csv(
        EXPENSE_FILE,
        mode="a",
        header=False,
        index=False,
    )


def update_expense(transaction_id, date, category, description, amount):
    """Update a transaction using its permanent ID."""
    expenses = load_expenses()
    matches = expenses["id"] == str(transaction_id)

    if not matches.any():
        raise ValueError("The selected transaction no longer exists.")

    updated = validate_expenses(
        pd.DataFrame([{
            "date": date,
            "category": category,
            "description": description,
            "amount": amount,
        }])
    ).iloc[0]

    for column in TRANSACTION_COLUMNS:
        expenses.loc[matches, column] = updated[column]

    expenses[COLUMNS].to_csv(EXPENSE_FILE, index=False)


def delete_expense(transaction_id):
    """Delete a transaction using its permanent ID."""
    expenses = load_expenses()
    matches = expenses["id"] == str(transaction_id)

    if not matches.any():
        raise ValueError("The selected transaction no longer exists.")

    expenses.loc[~matches, COLUMNS].to_csv(
        EXPENSE_FILE, index=False
    )


def import_expenses(file):
    """Import validated CSV records, skipping exact duplicates."""
    try:
        uploaded = pd.read_csv(file)
    except Exception as exc:
        raise ValueError("Could not read the CSV file.") from exc

    imported = validate_expenses(uploaded)
    initialize_storage()
    existing = load_expenses()

    existing_keys = set(
        map(
            tuple,
            existing[TRANSACTION_COLUMNS].astype(str).values.tolist(),
        )
    )

    new_rows = []
    duplicates = 0

    for _, row in imported.iterrows():
        key = tuple(str(row[column]) for column in TRANSACTION_COLUMNS)

        if key in existing_keys:
            duplicates += 1
            continue

        existing_keys.add(key)
        new_rows.append({
            "id": _new_id(),
            **row.to_dict(),
        })

    if new_rows:
        combined = pd.concat(
            [existing, pd.DataFrame(new_rows)[COLUMNS]],
            ignore_index=True,
        )
        combined[COLUMNS].to_csv(EXPENSE_FILE, index=False)

    return len(new_rows), duplicates


def export_expenses():
    """Return all transactions as UTF-8 CSV bytes."""
    expenses = load_expenses()
    return expenses[COLUMNS].to_csv(index=False).encode("utf-8")
