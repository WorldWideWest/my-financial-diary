import streamlit as st
import pandas as pd
import datetime as dt

import plotly.express as px

from main.utils.filter import Filter

filter = Filter()
WEEK = dt.date.today().isocalendar().week

def get_figure(data: pd.DataFrame) -> px.line:
    fig = px.line(data, x="Date", y="Amount", markers = True)

    fig.data[0].line.color = "#FF800B"

    fig.update_layout(title_font_color = "#fff")

    fig.layout.plot_bgcolor = "rgba(0, 0, 0, 0)"
    fig.layout.paper_bgcolor = "rgba(0, 0, 0, 0)"

    fig.layout.yaxis.color = "#fff"
    fig.layout.xaxis.color = "#fff"

    return fig

def transactions_view(transactions: pd.DataFrame, week: int) -> st.container:
    transactions_container = st.container()
    transactions_container.markdown(f"<h3 style='text-align:center;'>All Transactions in the Week { week } of the Year</h3>", unsafe_allow_html = True)
    transactions_container.dataframe(transactions, use_container_width = True)

    return transactions_container
    
def grouped_transactions_view(transactions: pd.DataFrame, grouped_transactions: pd.DataFrame, week: int) -> st.columns:
    grouped_transactions_container = st.columns([1, 3])
    grouped_transactions_container[0].markdown(f"<h6 style='text-align:center;'>Grouped Transactions by Category for the Week { WEEK } of the Month</h6>", unsafe_allow_html = True)
    grouped_transactions_container[0].dataframe(grouped_transactions)
    
    transactions = filter.group_by_date(transactions)

    figure = get_figure(transactions)
    figure.layout.title = f"Spendings by Day for the Week { week }"

    grouped_transactions_container[1].plotly_chart(figure, use_container_width = True)

    return grouped_transactions_container

def get_required_container(transactions: pd.DataFrame):
    actual_spendings = transactions["Amount"].sum()
    
    # Insted of 50, we want the value for the devidable categories devided by 4 (4 stands for the weeks in the month) 
    
    if(actual_spendings > 50):
        return st.error(f"{ actual_spendings } / { 50 }")
    return st.success(f"{ actual_spendings } / { 50 }")

def planned_spendings_info_view(transactions: pd.DataFrame) -> st.columns:
    planned_spending_container = st.columns([3, 1])
    planned_spending_container[0].info(f"Planned and Actual spendings for the week { WEEK }")

    with planned_spending_container[1]:
        get_required_container(transactions)

    return planned_spending_container

def weekly(data: pd.DataFrame, year: int = None, month: int = None, week: int = None) -> pd.DataFrame:
    """
        Make sure that the data is a copy of the dataframe and not 
        the original object that is fetched from Google Sheets API.

        To do that on passing the `data` argument to the function add
        the pandas method copy() in front of it to make sure that the 
        DataFrame was in fact copied.
    """
    
    filtered = data.copy()

    filtered["Date"] = pd.to_datetime(filtered["Date"], format="%m/%d/%Y")

    transactions = filter.filter_by_date(filtered, year = year, month = month, week = week)
    grouped = filter.group_by_category(transactions)

    with st.expander("Transactions", expanded = True):
        transactions_view(transactions, week)

    grouped_transactions_view(transactions, grouped, week)

    planned_spendings_info_view(transactions)


