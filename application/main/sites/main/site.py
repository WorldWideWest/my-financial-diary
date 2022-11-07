import os
import streamlit as st
import pandas as pd
import datetime as dt
import math

from main.components.tab.component import tabs 
from main.components.selectbox.component import selectbox
from main.db.repository import Repository
from main.utils.filter import Filter
from main.utils.chart import Chart

from main.static.components.data import TABS, MONTHS

WORKBOOK = os.environ.get("WORKBOOK")


def main_site(data: pd.DataFrame, planned: pd.DataFrame):
    tabs_component = tabs(TABS)

    with st.sidebar:
        year = st.selectbox(
            "Select the Year",
            options = range(2022, 2024),
            index = 0
        )

        month = selectbox(
            "Select the Month", 
            MONTHS, 
            dt.datetime.today().month - 1
        )

        week = st.selectbox(
            "Select the Week",
            options = range(1, 6),
            index = math.ceil(dt.datetime.today().day / 7) - 1
        )


    with tabs_component[0]: # Weekly Site
        from main.sites.weekly.report import Weekly
        weekly = Weekly(Repository(), Filter(), Chart(), WORKBOOK)

        weekly.set_year(year)
        weekly.set_month(month)
        weekly.set_week(week)
        
        weekly.report()


    with tabs_component[1]: # Monthly Site
        from main.sites.monthly.report import Monthly
        monthly = Monthly(Repository(), Filter(), Chart(), WORKBOOK)
        monthly.report(month, year)

