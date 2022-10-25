import streamlit as st
import pandas as pd
import datetime as dt
import math

from main.components.tab.component import tabs 
from main.components.selectbox.component import selectbox

from main.static.components.data import TABS, MONTHS


def main_site(data: pd.DataFrame, planned: pd.DataFrame):
    tabs_component = tabs(TABS)
    selected_month, selected_week = None, None

    with st.sidebar:
        select_year = st.selectbox(
            "Select the Year",
            options = range(2022, 2024),
            index = 0
        )

        selected_month = selectbox(
            "Select the Month", 
            MONTHS, 
            dt.datetime.today().month - 1
        )

        selected_week = st.selectbox(
            "Select the Week",
            options = range(1, 6),
            index = math.ceil(dt.datetime.today().day / 7) - 1
        )


    with tabs_component[0]: # Weekly Site
        from main.sites.weekly.report import weekly
        weekly(data.copy(), select_year, selected_month, selected_week)


    with tabs_component[1]: # Monthly Site
        from main.sites.monthly.report import monthly
        monthly(data.copy(), selected_month)

        from main.sites.monthly.planner import monthly_planner
        monthly_planner(planned, MONTHS[selected_month])
