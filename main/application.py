import os
import datetime
import pandas as pd
import streamlit as st

from .utils.repository import Repository

WORKBOOK = os.environ.get("WORKBOOK")


repository = Repository()

def run():

    transactions_data = repository.fetch(WORKBOOK, 0)

    from .sites.main.site import main_site
    main_site(transactions_data)





