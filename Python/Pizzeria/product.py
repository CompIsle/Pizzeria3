from abc import ABC, abstractmethod

class IProduct(ABC):
    @property
    @abstractmethod
    def description(self) -> str:
        ...

    @abstractmethod
    def cost(self) -> float:
        ...
