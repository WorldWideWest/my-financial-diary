import streamlit as st
import pandas as pd

from main.components.tab.component import tabs 

from main.static.components.data import TABS


def main_site(data: pd.DataFrame):
    tabs_component = tabs(TABS)
