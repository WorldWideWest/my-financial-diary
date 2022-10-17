import datetime
import pandas as pd
import streamlit as st

from .utils.get_data import fetch


def run():
    data = fetch("data")

    static_data = fetch("static-data")

    CURRENT_WEEK = datetime.datetime.today().isocalendar().week

    tabs = st.tabs(["Weekly", "Monthly", "Yarly", "Total"])

    with st.sidebar:
        CURRENT_WEEK = st.number_input(
            label = "Select the Week of the Year",
            min_value = 1, max_value = 52
        )

    with tabs[0]:
        from .reporters.weekly_module import weekly
        weekly_data = weekly(data, static_data, CURRENT_WEEK)

        st.title("Welcome to your financial report")

        st.dataframe(weekly_data[0])
        st.dataframe(weekly_data[1])

    with tabs[1]:
        from .reporters.monthly_module import monthly
        monthly_data = monthly(data, 9)

        st.dataframe(monthly_data)

