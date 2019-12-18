from abc import ABC,abstractmethod

class IDataTransmitter(ABC):
    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass