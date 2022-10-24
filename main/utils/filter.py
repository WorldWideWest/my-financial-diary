import pandas as pd
import streamlit as st

class Filter(object):

    @st.cache()
    def group_by_category(self, data: pd.DataFrame, month = 0) -> pd.DataFrame:
        data_by_category = None
        
        if month == 0:
            data_by_category = data.groupby("Category").sum("Amount")
        else:
            data_by_category = data[
                (data["Date"].dt.month == month)
            ].groupby("Category").sum("Amount")

        return data_by_category[["Amount"]]

    @st.cache()
    def get_monthly_transactions(self, data: pd.DataFrame, month: int) -> float:
        data["Date"] = pd.to_datetime(data["Date"], format="%m/%d/%Y")
        return data[(data["Date"].dt.month == month)]