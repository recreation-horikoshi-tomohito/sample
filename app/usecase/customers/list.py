from injector import inject
from app.repository.customers import ICustomerRepository
from app.usecase.customers import IListCustomersUseCase, ListCustomersInput, ListCustomersOutput, Customer


class ListCustomersUseCase(IListCustomersUseCase):
    @inject
    def __init__(self, repository: ICustomerRepository):
        self._repository = repository

    def execute(self, input: ListCustomersInput) -> ListCustomersOutput:
        customers = self._repository.list()

        if input.email:
            customers = [c for c in customers if c.email == input.email]

        # Customerオブジェクトのリストを作成
        customer_list = [
            Customer(id=c.id, name=c.name, email=c.email)
            for c in customers
        ]

        # ListCustomersOutput で包んで返す
        return ListCustomersOutput(customer_list=customer_list)
