import streamlit as st

from .utils.get_data import fetch


def run():
    data = fetch()


    tabs = st.tabs(["Weekly", "Monthly", "Yarly", "Total"])

    st.header("Welcome to your financial report")
    
    from .reporters.weekly_module import weekly
    weekly(data)

    st.dataframe(data)

