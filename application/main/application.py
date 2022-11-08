import os
import datetime
import pandas as pd
import streamlit as st

from .db.repository import Repository
from .db.models.income import IncomeModel
from .configuration import BaseConfiguration

WORKBOOK = os.environ.get("WORKBOOK")


repository = Repository()

def run():

    transactions_data = repository.fetch(WORKBOOK, 0)
    planning_data = repository.fetch(WORKBOOK, 1)

    from .sites.main.site import main_site
    main_site(transactions_data, planning_data)
    




