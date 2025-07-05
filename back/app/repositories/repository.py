import abc

class AbtractRepository(abc.ABC):
    @abc.abstractmethod
    def list(self):
        raise NotImplementedError
    
    @abc.abstractmethod
    def add(self, entity):
        raise NotImplementedError
    
    @abc.abstractmethod
    def get(self, identifier):    
        raise NotImplementedError
    
    @abc.abstractmethod
    def update(self, identifier, entity_data):
        raise NotImplementedError
    
    @abc.abstractmethod
    def delete(self, identifier):
        raise NotImplementedError