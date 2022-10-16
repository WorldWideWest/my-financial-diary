import os
import pandas as pd
import streamlit as st

import gspread
from oauth2client.service_account import ServiceAccountCredentials

@st.cache
def fetch() ->  pd.DataFrame:
    SCOPES = os.environ.get("SCOPES").strip().split(",")
    CREDENTIALS_FILE_NAME = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    TRANSACTION_SHEET_NAME = os.environ.get("TRANSACTION_SHEET_NAME")


    credentials = ServiceAccountCredentials.from_json_keyfile_name(os.path.join(os.getcwd(),CREDENTIALS_FILE_NAME), SCOPES)
    client  = gspread.authorize(credentials)

    data = client.open(TRANSACTION_SHEET_NAME).sheet1.get_all_records()

    return pd.DataFrame(data)
