from app.repository.customers import Customer, ICustomerRepository


class CustomerRepository(ICustomerRepository):
    def __init__(self) -> None:
        self._customers = [
            Customer(id=1, name="Alice", email="alice@example.com"),
            Customer(id=2, name="Bob", email="bob@example.com"),
            Customer(id=3, name="Charlie", email="charlie@example.com"),
        ]

    def list(self) -> list[Customer]:
        return self._customers
