import os
import urllib.parse
from sqlalchemy import create_engine
from app.utils.config_utils import DatabaseConfig
from sqlalchemy.orm import sessionmaker
from app.utils.logger import logger

class ConnectionStringBuilder:
    @staticmethod
    def get_default_connection_string() -> str:
        db_type = DatabaseConfig.get_type().lower()

        if db_type == "postgres":
            user = DatabaseConfig.get_username()
            password = DatabaseConfig.get_password()
            host = DatabaseConfig.get_server()
            port = DatabaseConfig.get_port()
            database = DatabaseConfig.get_database()
            return f"postgresql://{user}:{password}@{host}:{port}/{database}"

        elif db_type == "sql_server":
            connection_attributes = urllib.parse.quote_plus(
                f"DRIVER={DatabaseConfig.get_driver()};"
                f"SERVER={DatabaseConfig.get_server()};"
                f"DATABASE={DatabaseConfig.get_database()};"
                f"UID={DatabaseConfig.get_username()};"
                f"PWD={DatabaseConfig.get_password()};"
            )
            return f"mssql+pyodbc:///?odbc_connect={connection_attributes}"

        else:
            raise ValueError(f"Unsupported database type: {db_type}")

class SQLClient:
    def __init__(self, url=ConnectionStringBuilder.get_default_connection_string()):
        try:
            engine = create_engine(url, echo=True)
            self.__session = sessionmaker(
                autocommit=False, autoflush=False, bind=engine)
        except Exception as e:
            logger.error(
                f"Error trying to connect to the Database. error: {e}")
            raise

    def get_session(self):
        return self.__session()

sql_client = SQLClient()