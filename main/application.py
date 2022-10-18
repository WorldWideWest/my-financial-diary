import datetime
import pandas as pd
import streamlit as st

from .utils.repository import Repository


repository = Repository()

@st.cache
def run():

    transactions_data = repository.fetch(0)

    from .sites.main.site import main_site
    main_site(transactions_data)





