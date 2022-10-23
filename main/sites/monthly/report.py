import streamlit as st
import pandas as pd


def monthly(data: pd.DataFrame, selected_month: int):
    
    # Sum total spendings for each week in the year
    # Assign the week to the months
    # Build a heatmap

    data["Date"] = pd.to_datetime(data["Date"], format="%m/%d/%Y")

    weekly_spendings = pd.DataFrame(
        columns = range(1, 53),
        rows = []
    )

    




    return