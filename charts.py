
import matplotlib.pyplot as plt
import pandas as pd


def create_category_pie_chart(expenses):
    """Create a pie chart of spending by category."""
    if expenses.empty:
        return None

    summary = expenses.groupby("category")["amount"].sum()
    summary = summary[summary > 0]

    if summary.empty:
        return None

    fig, ax = plt.subplots(figsize=(7, 5))

    ax.pie(
        summary.values,
        labels=summary.index,
        autopct="%1.1f%%",
        startangle=90,
    )
    ax.set_title("Expense Distribution by Category")
    ax.axis("equal")

    fig.tight_layout()
    return fig


def create_category_bar_chart(expenses):
    """Compare total spending across categories."""
    if expenses.empty:
        return None

    summary = (
        expenses.groupby("category")["amount"]
        .sum()
        .sort_values(ascending=True)
    )

    if summary.empty:
        return None

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.barh(summary.index, summary.values)
    ax.set_title("Spending by Category")
    ax.set_xlabel("Amount (₹)")
    ax.set_ylabel("Category")
    ax.grid(axis="x", alpha=0.3)

    fig.tight_layout()
    return fig


def create_monthly_line_chart(expenses):
    """Display spending trends over time."""
    if expenses.empty:
        return None

    df = expenses.copy()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df = df.dropna(subset=["date", "amount"])

    if df.empty:
        return None

    daily = (
        df.groupby(df["date"].dt.normalize())["amount"]
        .sum()
        .sort_index()
    )

    fig, ax = plt.subplots(figsize=(9, 5))

    ax.plot(
        daily.index,
        daily.values,
        marker="o",
        linewidth=2,
    )

    ax.set_title("Daily Spending Trend")
    ax.set_xlabel("Date")
    ax.set_ylabel("Amount (₹)")
    ax.grid(True, alpha=0.3)
    fig.autofmt_xdate()
    fig.tight_layout()

    return fig
