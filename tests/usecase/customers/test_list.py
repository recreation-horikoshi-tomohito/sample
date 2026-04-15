from app.usecase.customers.list import ListCustomersUseCase, ListCustomersInput
from app.repository.customers.customer_repository import CustomerRepository


def test_list_customers_returns_all_customers():
    repository = CustomerRepository()
    use_case = ListCustomersUseCase(repository)

    output = use_case.execute(ListCustomersInput())

    assert len(output.customers) == 3


def test_list_customers_returns_correct_fields():
    repository = CustomerRepository()
    use_case = ListCustomersUseCase(repository)

    output = use_case.execute(ListCustomersInput())

    customer = output.customers[0]
    assert customer.id == 1
    assert customer.name == "Alice"
    assert customer.email == "alice@example.com"


def test_list_customers_all_have_required_fields():
    repository = CustomerRepository()
    use_case = ListCustomersUseCase(repository)

    output = use_case.execute(ListCustomersInput())

    for customer in output.customers:
        assert customer.id is not None
        assert customer.name is not None
        assert customer.email is not None
