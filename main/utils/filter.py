import pandas as pd
import streamlit as st

class Filter(object):

    @st.cache
    def group_by_category(self, data: pd.DataFrame) -> pd.DataFrame:
        data_by_category = data.groupby("Category").sum()
        return data_by_category[["Amount"]]

    @st.cache
    def sum_by_month(data: pd.DataFrame, month: str) -> float:
        return data[(data["Month"] == month)]