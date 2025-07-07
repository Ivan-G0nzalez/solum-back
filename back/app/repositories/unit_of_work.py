import abc

from app.repositories.sql_client import sql_client
from app.repositories.clinic_repository import ClinicRepository
from app.repositories.call_repository import CallRepository
from app.repositories.evaluation_repository import EvaluationRepository
from app.repositories.user_repository import UserRepository

class AbstractUnitOfWork(abc.ABC):

    @abc.abstractmethod
    def clinics(self):
        pass
    
    @abc.abstractmethod
    def calls(self):
        pass
    
    @abc.abstractmethod
    def evaluations(self):
        pass
    
    @abc.abstractmethod
    def users(self):
        pass

class UnitOfWork(AbstractUnitOfWork):
    def __init__(self):
        self.__session = sql_client.get_session()
        self.__clinic_repo = None
        self.__call_repo = None
        self.__evaluation_repo = None
        self.__user_repo = None
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type is not None:
                # If there was an exception, rollback the transaction
                self.__session.rollback()
            else:
                # If no exception, commit the transaction
                self.__session.commit()
        except Exception as e:
            # If commit/rollback fails, try to rollback
            try:
                self.__session.rollback()
            except:
                pass
        finally:
            # Always close the session
            try:
                self.__session.close()
            except Exception as e:
                # Log but don't raise - session close errors shouldn't break the app
                pass

    def commit(self):
        """Manually commit the transaction"""
        self.__session.commit()

    def rollback(self):
        """Manually rollback the transaction"""
        self.__session.rollback()

    def close(self):
        """Close the session"""
        self.__session.close()

    @property
    def clinics(self):
        if self.__clinic_repo is None:
            self.__clinic_repo = ClinicRepository(self.__session)
        return self.__clinic_repo
    
    @property
    def calls(self):
        if self.__call_repo is None:
            self.__call_repo = CallRepository(self.__session)
        return self.__call_repo
    
    @property
    def evaluations(self):
        if self.__evaluation_repo is None:
            self.__evaluation_repo = EvaluationRepository(self.__session)
        return self.__evaluation_repo
    
    @property
    def users(self):
        if self.__user_repo is None:
            self.__user_repo = UserRepository(self.__session)
        return self.__user_repo