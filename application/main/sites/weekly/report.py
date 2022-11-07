import streamlit as st
import pandas as pd
import datetime as dt

import plotly.express as px

from main.utils.filter import Filter
from main.utils.chart import Chart
from main.db.repository import Repository

from main.static.components.data import MONTHS

chart = Chart()
filter = Filter()

hovertemplate = "<span style='color: #fff;'><span style='font-weight: 700;'>Day: %{x}</span>,<br>Amount: %{y:.2f} KM</span><extra></extra>"


class Weekly:

    def __init__(_self, repository: Repository, filter: Filter, chart: Chart, workbook: str):
        _self.__repository = repository
        _self.__filter = filter
        _self.__chart = chart
        _self.__workbook = workbook

    def set_year(_self, year: int):
        _self.year = year

    def set_month(_self, month: int):
        _self.month = month
        _self.set_month_name()

    def set_month_name(_self):
        _self.month_name = MONTHS[_self.month]

    def set_week(_self, week: int):
        _self.week = week

    def get_required_container(_self, data: pd.DataFrame, month: str):
        planned = data[month].sum()
        actual = data["Spent"].sum()

        text = "{:.2f} / {:.2f}".format(actual, planned)

        return st.error(text) if actual > planned else st.success(text)

    def planned_spendings_info_view(_self, data: pd.DataFrame) -> st.columns:
        planned_spending_container = st.columns([3, 1])
        planned_spending_container[0].info(f"Planned and Actual spendings for the week { _self.week } in { _self.month_name }")

        with planned_spending_container[1]:
            _self.get_required_container(data, _self.month)

        return planned_spending_container

    def report(_self) -> pd.DataFrame:
        data = _self.__repository.fetch(_self.__workbook, 0)
        planned = _self.__repository.fetch(_self.__workbook, 1)

        transactions = _self.__filter.filter_by_date(data, year = _self.year, month = _self.month, week = _self.week)
        grouped = _self.__filter.group_by_category(transactions)

        with st.expander(f"All Transactions for Week { _self.week } in { _self.month_name } ", expanded = False):
            st.dataframe(transactions, use_container_width = True)

        figure = _self.__chart.line(_self.__filter.group_by_date(transactions), "Date", "Amount")
        figure.update_traces(hovertemplate = hovertemplate)
        figure.layout.title = f"Spendings by Day for Week { _self.week } in { _self.month_name }"
        st.plotly_chart(figure, use_container_width = True)

        category = st.container()
        category.markdown(f"<h6 style='text-align:left;'>Grouped Transactions by Category for { _self.week } in { _self.month_name }</h6>", unsafe_allow_html = True)
        category.dataframe(grouped)

        planned = _self.__filter.spendings_statistics(planned, transactions, _self.month_name, True)
        st.dataframe(planned)

        _self.planned_spendings_info_view(planned)




