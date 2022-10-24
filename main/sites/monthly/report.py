import streamlit as st
import pandas as pd
import math
import plotly.graph_objects as go
import plotly.express as px

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
        colorscale = "YlOrRd",
        hovertemplate = hovertemplate,
        texttemplate = texttemplate,
    ))

    figure.update_layout(
        xaxis = dict(showgrid = False),
        yaxis = dict(showgrid = False)
    )

    return figure


def get_figure(data: pd.DataFrame) -> px.line:
    fig = px.line(data, x="Date", y="Amount", markers = True)

    fig.data[0].line.color = "#FF800B"

    fig.update_layout(title_font_color = "#fff")

    fig.layout.plot_bgcolor = "rgba(0, 0, 0, 0)"
    fig.layout.paper_bgcolor = "rgba(0, 0, 0, 0)"

    fig.layout.yaxis.color = "#fff"
    fig.layout.xaxis.color = "#fff"

    hovertemplate = "<span style='color: #fff;'><span style='font-weight: 700;'>Day: %{x}</span>,<br>Amount: %{y:.2f} KM</span><extra></extra>"

    fig.update_traces(hovertemplate = hovertemplate)

    return fig

def monthly(data: pd.DataFrame, month: int):
    
    st.plotly_chart(get_weekly_spendings_heatmap(data), use_container_width = True)

    transactions = filter.filter_by_date(data, month = month)

    with st.expander("Monthly Transactions", expanded = False):
        st.dataframe(transactions)


    monthly_aggregation = filter.group_by_date(transactions)
    st.plotly_chart(get_figure(monthly_aggregation), use_container_width = True)

    




    