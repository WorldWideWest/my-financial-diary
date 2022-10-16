import streamlit as st
import pandas as pd
import datetime

def weekly(data: pd.DataFrame, week: int):
    weeks = []

    for date in data["Date"]:
        date = datetime.datetime.strptime(date, "%m/%d/%Y")

        weeks.append(date.isocalendar().week)
        
    data["Week"] = weeks
    
    weekly_data = data[data["Week"] == week]

    return weekly_data