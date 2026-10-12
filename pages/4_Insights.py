
from datetime import date

import streamlit as st

from data_manager import load_expenses
from budget_manager import get_budget
from analysis import generate_financial_insights

st.set_page_config(page_title="Insights", page_icon="💡", layout="wide")
st.title("💡 Financial Insights")

expenses = load_expenses()
today = date.today()
budget = get_budget(today.year, today.month)

st.caption("Insights are calculated from your saved transactions.")

insights = generate_financial_insights(
    expenses,
    budget=budget,
)

for number, insight in enumerate(insights, start=1):
    st.markdown(f"**{number}.** {insight}")

st.divider()
st.caption(
    "These insights are based on recorded expenses and are intended "
    "to support budgeting decisions."
)
