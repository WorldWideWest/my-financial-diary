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
    transactions_container.subheader(f"All Transactions in the Week { WEEK } of the Year")
    transactions_container.dataframe(transactions, use_container_width = True)
    
    grouped_transactions_container = st.columns(2)
    grouped_transactions_container[0].subheader(f"Grouped Transactions by Category for the Week { WEEK } of the Year")
    grouped_transactions_container[0].dataframe(grouped_transactions)
