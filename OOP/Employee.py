class Salary:
    """
    Salary 클래스

    속성 : base_pay, bonus, overtime

    메서드:
        need:
            get_total():
                세전 월급
                base_pay + bonus + tax

            get_tax():
                근로자 세금: self.base_pay * 0.1
                ex: 37.0
            get_net():
                실수령액 : self.base_pay - self.get_tax()
                ex: 333

        maybe:
            get_base_pay
            get_bonus
            get_overtime

    """

    def __init__(self, base_pay: int, bonus: int, overtime: int):
        self.base_pay = max(base_pay, 0)
        self.bonus = max(bonus, 0)
        self.overtime = max(overtime, 0)

    def get_tax(self):
        return self.get_total() * 0.1

    def get_net(self):
        return self.get_total() - self.get_tax()

    def get_total(self):
        return self.base_pay + self.bonus + self.overtime

    def get_base_pay(self):
        return self.base_pay

    def get_bonus(self):
        return self.bonus

    def get_overtime(self):
        return self.overtime


class WorkHistory:
    def __init__(self, company, position, start_year, end_year):
        self.company = company
        self.position = position
        self.start_year = start_year
        self.end_year = end_year

    def get_years(self):
        return self.end_year - self.start_year

    def to_string(self):
        return f"{self.company} · {self.position} · {self.get_years()}년"


class Employee:
    """
    Employee 클래스

    속성 : name

    메서드:
        need:

            to_string():
                출력값: 이름  총액  세금  실수령액
                ex:     김민수  370  37.0  실수령액
    """

    def __init__(
        self,
        base_pay: int,
        bonus: int,
        overtime: int,
        name: str,
        dept: str,
        histories: list[WorkHistory] | None = None,
    ):
        self.salary = Salary(base_pay, bonus, overtime)
        self.name = name
        self.dept = dept
        # list[WorkHistory] 는 self.histories 이놈 타입
        self.histories: list[WorkHistory] = histories or []

    def get_career(self) -> int:
        return sum(h.get_years() for h in self.histories)

    def to_string(self) -> str:
        sal = self.salary

        career = f"{self.get_career()}년"
        return (
            f"{self.name:<{8 - len(self.name)}}"
            f"{self.dept:<{10 - len(self.dept)}}"
            f"{career:<5}"
            f"{sal.get_total():<8}{sal.get_tax():<8}{sal.get_net():<8}"
        )

    def to_string_old(self) -> str:
        sal = self.salary
        return (
            f"{self.name:<{8 - len(self.name)}}"
            f"{sal.get_total():<8}{sal.get_tax():<8}{sal.get_net():<8}"
        )

    def get_employee_total(self):
        return self.salary.get_total()

    def __del__(self):
        pass


class Department:
    def __init__(self, name, employees: list[Employee]):
        self.name = name
        self.employee = employees

    def add_employee(self, employee: Employee):
        self.employee.append(employee)

    def get_avg_career(self):
        return sum([x.get_career() for x in self.employee]) / len(self.employee)

    def get_payroll(self):
        return sum([x.get_employee_total() for x in self.employee])

    def print_members(self):
        print(f"{'이름':<6}{'부서':<8}{'경력':<4}{'총액':<6}{'세금':<6}{'실수령액':<4}")
        for emp in self.employee:
            print(emp.to_string())
        return

    def get_department_employee_count(self):
        return len(self.employee)


class Company:
    def __init__(self, name: str, department: list[Department]):
        self.name = name
        self.department = department

    def add_department(self, department: Department):
        self.department.append(department)

    def get_employee_count(self):
        return sum([x.get_department_employee_count() for x in self.department])

    def get_payroll(self):
        return sum([x.get_payroll() for x in self.department])

    def print_report(self):
        for x in self.department:
            x.print_members()
            print()

    def new_employee(
        self,
        name,
        salary: Salary,
        histories: list[WorkHistory] | None,
        department: str,
    ):
        emp = Employee(
            salary.base_pay, salary.bonus, salary.overtime, name, department, histories
        )

        for dept in self.department:
            if dept.name == department:
                dept.add_employee(emp)
                return

        self.add_department(Department(department, [emp]))
        return


company = Company("우리회사", [])

company.new_employee(
    "김민수",
    Salary(300, 50, 20),
    [WorkHistory("소프트웍스", "개발자", 2017, 2024)],
    "개발팀",
)
company.new_employee(
    "이지은",
    Salary(320, 40, 30),
    [WorkHistory("휴먼랩", "인사담당", 2020, 2024)],
    "인사팀",
)
company.new_employee("박준호", Salary(280, 60, 10), None, "영업팀")
company.new_employee(
    "최서연",
    Salary(350, 30, 25),
    [
        WorkHistory("데이터랩", "분석가", 2013, 2017),
        WorkHistory("클라우드원", "엔지니어", 2017, 2021),
        WorkHistory("넥스트AI", "리드", 2021, 2024),
    ],
    "개발팀",
)
company.new_employee(
    "한도윤",
    Salary(300, 70, 15),
    [WorkHistory("브랜드웍스", "마케터", 2021, 2024)],
    "마케팅팀",
)

company.print_report()
