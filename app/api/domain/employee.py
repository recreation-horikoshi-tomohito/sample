from datetime import date


class Employee:
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

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "role": self.role,
            "position": self.position,
            "department": self.department,
            "age": self.age,
            "hire_date": self.hire_date,
            "years_of_service": self.years_of_service,
        }
