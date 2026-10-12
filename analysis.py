import pandas as pd
from datetime import date

def get_total_expenses(expenses):
    """Return the sum of all expenses."""
    if expenses.empty:
        return 0.0

    return float(expenses["amount"].sum())


def get_average_expense(expenses):
    """Return the average transaction amount."""
    if expenses.empty:
        return 0.0

    return float(expenses["amount"].mean())


def get_category_summary(expenses):
    """Calculate total spending by category."""
    if expenses.empty:
        return pd.DataFrame(
            columns=["category", "amount", "percentage"]
        )

    summary = (
        expenses.groupby("category", as_index=False)["amount"]
        .sum()
        .sort_values("amount", ascending=False)
    )

    total = summary["amount"].sum()

    summary["percentage"] = (
        summary["amount"] / total * 100
        if total > 0
        else 0
    )

    return summary.reset_index(drop=True)


def get_monthly_summary(expenses):
    """Calculate total spending for each month."""
    if expenses.empty:
        return pd.DataFrame(
            columns=["month", "amount"]
        )

    df = expenses.copy()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])

    df["month"] = df["date"].dt.to_period("M").astype(str)

    summary = (
        df.groupby("month", as_index=False)["amount"]
        .sum()
        .sort_values("month")
    )

    return summary.reset_index(drop=True)


def get_daily_summary(expenses):
    """Calculate total spending for each day."""
    if expenses.empty:
        return pd.DataFrame(
            columns=["date", "amount"]
        )

    df = expenses.copy()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])

    summary = (
        df.groupby(df["date"].dt.date)["amount"]
        .sum()
        .reset_index(name="amount")
        .rename(columns={"date": "date"})
        .sort_values("date")
    )

    return summary.reset_index(drop=True)


def get_top_category(expenses):
    """Return the highest-spending category and its total."""
    summary = get_category_summary(expenses)

    if summary.empty:
        return None, 0.0

    top = summary.iloc[0]

    return str(top["category"]), float(top["amount"])


def generate_financial_insights(expenses, budget=None):
    """Generate simple, data-driven personal finance insights."""
    insights = []

    if expenses.empty:
        return [
            "Start recording expenses to receive personalized "
            "spending insights."
        ]

    df = expenses.copy()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

    df = df.dropna(subset=["date", "amount"])
    df = df[df["amount"] > 0]

    if df.empty:
        return ["No valid expense records are available for analysis."]

    today = date.today()
    current_month = df[
        (df["date"].dt.year == today.year)
        & (df["date"].dt.month == today.month)
    ]

    # Highest-spending category across all recorded transactions
    category_totals = df.groupby("category")["amount"].sum()

    if not category_totals.empty:
        top_category = category_totals.idxmax()
        top_amount = float(category_totals.max())
        total = float(category_totals.sum())
        share = top_amount / total * 100 if total else 0

        insights.append(
            f"Your highest-spending category is {top_category}, "
            f"with ₹{top_amount:,.2f} spent "
            f"({share:.1f}% of recorded expenses)."
        )

    # Current-month spending
    month_spent = float(current_month["amount"].sum())

    if current_month.empty:
        insights.append(
            "You have no recorded expenses for the current month."
        )
    else:
        insights.append(
            f"You have recorded ₹{month_spent:,.2f} "
            f"in expenses this month."
        )

        active_days = current_month["date"].dt.date.nunique()
        daily_average = month_spent / active_days

        insights.append(
            f"Your average spending per day with recorded "
            f"expenses this month is ₹{daily_average:,.2f}."
        )

    # Compare the two most recent calendar months with data
    df["month"] = df["date"].dt.to_period("M")

    monthly_totals = df.groupby("month")["amount"].sum().sort_index()

    if len(monthly_totals) >= 2:
        previous = float(monthly_totals.iloc[-2])
        latest = float(monthly_totals.iloc[-1])

        if previous > 0:
            change = (latest - previous) / previous * 100

            if change > 0:
                insights.append(
                    f"Spending increased by {change:.1f}% "
                    "compared with the previous month with recorded "
                    "expenses."
                )
            elif change < 0:
                insights.append(
                    f"Spending decreased by {abs(change):.1f}% "
                    "compared with the previous month with recorded "
                    "expenses."
                )
            else:
                insights.append(
                    "Spending was unchanged compared with the "
                    "previous month with recorded expenses."
                )

    # Budget assessment for the current month
    if budget is not None and budget > 0:
        percentage = month_spent / budget * 100
        remaining = budget - month_spent

        if percentage > 100:
            insights.append(
                f"You exceeded your current monthly budget by "
                f"₹{abs(remaining):,.2f}. Review non-essential spending."
            )
        elif percentage >= 80:
            insights.append(
                f"You have used {percentage:.1f}% of your monthly "
                f"budget. ₹{remaining:,.2f} remains."
            )
        else:
            insights.append(
                f"You have used {percentage:.1f}% of your monthly "
                f"budget, with ₹{remaining:,.2f} remaining."
            )

    # Actionable suggestion based on category concentration
    if not category_totals.empty and total > 0:
        if share >= 40:
            insights.append(
                f"Consider reviewing your {top_category} spending "
                "to see whether there are opportunities to save."
            )

    return insights
