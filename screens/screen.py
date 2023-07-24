from abc import ABC, abstractmethod

class Screen(ABC):

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def activated(self):
        pass
    
    @abstractmethod
    def deactivated(self):
        pass