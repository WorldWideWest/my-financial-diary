import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st



class Chart:

    @st.experimental_memo()
    def line(_self, data: pd.DataFrame, xaxis: str, yaxis: str) -> px.line:
        fig = px.line(data, x = xaxis, y = yaxis, markers = True)

        fig.data[0].line.color = "#FF800B"

        fig.update_layout(title_font_color = "#fff")

        fig.layout.plot_bgcolor = "rgba(0, 0, 0, 0)"
        fig.layout.paper_bgcolor = "rgba(0, 0, 0, 0)"

        fig.layout.yaxis.color = "#fff"
        fig.layout.xaxis.color = "#fff"

        fig.update_traces(
            marker = dict(size = 12, line = dict(width = 2, color = "#001024"))
        )

        return fig