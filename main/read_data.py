import os
import json
import pandas as pd

import gspread
from oauth2client.service_account import ServiceAccountCredentials


SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets",
]

credentials_file = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

print()

credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, SCOPES)

client  = gspread.authorize(credentials)


data = client.open("Personal Budget Planner").sheet1.get_all_records()

dataFrame = pd.DataFrame(data)

print(dataFrame)