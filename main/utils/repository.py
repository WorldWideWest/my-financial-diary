import os
import pandas as pd
import streamlit as st

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from main.configuration import BaseConfiguration


class Repository(BaseConfiguration):
    
    @st.cache()
    def fetch(self, index: int) ->  pd.DataFrame:
        """
            The `fetch()` method is the prt of the Repository class which mimics a real
            repositorty. In our case the database is Google Sheets which is accessed through the Google Cloud Platform [API](https://console.cloud.google.com/marketplace/product/google/sheets.googleapis.com?q=search&referrer=search&project=personal-budget-diary).
            
            The input parameter `index` is used to access the sheet in the Google Sheet Workbook and `it starts counting from 0`.
            Also the method contains the `st.cache` decorator to cash the data from the first call to the API.

            The return of this method is a pandas DataFrame which contains records from the requsted worksheet.
        """


        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            os.path.join(os.getcwd(), self.CREDENTIALS_FILE_NAME), self.SCOPES)
        client  = gspread.authorize(credentials)

        data = client.open(self.TRANSACTION_SHEET).get_worksheet(index).get_all_records()

        return pd.DataFrame(data)

    



