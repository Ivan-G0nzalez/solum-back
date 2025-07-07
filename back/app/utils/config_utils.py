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
    
    @staticmethod
    def get_jwt_secret_key():
        return os.getenv('JWT_SECRET_KEY', '09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7')
    
    @staticmethod
    def get_jwt_algorithm():
        return os.getenv('JWT_ALGORITHM', 'HS256')
    
    @staticmethod
    def get_jwt_access_token_expire_minutes():
        return int(os.getenv('JWT_ACCESS_TOKEN_EXPIRE_MINUTES', '30'))

    