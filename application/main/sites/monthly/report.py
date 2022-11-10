import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from main.utils.filter import Filter
from main.utils.chart import Chart
from main.db.repository import Repository
from main.sites.base.base_report import BaseReport

from main.static.components.data import MONTHS


class Monthly(BaseReport):

    def __init__(_self, repository: Repository, filter: Filter, chart: Chart, workbook: str) -> None:
        _self.__workbook = workbook
        _self.__repository = repository
        _self.__filter = filter
        _self.__chart = chart

        _self.get_data()

    def get_data(_self):
        _self.data = _self.__repository.fetch(_self.__workbook, 0)
        _self.planned = _self.__repository.fetch(_self.__workbook, 1)

    @st.experimental_memo()
    def weekly_spendings_data_filter(_self, data: pd.DataFrame) -> dict: 
        processed = _self.__filter.filter_by_date(data = data)
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
        hovertemplate = "<span style='background-color: #fff; color: #001024;'>Month: %{x},<br>Week: %{y},<br>Spending: %{z:.2f} KM</span><extra></extra>"

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

    def get_required_container(_self, data: pd.DataFrame):
        text = f"No Statistics Available for { _self.month_name }"

        if not isinstance(_self.__filter.try_get_column(data, _self.month_name), KeyError):
            planned = data[_self.month_name].sum()
            actual = data["Spent"].sum()

            text = "{:.2f} / {:.2f}".format(actual, planned)

            return {"status": "error", "content": text} if actual > planned else {"status": "success", "content": text}

        return {"status": "error", "content": text}
    
    def get_spendings_info_component(_self, data: pd.DataFrame) -> st.columns:
        planned_spending_container = st.columns([3, 1])
        planned_spending_container[0].info(f"Planned and Actual spendings for the week { _self.week } in { _self.month_name }")

        result = _self.get_required_container(data)
        
        if result["status"] == "error":
            planned_spending_container[1].error(result["content"])
        else:
            planned_spending_container[1].success(result["content"])

        return planned_spending_container
    
    def process(_self):

        heatmap = _self.get_weekly_spendings_heatmap(_self.data)
        heatmap.layout.title = f"Spendings for each Week in the Month for { _self.year }"

        transactions = _self.__filter.filter_by_date(_self.data, month = _self.month)

        spendings_by_day = _self.__filter.group_by_date(transactions)
        spendings_by_day_chart = _self.__chart.line(spendings_by_day, "Date", "Amount")

        hovertemplate = "<span style='color: #fff;'><span style='font-weight: 700;'>Day: %{x}</span>,<br>Amount: %{y:.2f} KM</span><extra></extra>"
        spendings_by_day_chart.update_traces(hovertemplate = hovertemplate)
        spendings_by_day_chart.layout.title = f"Spendings by Day in { _self.month_name }"

        planned = _self.__filter.spendings_statistics(_self.planned, transactions, _self.month_name,  False)

        _self.render(heatmap, transactions, spendings_by_day_chart, planned)


    def render(_self, heatmap: go.Figure, transactions: pd.DataFrame, spendings_by_day: go.Figure, planned: pd.DataFrame):
        
        st.plotly_chart(heatmap, use_container_width = True)

        with st.expander(f"Transactions for { _self.month_name }", expanded = False):
            st.dataframe(transactions)

        st.plotly_chart(spendings_by_day, use_container_width = True)

        st.dataframe(planned, use_container_width = True)

        _self.get_spendings_info_component(planned)

    