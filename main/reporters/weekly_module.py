import streamlit as st
import pandas as pd
import datetime

@st.cache
def categorised_data(weekly_data: pd.DataFrame) -> pd.DataFrame:
    data_by_category = weekly_data.groupby("Category").sum()
    return data_by_category[["Amount"]]


def weekly(data: pd.DataFrame, static_data: pd.DataFrame, week: int):
    weeks = []
    processed = data.copy()
    data_by_category = None

    for date in processed["Date"]:
        date = datetime.datetime.strptime(date, "%m/%d/%Y")

        weeks.append(date.isocalendar().week)
        
    processed["Week"] = weeks
    
    processed = processed[processed["Week"] == week]
    
    if(not processed.empty):
        data_by_category = categorised_data(processed)

    return processed, data_by_category

