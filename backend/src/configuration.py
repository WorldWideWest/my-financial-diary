import os

class BaseConfiguration(object):

    ENVIRONMENT = os.environ.get("ENVIRONMENT")

    POSTGRES_PORT = os.environ.get("POSTGRES_PORT")
    POSTGRES_USER = os.environ.get("POSTGRES_USER")
    POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
    POSTGRES_DB = os.environ.get("POSTGRES_DB")
    POSTGRES_HOST = os.environ.get("POSTGRES_HOST")


