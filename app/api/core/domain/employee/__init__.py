from dataclasses import dataclass


@dataclass
class EmployeeInput:
    """
    社員の入力データを表すDTO。
    外部から社員情報を受け取る際に使用し、usecase層への入力型として機能する。
    """
    name: str
    role: str
    position: str
    department: str
    age: int
    hire_date: str


@dataclass
class EmployeeOutput:
    """
    社員の出力データを表すDTO。
    usecase層からpresentation層へ社員情報を渡す際に使用する。
    勤続年数（years_of_service）を含み、statusは含まない。
    """
    id: int
    name: str
    role: str
    position: str
    department: str
    age: int
    hire_date: str
    years_of_service: int
