import streamlit as st
import pandas as pd

from main.utils.filter import Filter

filter = Filter()


def monthly(data: pd.DataFrame, month: int):
    processed = data.copy()
    
    processed["Date"] =  pd.to_datetime(processed["Date"], format="%m/%d/%Y")

    processed = processed[(processed["Date"].dt.month == month)]

    data_by_category = filter.group_by_category(processed)





    return data_by_category