from src.configuration import BaseConfiguration

"""
from sqlalchemy import URL

engine = create_engine("postgresql+psycopg2://scott:tiger@localhost/mydatabase")

)
"""
class DbConfig(BaseConfiguration):


    def get_connection_string(self):
        return f"postgresql+psycopg2://{ self.POSTGRES_USER }:{ self.POSTGRES_PASSWORD }@{ self.POSTGRES_HOST }/{ self.POSTGRES_DB }"



