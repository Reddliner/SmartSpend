
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from data_manager import load_expenses
from analysis import (
    get_category_summary,
    get_monthly_summary,
    get_top_category,
)
from charts import (
    create_category_pie_chart,
    create_category_bar_chart,
    create_monthly_line_chart,
)

st.set_page_config(
    page_title="SmartSpend",
    page_icon="💰",
    layout="wide",
)

st.title("💰 SmartSpend")
st.caption("Your personal finance overview")

expenses = load_expenses()

if not expenses.empty:
    expenses["date"] = pd.to_datetime(
        expenses["date"], errors="coerce"
    )
    expenses["amount"] = pd.to_numeric(
        expenses["amount"], errors="coerce"
    )
    expenses = expenses.dropna(
        subset=["date", "category", "description", "amount"]
    )
    expenses = expenses[expenses["amount"] > 0].copy()

total = float(expenses["amount"].sum()) if not expenses.empty else 0.0
count = len(expenses)
average = float(expenses["amount"].mean()) if count else 0.0
top_category, top_amount = get_top_category(expenses)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Expenses", f"₹{total:,.2f}")
col2.metric("Transactions", count)
col3.metric("Average Expense", f"₹{average:,.2f}")
col4.metric("Top Category", top_category or "N/A")

st.divider()

st.header("📊 Spending Analytics")

if expenses.empty:
    st.info("Add expenses on the Transactions page to see analytics.")
else:
    left, right = st.columns(2)

    with left:
        st.subheader("Category Distribution")
        fig = create_category_pie_chart(expenses)
        if fig is not None:
            st.pyplot(fig)
            plt.close(fig)

    with right:
        st.subheader("Spending by Category")
        fig = create_category_bar_chart(expenses)
        if fig is not None:
            st.pyplot(fig)
            plt.close(fig)

    st.subheader("Daily Spending Trend")
    fig = create_monthly_line_chart(expenses)
    if fig is not None:
        st.pyplot(fig)
        plt.close(fig)

    st.subheader("Category Summary")
    summary = get_category_summary(expenses).copy()
    summary["amount"] = summary["amount"].map(
        lambda value: f"₹{value:,.2f}"
    )
    summary["percentage"] = summary["percentage"].map(
        lambda value: f"{value:.1f}%"
    )
    st.dataframe(summary, use_container_width=True, hide_index=True)

    st.subheader("Monthly Spending")
    monthly = get_monthly_summary(expenses).copy()
    if not monthly.empty:
        monthly["amount"] = monthly["amount"].map(
            lambda value: f"₹{value:,.2f}"
        )
        st.dataframe(monthly, use_container_width=True, hide_index=True)

st.divider()

st.header("🧾 Recent Transactions")

if expenses.empty:
    st.info("No transactions recorded yet.")
else:
    recent = expenses.sort_values(
        "date", ascending=False
    ).head(10).copy()

    recent["date"] = recent["date"].dt.strftime("%d %b %Y")
    recent["amount"] = recent["amount"].map(
        lambda value: f"₹{value:,.2f}"
    )

    st.dataframe(
        recent[["date", "category", "description", "amount"]],
        use_container_width=True,
        hide_index=True,
    )

st.caption(
    "Use the sidebar to navigate between Dashboard, Transactions, "
    "Budgets, and Insights."
)
