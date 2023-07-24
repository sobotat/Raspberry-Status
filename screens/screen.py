from abc import ABC, abstractmethod

class Screen(ABC):

    @abstractmethod
    def update():
        pass

    @abstractmethod
    def activated():
        pass
    
    @abstractmethod
    def deactivated():
        pass