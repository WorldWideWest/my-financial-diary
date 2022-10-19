import streamlit as st
import pandas as pd
import datetime

from main.components.tab.component import tabs 
from main.components.selectbox.component import selectbox

from main.static.components.data import TABS, MONTHS


def main_site(data: pd.DataFrame):
    tabs_component = tabs(TABS)
    selected_month, selected_week = None, None

    with st.sidebar:
        selected_month = selectbox(
            "Select the month", 
            MONTHS, 
            datetime.datetime.today().month - 1
        )

        selected_week = st.selectbox(
            "Select the week",
            options = range(1, 53),
            index = datetime.datetime.today().isocalendar().week - 1
        )

    with tabs_component[0]: # Weekly Site
        from main.sites.weekly.report import weekly
        weekly(data.copy())
