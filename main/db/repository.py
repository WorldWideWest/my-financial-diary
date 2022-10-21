import pandas as pd
import streamlit as st

import gspread
from gspread.exceptions import WorksheetNotFound

from oauth2client.service_account import ServiceAccountCredentials

from main.configuration import BaseConfiguration
from main.db.models.base import BaseModel
from main.db.models.income import IncomeModel


class Repository(BaseConfiguration):
    """
        Repository class is used as a mimic to a real repositrory class like in SQLAlchemy but in our case the 
        database is Google Sheets and it is accessed through the Google Cloud Platform [API](https://console.cloud.google.com/marketplace/product/google/sheets.googleapis.com?q=search&referrer=search&project=personal-budget-diary).

        The Repository class inherites from the BaseConfiguration class which containse our environment variables which are defined in the .env file or are exported in the system itself.

        To authenticate with GCP we use the custom dunder method `__authenticate__` which populates our `__client` property which will be used through out the class to give us read/write functionality to Google Sheets.

    """
    __client = None

    def __init__(self) -> None:
        self.__authenticate__()
        super().__init__()

    def __authenticate__(self):
        try:
            credentials = ServiceAccountCredentials.from_json_keyfile_name(
                self.CREDENTIALS_FILE_NAME, self.SCOPES)

            self.__client  = gspread.authorize(credentials)
        except Exception as e:
            print(f"Authentication failure: { str(e.args) }")
            
    @st.cache()
    def fetch(self, workbook: str, index: int) ->  pd.DataFrame:
        """
            The `fetch()` method is the prt of the Repository class which mimics a real
            repositorty. In our case the database is Google Sheets which is accessed through the Google Cloud Platform [API](https://console.cloud.google.com/marketplace/product/google/sheets.googleapis.com?q=search&referrer=search&project=personal-budget-diary).
            
            The input parameter `index` is used to access the sheet in the Google Sheet Workbook and `it starts counting from 0`.
            Also the method contains the `st.cache` decorator to cash the data from the first call to the API.

            The return of this method is a pandas DataFrame which contains records from the requsted worksheet.
        """
        try:
            data = self.__client.open(workbook).get_worksheet(index).get_all_records()
            return pd.DataFrame(data)
        except Exception as e:
            print(f"Fetch failure: { str(e) }")


    def migrate(self, workbook_name: str, model: BaseModel, index = -1):
        try:    

            columns = [column for column in model.columns() if column != "table_name"]
            workbook = self.__client.open(workbook_name)

            
            if isinstance(self.try_open(workbook_name, model.table_name), WorksheetNotFound):
                workbook.add_worksheet(model.table_name, 0, 0)

            worksheet = workbook.worksheet(model.table_name)
            if len(worksheet.get_all_records()) == 0:
                for x, value in enumerate(columns):
                    worksheet.update_cell(1, x + 1, value)
                

            return
        except Exception as e:
            print(e)

    def try_open(self, workbook: str, worksheet: str):
        try:
            self.__client.open(workbook).worksheet(worksheet)
        except WorksheetNotFound as e:
            return e