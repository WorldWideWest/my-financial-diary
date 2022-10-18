import os

class BaseConfiguration:
    SCOPES = os.environ.get("SCOPES").strip().split(",")
    CREDENTIALS_FILE_NAME = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    TRANSACTION_SHEET = os.environ.get("TRANSACTION_SHEET")