from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class ListCustomersInput:
    email: str | None = None


@dataclass
class Customer:
    id: int
    name: str
    email: str

@dataclass
class ListCustomersOutput:
    customer_list: list[Customer]


class IListCustomersUseCase(ABC):
    @abstractmethod
    def execute(self, input: ListCustomersInput) -> ListCustomersOutput:
        raise NotImplementedError
