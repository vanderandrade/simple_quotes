import abc

class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add(self, quote):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, reference):
        raise NotImplementedError

    @abc.abstractmethod
    def get_all(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_quotes(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_quoters(self):
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, reference):
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, reference):
        raise NotImplementedError