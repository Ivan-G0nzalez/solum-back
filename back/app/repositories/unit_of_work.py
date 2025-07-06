import abc

from app.repositories.sql_client import sql_client
from app.repositories.clinic_repository import ClinicRepository
from app.repositories.call_repository import CallRepository
from app.repositories.evaluation_repository import EvaluationRepository

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

class UnitOfWork(AbstractUnitOfWork):
    def __init__(self):
        self.__session = sql_client.get_session()
        self.__clinic_repo = None
        self.__call_repo = None
        self.__evaluation_repo = None

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