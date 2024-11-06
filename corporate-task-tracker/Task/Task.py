from Employee.Employee import Employee

class Task:
    def __init__(self, title: str, description: str, estimated_hours: int = 0, cost: int = 0, assigners: list = None, observers: list = None, status : str = "In Work"):
        self.title = title
        self.description = description
        self.estimated_hours = estimated_hours
        self.cost = cost
        self.assigners = assigners if assigners else []
        self.observers = observers if observers else []
        self.status = status

    def AddAssigner(self, employee: Employee) -> None:
        self.assigners.append(employee)

    def AddObserver(self, employee: Employee) -> None:
        self.observers.append(employee)