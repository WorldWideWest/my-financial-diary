import streamlit as st
import pandas as pd
import datetime as dt

from main.utils.filter import Filter

filter = Filter()

def weekly(data: pd.DataFrame) -> pd.DataFrame:
    """
        Make sure that the data is a copy of the dataframe and not 
        the original object that is fetched from Google Sheets API.

        To do that on passing the `data` argument to the function add
        the pandas method copy() in front of it to make sure that the 
        DataFrame was in fact copied.
    """
    data["Date"] = pd.to_datetime(data["Date"], format="%m/%d/%Y")
    
    WEEK = dt.date.today().isocalendar().week
    
    transactions = data[(
        data["Date"].dt.isocalendar().week == WEEK
    )]
    grouped_transactions = filter.group_by_category(transactions)

    transactions_container = st.container()
    transactions_container.markdown(f"<h3 style='text-align:center;'>All Transactions in the Week { WEEK } of the Year</h3>", unsafe_allow_html = True)
    transactions_container.dataframe(transactions, use_container_width = True)
    
    grouped_transactions_container = st.columns([1, 2])
    grouped_transactions_container[0].markdown(f"<h6 style='text-align:center;'>Grouped Transactions by Category for the Week { WEEK } of the Year</h6>", unsafe_allow_html = True)
    grouped_transactions_container[0].dataframe(grouped_transactions)
    
    grouped_transactions_container[1].markdown(f"<h5 style='text-align:center;'>Transactions by Day for the { WEEK } of the Year</h5>", unsafe_allow_html = True)
    grouped_transactions_container[1].line_chart(transactions, x = "Date", y = "Amount")
