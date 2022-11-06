import pandas as pd
import streamlit as st
import math

class Filter(object):

    @st.experimental_memo()
    def group_by_category(_self, data: pd.DataFrame) -> pd.DataFrame:
        grouped = data.groupby("Category").sum("Amount")

        return grouped[["Amount"]]
    
    @st.experimental_memo()
    def group_by_date(_self, data: pd.DataFrame) -> pd.DataFrame:
        data["Date"] = pd.to_datetime(data["Date"], format="%m/%d/%Y")

        grouped = data.groupby("Date", as_index = False).sum("Amount")
        return grouped[["Date", "Amount"]]

    @st.experimental_memo()
    def filter_by_date(_self, data: pd.DataFrame, day:int = None, week:int = None, month:int = None, year:int = None) -> pd.DataFrame:
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

    @st.experimental_memo()
    def get_monthly_transactions(_self, data: pd.DataFrame, month: int) -> float:
        data["Date"] = pd.to_datetime(data["Date"], format="%m/%d/%Y")
        return data[(data["Date"].dt.month == month)]

    @st.experimental_memo()
    def spendings_statistics(_self, planned: pd.DataFrame, transactions: pd.DataFrame, month: str, devidable: bool) -> pd.DataFrame:

        """
            `spendings_statistics` - method takes as arguments:
                - planned - a DataFrame that includes the planned spendings by category for a given month
                - transactions - is a DataFrame with all transactions for the month that the data was planned for
                - month - string representation of a month
                - devidable - is a column in the planned DataFrame where the categories are splited into devidable (TRUE) and not devidable (FALSE), those who are not devidable will only show up in the monthly planning and those who are devidable will show up in the weekly preview.
        """

        data = planned.copy()
        data["Devidable"] = data["Devidable"].replace({"TRUE": True, "FALSE": False})

        if not isinstance(_self.try_get_column(data, month), IndexError):
            data = data[data["Devidable"] == devidable]
            data = data[["Categories", month]]

            data["Spent"], total = 0, 0

            for category in planned["Categories"]:
                total = transactions[transactions["Category"] == category]["Amount"].sum()
                index = data[data["Categories"] == category].index
                
                if not isinstance(_self.try_get_index(index), IndexError):
                    index = index[0]
                    data.loc[index, "Spent"] = total
        
        return data

    def try_get_index(_self, index):
        try:
            index[0:1][0]
        except IndexError as e:
            return e

    def try_get_column(_self, data: pd.DataFrame, month: str):
        try:
            data[month]
        except IndexError as e:
            return e