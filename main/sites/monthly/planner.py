import streamlit as st
import pandas as pd

from main.db.repository import Repository

repository = Repository()

def monthly_planner(data: pd.DataFrame, month: str):

    planned = data
        

    st.dataframe(planned[["Categories", month]])

    return