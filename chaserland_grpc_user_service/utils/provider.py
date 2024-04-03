from abc import ABC, abstractmethod


class Provider(ABC):
    @staticmethod
    @abstractmethod
    def register(server):
        raise NotImplementedError
