from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Customer:
    id: int
    name: str
    email: str


class ICustomerRepository(ABC):
    @abstractmethod
    def list(self) -> list[Customer]:
        raise NotImplementedError
