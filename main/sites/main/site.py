import streamlit as st
import pandas as pd

from main.components.tab.component import tabs 

from main.static.components.data import TABS


def main_site(data: pd.DataFrame):
    tabs_component = tabs(TABS)

    with tabs_component[0]: # Weekly Site
        from main.sites.weekly.report import weekly
        weekly(data.copy())
