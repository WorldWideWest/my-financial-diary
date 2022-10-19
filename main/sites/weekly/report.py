import streamlit as st
import pandas as pd
import datetime as dt

from main.utils.filter import Filter

filter = Filter()
WEEK = dt.date.today().isocalendar().week


def transactions_view(transactions: pd.DataFrame) -> st.container:
    transactions_container = st.container()
    transactions_container.markdown(f"<h3 style='text-align:center;'>All Transactions in the Week { WEEK } of the Year</h3>", unsafe_allow_html = True)
    transactions_container.dataframe(transactions, use_container_width = True)

    return transactions_container
    
def grouped_transactions_view(transactions: pd.DataFrame, grouped_transactions: pd.DataFrame) -> st.columns:
    grouped_transactions_container = st.columns([1, 2])
    grouped_transactions_container[0].markdown(f"<h6 style='text-align:center;'>Grouped Transactions by Category for the Week { WEEK } of the Year</h6>", unsafe_allow_html = True)
    grouped_transactions_container[0].dataframe(grouped_transactions)
    
    grouped_transactions_container[1].markdown(f"<h5 style='text-align:center;'>Transactions by Day for the { WEEK } of the Year</h5>", unsafe_allow_html = True)
    transactions_by_date = transactions.groupby("Date").sum()

    transactions_grouped_by_date = transactions.groupby("Date").sum()
    transactions_by_date = pd.DataFrame(
        data = {
            "Date": transactions_grouped_by_date.index,
            "Amount": transactions_by_date["Amount"]
        }
    )

    grouped_transactions_container[1].line_chart(transactions_by_date, x = "Date", y = "Amount")

    return grouped_transactions_container

def get_required_container(transactions: pd.DataFrame):
    actual_spendings = transactions["Amount"].sum()
    if(actual_spendings > 50):
        return st.error(f"{ actual_spendings } / { 50 }")
    return st.success(f"{ actual_spendings } / { 50 }")

def planned_spendings_info_view(transactions: pd.DataFrame) -> st.columns:
    planned_spending_container = st.columns([3, 1])
    planned_spending_container[0].info(f"Planned and Actual spendings for the week { WEEK }")

    with planned_spending_container[1]:
        get_required_container(transactions)

    return planned_spending_container

def weekly(data: pd.DataFrame) -> pd.DataFrame:
    """
        Make sure that the data is a copy of the dataframe and not 
        the original object that is fetched from Google Sheets API.

        To do that on passing the `data` argument to the function add
        the pandas method copy() in front of it to make sure that the 
        DataFrame was in fact copied.
    """
    data["Date"] = pd.to_datetime(data["Date"], format="%m/%d/%Y")
    
    
    transactions = data[(
        data["Date"].dt.isocalendar().week == WEEK
    )]

    grouped_transactions = filter.group_by_category(transactions)

    with st.expander("Transactions", expanded = True):
        transactions_view(transactions)

    grouped_transactions_view(transactions, grouped_transactions)

    planned_spendings_info_view(transactions)


