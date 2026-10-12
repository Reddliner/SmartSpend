
from datetime import date

import pandas as pd
import streamlit as st

from data_manager import (
    load_expenses,
    add_expense,
    update_expense,
    delete_expense,
    import_expenses,
    export_expenses,
)

st.set_page_config(page_title="Transactions", page_icon="🧾", layout="wide")
st.title("🧾 Transactions")

categories = [
    "Food", "Transport", "Education", "Shopping",
    "Bills", "Entertainment", "Health", "Other",
]


def show_error(error):
    st.error(str(error))


st.header("Add an Expense")

with st.form("add_expense", clear_on_submit=True):
    expense_date = st.date_input("Date", value=date.today())
    category = st.selectbox("Category", categories)
    description = st.text_input("Description")
    amount = st.number_input("Amount (₹)", min_value=0.01, value=100.0)
    submitted = st.form_submit_button("Save Expense", type="primary")

    if submitted:
        if not description.strip():
            st.error("Please enter a description.")
        else:
            try:
                add_expense(expense_date, category, description, amount)
                st.success("Expense saved.")
                st.rerun()
            except (ValueError, OSError) as error:
                show_error(error)

st.divider()
st.header("Filter Transactions")

expenses = load_expenses()
filtered = expenses.copy()

if not expenses.empty:
    dates = pd.to_datetime(expenses["date"], errors="coerce").dropna()

    if not dates.empty:
        left, right = st.columns(2)
        with left:
            start = st.date_input("Start date", value=dates.min().date())
        with right:
            end = st.date_input("End date", value=dates.max().date())

        available = sorted(expenses["category"].unique().tolist())
        selected = st.multiselect(
            "Categories",
            available,
            default=available,
        )

        expense_dates = pd.to_datetime(
            expenses["date"], errors="coerce"
        ).dt.date

        if start <= end:
            mask = (
                expense_dates.between(start, end)
                & expenses["category"].isin(selected)
            )
            filtered = expenses.loc[mask].copy()
        else:
            filtered = expenses.iloc[0:0].copy()
            st.error("Start date must not be after end date.")

st.subheader(f"Transaction History ({len(filtered)})")

if filtered.empty:
    st.info("No transactions match your filters.")
else:
    display = filtered.copy()
    display["amount"] = display["amount"].map(
        lambda value: f"₹{float(value):,.2f}"
    )
    st.dataframe(display, use_container_width=True, hide_index=True)

st.divider()
st.header("Edit or Delete a Transaction")

all_expenses = load_expenses()

if not all_expenses.empty:
    records = all_expenses.copy()
    records["label"] = records.apply(
        lambda row: (
            f"{row['date']} | {row['description']} | "
            f"{row['category']} | ₹{float(row['amount']):,.2f}"
        ),
        axis=1,
    )

    selected_id = st.selectbox(
        "Select transaction",
        records["id"].tolist(),
        format_func=lambda value: records.loc[
            records["id"] == value, "label"
        ].iloc[0],
    )

    row = records.loc[records["id"] == selected_id].iloc[0]
    current_category = str(row["category"])
    edit_categories = categories.copy()

    if current_category not in edit_categories:
        edit_categories.append(current_category)

    with st.form("edit_expense"):
        edit_date = st.date_input(
            "Edit date",
            value=pd.to_datetime(row["date"]).date(),
        )
        edit_category = st.selectbox(
            "Edit category",
            edit_categories,
            index=edit_categories.index(current_category),
        )
        edit_description = st.text_input(
            "Edit description",
            value=str(row["description"]),
        )
        edit_amount = st.number_input(
            "Edit amount (₹)",
            min_value=0.01,
            value=float(row["amount"]),
        )
        update = st.form_submit_button("Save Changes")

        if update:
            try:
                update_expense(
                    selected_id,
                    edit_date,
                    edit_category,
                    edit_description,
                    edit_amount,
                )
                st.success("Transaction updated.")
                st.rerun()
            except (ValueError, OSError) as error:
                show_error(error)

    confirm = st.checkbox("Confirm permanent deletion")

    if st.button("Delete Transaction", disabled=not confirm):
        try:
            delete_expense(selected_id)
            st.success("Transaction deleted.")
            st.rerun()
        except (ValueError, OSError) as error:
            show_error(error)

st.divider()
st.header("CSV Import and Export")

uploaded = st.file_uploader("Upload expense CSV", type=["csv"])

if uploaded is not None and st.button("Import CSV"):
    try:
        added, duplicates = import_expenses(uploaded)
        st.success(
            f"Imported {added} transaction(s); skipped {duplicates} duplicate(s)."
        )
        st.rerun()
    except (ValueError, OSError) as error:
        show_error(error)

st.download_button(
    "Download All Expenses",
    data=export_expenses(),
    file_name="smartspend_expenses.csv",
    mime="text/csv",
)
