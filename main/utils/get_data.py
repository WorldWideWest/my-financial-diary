import os
import pandas as pd
import streamlit as st

import gspread
from oauth2client.service_account import ServiceAccountCredentials


@st.cache(allow_output_mutation = True)
def fetch(index: int) ->  pd.DataFrame:

    SCOPES = os.environ.get("SCOPES").strip().split(",")
    CREDENTIALS_FILE_NAME = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    TRANSACTION_SHEET = os.environ.get("TRANSACTION_SHEET")
    
    credentials = ServiceAccountCredentials.from_json_keyfile_name(os.path.join(os.getcwd(),CREDENTIALS_FILE_NAME), SCOPES)
    client  = gspread.authorize(credentials)

    return pd.DataFrame(client.open(TRANSACTION_SHEET).get_worksheet(index).get_all_records())



