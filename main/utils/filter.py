import pandas as pd
import streamlit as st
import math

class Filter(object):

    @st.cache()
    def group_by_category(self, data: pd.DataFrame) -> pd.DataFrame:
        grouped = data.groupby("Category").sum("Amount")

        return grouped[["Amount"]]

    @st.cache()
    def filter_by_date(self, data: pd.DataFrame, day:int = None, week:int = None, month:int = None, year:int = None) -> pd.DataFrame:
        data["Date"] = pd.to_datetime(data["Date"], format="%m/%d/%Y")
        data["Week"] = pd.to_numeric(data["Date"].dt.day / 7).apply(lambda x: math.ceil(x))
        
        if year:
            data = data[data["Date"].dt.year == year]
        
        if month:
            data = data[data["Date"].dt.month == month]
        
        if week:
            data = data[data["Week"] == week]
        
        if day:
            data = data[data["Date"].dt.day == day]

        return data

    @st.cache()
    def get_monthly_transactions(self, data: pd.DataFrame, month: int) -> float:
        data["Date"] = pd.to_datetime(data["Date"], format="%m/%d/%Y")
        return data[(data["Date"].dt.month == month)]