import streamlit as st
import pandas as pd
import math
import plotly.graph_objects as go

from main.static.components.data import MONTHS
from main.utils.filter import Filter

filter = Filter()


@st.experimental_memo()
def weekly_spendings_data_filter(data: pd.DataFrame) -> dict: 
    data["Date"] = pd.to_datetime(data["Date"], format="%m/%d/%Y")

    processed = data.copy()
    processed["Month"] = processed["Date"].dt.month_name()
    processed["Week"] = pd.to_numeric(processed["Date"].dt.day / 7).apply(lambda x: math.ceil(x))

    months = pd.DataFrame()

    for month in range(1, 13):

        aggregated_weeks = processed[processed["Month"] == MONTHS[month]].groupby("Week").sum("Amount")
        aggregated_weeks = pd.Series(aggregated_weeks["Amount"].tolist(), index = aggregated_weeks.index)
            
        months[MONTHS[month]] = aggregated_weeks

    
    return {
        "z": months.values.tolist(),
        "x": months.columns.tolist(),
        "y": months.index.tolist()
    }


@st.cache()
def get_weekly_spendings_heatmap(data: pd.DataFrame) -> go.Heatmap:
    heatmap_object = weekly_spendings_data_filter(data)

    hovertemplate = "Month: %{x},<br>Week: %{y},<br>Spending: %{z:.2f} KM<extra></extra>"
    texttemplate = "%{z:.2f}"

    figure = go.Figure(data = go.Heatmap(
        heatmap_object,
        colorscale = "magma",
        hovertemplate = hovertemplate,
        texttemplate = texttemplate,
    ))

    figure.update_layout(
        xaxis = dict(showgrid = False),
        yaxis = dict(showgrid = False)
    )

    return figure

def monthly(data: pd.DataFrame, selected_month: int):
    
    st.plotly_chart(get_weekly_spendings_heatmap(data), use_container_width = True)

    grouped_by_category = filter.get_monthly_transactions(data, selected_month)

    st.dataframe(grouped_by_category)




    