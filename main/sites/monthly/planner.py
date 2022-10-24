import streamlit as st
import pandas as pd

from main.db.repository import Repository

repository = Repository()

def monthly(data: pd.DataFrame, month: str):

    planned = data
        

    st.dataframe(planned[["Budget Labels", month]])

    return