import os
import pandas as pd
import streamlit as st

import gspread
from oauth2client.service_account import ServiceAccountCredentials


@st.cache(allow_output_mutation = True)
def fetch(sheet_type: str) ->  pd.DataFrame:

    SCOPES = os.environ.get("SCOPES").strip().split(",")
    CREDENTIALS_FILE_NAME = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    TRANSACTION_SHEET = os.environ.get("TRANSACTION_SHEET")
    
    credentials = ServiceAccountCredentials.from_json_keyfile_name(os.path.join(os.getcwd(),CREDENTIALS_FILE_NAME), SCOPES)
    client  = gspread.authorize(credentials)

    if sheet_type.lower() == "data":
        return pd.DataFrame(client.open(TRANSACTION_SHEET).sheet1.get_all_records())

    elif sheet_type.lower() == "static-data":
        return pd.DataFrame(client.open(TRANSACTION_SHEET).get_worksheet(2).get_all_records())

