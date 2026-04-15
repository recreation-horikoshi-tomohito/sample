from injector import Module

from app.repository.customers import ICustomerRepository
from app.repository.customers.customer_repository import CustomerRepository
from app.usecase.customers.list import IListCustomersUseCase, ListCustomersUseCase


class AppModule(Module):
    def configure(self, binder):
        binder.bind(ICustomerRepository, to=CustomerRepository)
        binder.bind(IListCustomersUseCase, to=ListCustomersUseCase)
