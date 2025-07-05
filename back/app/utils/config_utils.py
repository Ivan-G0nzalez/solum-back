import os

from dotenv import load_dotenv

load_dotenv()


class DatabaseConfig:
    """Stub for database configuration. Replace with your actual implementation."""
    @staticmethod
    def get_type() -> str:
        # Could be "postgres" or "sql_server"
        return os.getenv("DB_TYPE", "postgres")

    @staticmethod
    def get_username() -> str:
        return os.getenv("DB_USER", "your_user")

    @staticmethod
    def get_password() -> str:
        return os.getenv("DB_PASSWORD", "your_password")

    @staticmethod
    def get_server() -> str:
        return os.getenv("DB_HOST", "localhost")

    @staticmethod
    def get_port() -> str:
        return os.getenv("DB_PORT", "5432")

    @staticmethod
    def get_database() -> str:
        return os.getenv("DB_NAME", "your_db")

    @staticmethod
    def get_driver() -> str:
        return os.getenv("DB_DRIVER", "{ODBC Driver 17 for SQL Server}")


class GlobalConfig:
    @staticmethod
    def get_ui_path():
        return os.getenv('BASE_FRONTEND_URL')
    
    @staticmethod
    def get_log_path():
        return os.getenv('PATH_LOGGER_FILES')
    
    @staticmethod
    def get_log_filename():
        return os.getenv('LOG_FILENAME')

    