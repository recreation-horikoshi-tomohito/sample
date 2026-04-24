from datetime import date


class Employee:
    """
    社員エンティティ。ドメイン層の中核オブジェクト。
    IDを持つビジネスオブジェクトであり、勤続年数の計算などドメインロジックを担う。
    変換メソッドは持たず、usecase層でEmployeeOutputに変換する。
    """

    def __init__(self, id, name, role, position, department, age, hire_date):
        self.id = id
        self.name = name
        self.role = role
        self.position = position
        self.department = department
        self.age = age
        self.hire_date = hire_date

    @property
    def years_of_service(self):
        hired = date.fromisoformat(self.hire_date)
        today = date.today()
        return (today.year - hired.year) - (
            1 if (today.month, today.day) < (hired.month, hired.day) else 0
        )
