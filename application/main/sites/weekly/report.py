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
WEEK = dt.date.today().isocalendar().week

hovertemplate = "<span style='color: #fff;'><span style='font-weight: 700;'>Day: %{x}</span>,<br>Amount: %{y:.2f} KM</span><extra></extra>"


class Weekly:

    def __init__(_self, repository: Repository, filter: Filter, chart: Chart, workbook: str):
        _self.__repository = repository
        _self.__filter = filter
        _self.__chart = chart
        _self.__workbook = workbook
        

    def get_required_container(_self, transactions: pd.DataFrame):
        actual_spendings = transactions["Amount"].sum()
        
        if(actual_spendings > 50):
            return st.error("{:.2f} / {}".format(actual_spendings, 50))
        return st.success("{:.2f} / {}".format(actual_spendings, 50))

    def planned_spendings_info_view(_self, transactions: pd.DataFrame) -> st.columns:
        planned_spending_container = st.columns([3, 1])
        planned_spending_container[0].info(f"Planned and Actual spendings for the week { WEEK }")

        with planned_spending_container[1]:
            _self.get_required_container(transactions)

        return planned_spending_container

    def report(_self, year: int = None, month: int = None, week: int = None) -> pd.DataFrame:
        data = _self.__repository.fetch(_self.__workbook, 0)
        planned = _self.__repository.fetch(_self.__workbook, 1)

        transactions = _self.__filter.filter_by_date(data, year = year, month = month, week = week)
        grouped = _self.__filter.group_by_category(transactions)

        with st.expander(f"All Transactions for Week { week } in { MONTHS[month] } ", expanded = False):
            st.dataframe(transactions, use_container_width = True)

        figure = _self.__chart.line(_self.__filter.group_by_date(transactions), "Date", "Amount")
        figure.update_traces(hovertemplate = hovertemplate)
        figure.layout.title = f"Spendings by Day for Week { week } in { MONTHS[month] }"
        st.plotly_chart(figure, use_container_width = True)

        category = st.container()
        category.markdown(f"<h6 style='text-align:left;'>Grouped Transactions by Category for { week } in { MONTHS[month] }</h6>", unsafe_allow_html = True)
        category.dataframe(grouped)

        planned = _self.__filter.spendings_statistics(planned, transactions, MONTHS[month], True)
        st.dataframe(planned)

        _self.planned_spendings_info_view(transactions)




