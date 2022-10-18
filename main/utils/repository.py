import os
import pandas as pd
import streamlit as st

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from main.configuration import BaseConfiguration


class Repository(BaseConfiguration):

    def fetch(self, index: int) ->  pd.DataFrame:

        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            os.path.join(os.getcwd(), self.CREDENTIALS_FILE_NAME), self.SCOPES)
        client  = gspread.authorize(credentials)

        data = client.open(self.TRANSACTION_SHEET).get_worksheet(index).get_all_records()

        return pd.DataFrame(data)



