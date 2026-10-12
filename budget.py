
import pandas as pd


def get_monthly_expenses(expenses, year, month):
    """Return expenses recorded in a specific month."""
    if expenses.empty:
        return 0.0

    df = expenses.copy()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

    df = df.dropna(subset=["date", "amount"])

    monthly = df[
        (df["date"].dt.year == year)
        & (df["date"].dt.month == month)
    ]

    return float(monthly["amount"].sum())


def calculate_budget_status(expenses, budget_amount, year, month):
    """Calculate budget usage and remaining balance."""
    budget_amount = float(budget_amount)

    if not pd.notna(budget_amount) or budget_amount <= 0:
        raise ValueError("Budget must be greater than zero.")

    spent = get_monthly_expenses(expenses, year, month)
    remaining = budget_amount - spent
    usage_percentage = (spent / budget_amount) * 100

    if spent > budget_amount:
        status = "exceeded"
    elif usage_percentage >= 80:
        status = "warning"
    else:
        status = "normal"

    return {
        "budget": budget_amount,
        "spent": spent,
        "remaining": remaining,
        "usage_percentage": usage_percentage,
        "status": status,
    }
