import datetime
import pandas as pd
import streamlit as st

from .utils.get_data import fetch
from .components.form.form import form
from .static.static_data import MONTHS, TABS


def run():
    data = fetch(0)
    static_data = fetch(2)
    


    CURRENT_WEEK = datetime.datetime.today().isocalendar().week
    CURRENT_MONTH = datetime.datetime.today().month

    print(data)

    static_data.to_csv("static_data.csv")

    tabs = st.tabs(TABS)

    with st.sidebar:
        CURRENT_WEEK = st.number_input(
            label = "Select the Week of the Year",
            min_value = 1, max_value = 52
        )

        CURRENT_MONTH = st.selectbox(
            label = "Select the month",
            options = list(MONTHS.keys()),
            index = CURRENT_MONTH,
            format_func = lambda x:MONTHS[ x ]
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
        
        form_component = form(static_data)

