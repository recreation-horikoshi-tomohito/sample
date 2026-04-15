from abc import ABC, abstractmethod
from dataclasses import dataclass

from injector import inject

from app.repository.customers import Customer, ICustomerRepository


@dataclass
class ListCustomersInput:
    pass


@dataclass
class ListCustomersOutput:
    customers: list[Customer]


class IListCustomersUseCase(ABC):
    @abstractmethod
    def execute(self, input: ListCustomersInput) -> ListCustomersOutput:
        ...


class ListCustomersUseCase(IListCustomersUseCase):
    @inject
    def __init__(self, repository: ICustomerRepository) -> None:
        self._repository = repository

    def execute(self, input: ListCustomersInput) -> ListCustomersOutput:
        customers = self._repository.list()
        return ListCustomersOutput(customers=customers)
