from app.repository.customers import Customer, ICustomerRepository


class CustomerRepository(ICustomerRepository):
    def __init__(self) -> None:
        self._customers: list[Customer] = [
            Customer(id=1, name="山田太郎", email="yamada@example.com"),
            Customer(id=2, name="鈴木花子", email="suzuki@example.com"),
            Customer(id=3, name="田中次郎", email="tanaka@example.com"),
        ]

    def list(self) -> list[Customer]:
        return self._customers
