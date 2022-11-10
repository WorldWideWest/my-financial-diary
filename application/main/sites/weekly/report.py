import streamlit as st
import pandas as pd
import datetime as dt

import plotly.express as px

from main.utils.filter import Filter
from main.utils.chart import Chart
from main.db.repository import Repository
from main.sites.base.base_report import BaseReport

class Weekly(BaseReport):

    def __init__(_self, repository: Repository, filter: Filter, chart: Chart, workbook: str):
        _self.__repository = repository
        _self.__filter = filter
        _self.__chart = chart
        _self.__workbook = workbook

        _self.get_data()
    
    def get_data(_self):
        _self.data = _self.__repository.fetch(_self.__workbook, 0)
        _self.planned = _self.__repository.fetch(_self.__workbook, 1)

    def get_required_container(_self, data: pd.DataFrame) -> dict:
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

    def get_filtered_transactions_dataframe(_self, transactions: pd.DataFrame):
        expander = st.expander(f"All Transactions for Week { _self.week } in { _self.month_name } ", expanded = False)
        expander.dataframe(transactions, use_container_width = True)
        
        return expander

    def get_spendings_by_day_chart(_self, transactions: pd.DataFrame):
        hovertemplate = "<span style='color: #fff;'><span style='font-weight: 700;'>Day: %{x}</span>,<br>Amount: %{y:.2f} KM</span><extra></extra>"

        figure = _self.__chart.line(transactions, "Date", "Amount")

        figure.update_traces(hovertemplate = hovertemplate)
        figure.layout.title = f"Spendings by Day for Week { _self.week } in { _self.month_name }"

        return st.plotly_chart(figure, use_container_width = True)

    def get_grouped_spendings_for_week_dataframe(_self, data: pd.DataFrame):
        container = st.container()
        container.markdown(f"<h6 style='text-align:left;'>Grouped Transactions by Category</br>for Week { _self.week } in { _self.month_name }</h6>", unsafe_allow_html = True)
        container.dataframe(data)

        return container

    def get_spending_statistics_dataframe(_self, statistics):
        return st.dataframe(statistics) 

    def process(_self) -> pd.DataFrame:
        transactions = _self.__filter.filter_by_date(_self.data, year = _self.year, month = _self.month, week = _self.week)
        grouped_by_category = _self.__filter.group_by_category(transactions)

        grouped_by_date = _self.__filter.group_by_date(transactions)        

        planned = _self.__filter.spendings_statistics(_self.planned, transactions, _self.month_name, True)
        
        _self.render(transactions, grouped_by_category, grouped_by_date, planned)

    def render(_self, transactions: pd.DataFrame, grouped_by_category: pd.DataFrame, grouped_by_date: pd.DataFrame, planned: pd.DataFrame):
        
        _self.get_filtered_transactions_dataframe(transactions)

        _self.get_spendings_by_day_chart(grouped_by_date)

        columns = st.columns([2, 2])
        with columns[0]:
            _self.get_grouped_spendings_for_week_dataframe(grouped_by_category)
        with columns[1]:
            _self.get_spending_statistics_dataframe(planned)

        _self.get_spendings_info_component(planned)






