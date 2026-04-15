from app.usecase.customers.list import ListCustomersUseCase, ListCustomersInput
from app.repository.customers.customer_repository import CustomerRepository


def test_list_customers_returns_all_customers():
    repository = CustomerRepository()
    use_case = ListCustomersUseCase(repository)

    output = use_case.execute(ListCustomersInput())

    assert len(output.customer_list) == 3


def test_list_customers_returns_correct_fields():
    repository = CustomerRepository()
    use_case = ListCustomersUseCase(repository)

    output = use_case.execute(ListCustomersInput())

    customer = output.customer_list[0]
    assert customer.id == 1
    assert customer.name == "山田太郎"
    assert customer.email == "yamada@example.com"


def test_list_customers_all_have_required_fields():
    repository = CustomerRepository()
    use_case = ListCustomersUseCase(repository)

    output = use_case.execute(ListCustomersInput())

    for customer in output.customer_list:
        assert customer.id is not None
        assert customer.name is not None
        assert customer.email is not None
