import datetime
import streamlit as st

from .utils.get_data import fetch


def run():
    data = fetch()

    CURRENT_WEEK = datetime.datetime.today().isocalendar().week

    tabs = st.tabs(["Weekly", "Monthly", "Yarly", "Total"])
    st.header("Welcome to your financial report")
    
    from .reporters.weekly_module import weekly
    tabs[0].dataframe(weekly(data, CURRENT_WEEK))

