import streamlit as st
import pandas as pd
import datetime as dt

import plotly.express as px

from main.utils.filter import Filter
from main.utils.chart import Chart

from main.static.components.data import MONTHS

chart = Chart()
filter = Filter()
WEEK = dt.date.today().isocalendar().week

hovertemplate = "<span style='color: #fff;'><span style='font-weight: 700;'>Day: %{x}</span>,<br>Amount: %{y:.2f} KM</span><extra></extra>"


class Weekly:

    def get_required_container(_self, transactions: pd.DataFrame):
        actual_spendings = transactions["Amount"].sum()
        
        # Insted of 50, we want the value for the devidable categories devided by 4 (4 stands for the weeks in the month) 
        
        if(actual_spendings > 50):
            return st.error("{:.2f} / {}".format(actual_spendings, 50))
        return st.success("{:.2f} / {}".format(actual_spendings, 50))

    def planned_spendings_info_view(_self, transactions: pd.DataFrame) -> st.columns:
        planned_spending_container = st.columns([3, 1])
        planned_spending_container[0].info(f"Planned and Actual spendings for the week { WEEK }")

        with planned_spending_container[1]:
            _self.get_required_container(transactions)

        return planned_spending_container

    def report(_self, data: pd.DataFrame, year: int = None, month: int = None, week: int = None) -> pd.DataFrame:
        """
            Make sure that the data is a copy of the dataframe and not 
            the original object that is fetched from Google Sheets API.

            To do that on passing the `data` argument to the function add
            the pandas method copy() in front of it to make sure that the 
            DataFrame was in fact copied.
        """
        

        transactions = filter.filter_by_date(data, year = year, month = month, week = week)
        grouped = filter.group_by_category(transactions)

        with st.expander(f"All Transactions for Week { week } in { MONTHS[month] } ", expanded = False):
            st.dataframe(transactions, use_container_width = True)

        figure = chart.line(filter.group_by_date(transactions), "Date", "Amount")
        figure.update_traces(hovertemplate = hovertemplate)
        figure.layout.title = f"Spendings by Day for Week { week } in { MONTHS[month] }"
        st.plotly_chart(figure, use_container_width = True)

        category = st.container()

        category.markdown(f"<h6 style='text-align:left;'>Grouped Transactions by Category for { week } in { MONTHS[month] }</h6>", unsafe_allow_html = True)
        category.dataframe(grouped)

        _self.planned_spendings_info_view(transactions)


