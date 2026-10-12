
import calendar
from datetime import date

import streamlit as st

from data_manager import load_expenses
from budget import calculate_budget_status
from budget_manager import get_budget, save_budget

st.set_page_config(page_title="Budgets", page_icon="🎯", layout="wide")
st.title("🎯 Monthly Budgets")

today = date.today()

col1, col2 = st.columns(2)

with col1:
    year = st.number_input(
        "Year", min_value=1900, max_value=2200,
        value=today.year, step=1,
    )

with col2:
    month = st.selectbox(
        "Month",
        range(1, 13),
        index=today.month - 1,
        format_func=lambda value: calendar.month_name[value],
    )

year = int(year)
month = int(month)
saved = get_budget(year, month)

with st.form("save_budget"):
    amount = st.number_input(
        "Monthly budget (₹)",
        min_value=0.0,
        value=saved if saved is not None else 5000.0,
        step=500.0,
    )
    submitted = st.form_submit_button("Save Budget", type="primary")

    if submitted:
        if amount <= 0:
            st.error("Budget must be greater than zero.")
        else:
            try:
                save_budget(year, month, amount)
                st.success("Budget saved.")
                st.rerun()
            except (ValueError, OSError) as error:
                st.error(str(error))

saved = get_budget(year, month)

if saved is not None:
    status = calculate_budget_status(
        load_expenses(), saved, year, month
    )

    a, b, c = st.columns(3)
    a.metric("Budget", f"₹{saved:,.2f}")
    b.metric("Spent", f"₹{status['spent']:,.2f}")
    c.metric("Remaining", f"₹{status['remaining']:,.2f}")

    percentage = status["usage_percentage"]
    st.progress(min(max(percentage / 100, 0.0), 1.0))

    if status["status"] == "exceeded":
        st.error(f"Budget exceeded by ₹{abs(status['remaining']):,.2f}.")
    elif status["status"] == "warning":
        st.warning(f"{percentage:.1f}% of the budget has been used.")
    else:
        st.success(f"{percentage:.1f}% of the budget has been used.")
else:
    st.info("Save a budget to start monitoring monthly spending.")
