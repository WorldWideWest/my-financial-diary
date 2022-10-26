import streamlit as st
import pandas as pd
import math
import plotly.graph_objects as go
import plotly.express as px

from main.static.components.data import MONTHS
from main.utils.filter import Filter
from main.utils.chart import Chart

filter = Filter()
chart = Chart()

hovertemplate = "<span style='color: #fff;'><span style='font-weight: 700;'>Day: %{x}</span>,<br>Amount: %{y:.2f} KM</span><extra></extra>"
heatmap_hover_template = "<span style='background-color: #fff; color: #001024;'>Month: %{x},<br>Week: %{y},<br>Spending: %{z:.2f} KM</span><extra></extra>"

class Monthly:

    @st.experimental_memo()
    def weekly_spendings_data_filter(_self, data: pd.DataFrame) -> dict: 
        processed = filter.filter_by_date(data)
        processed["Month"] = processed["Date"].dt.month_name()

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


    @st.experimental_memo()
    def get_weekly_spendings_heatmap(_self, data: pd.DataFrame) -> go.Figure:
        heatmap_object = _self.weekly_spendings_data_filter(data)

        texttemplate = "%{z:.2f}"

        figure = go.Figure(data = go.Heatmap(
            heatmap_object,
            colorscale = "YlOrRd",
            hovertemplate = hovertemplate,
            texttemplate = texttemplate,
            xgap = 2,
            ygap = 2
        ))

        figure.update_layout(
            xaxis = dict(showgrid = False),
            yaxis = dict(showgrid = False),
            hoverlabel = dict(bgcolor = "white"),
        )

        return figure


    @st.experimental_memo()
    def report(_self, data: pd.DataFrame, month: int, year: int):
        
        heatmap = _self.get_weekly_spendings_heatmap(data)
        heatmap.layout.title = f"Spendings for each Week in the Month for { year }"
        heatmap.update_traces(hovertemplate = heatmap_hover_template)

        st.plotly_chart(heatmap, use_container_width = True)

        transactions = filter.filter_by_date(data, month = month)

        with st.expander(f"Transactions for { MONTHS[month] }", expanded = False):
            st.dataframe(transactions)

        monthly_aggregation = filter.group_by_date(transactions)
        
        figure = chart.line(monthly_aggregation, "Date", "Amount")
        figure.update_traces(hovertemplate = hovertemplate)
        figure.layout.title = f"Spendings by Day in { MONTHS[month] }"

        st.plotly_chart(figure, use_container_width = True)

        




    