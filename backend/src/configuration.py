import os

class BaseConfiguration(object):
    def __init__(self) -> None:
        
        self.set_connection_string()

    ENVIRONMENT = os.environ.get("ENVIRONMENT")

    DB_DIALECT = os.environ.get("DB_DIALECT")
    DB_DRIVER = os.environ.get("DB_DRIVER")
    DB_USER = os.environ.get("DB_USER")
    DB_PASSWORD = os.environ.get("DB_USER")
    DB_HOST = os.environ.get("DB_HOST")
    DB_PORT = os.environ.get("DB_PORT")
    DB_NAME = os.environ.get("DB_NAME")

    def set_connection_string(self) -> None:
        self.SQLALCHEMY_DATABASE_URL = f"{ self.DB_DIALECT }+{ self.DB_DRIVER }://{ self.DB_USER }:{ self.DB_PASSWORD }@{ self.DB_HOST }:{ self.DB_PORT }/{ self.DB_NAME }"
