from Task.Task import Task
from Employee.Employee import Employee

class TaskManager:
    def __init__(self) -> None:
        self.__current_task_id = 0
        self.__tasks = dict()

    def GetAllTasks(self):
        return self.__tasks

    def GetCurrentId(self) -> int:
        return self.__current_task_id

    def AddTask(self, task: Task) -> None:
        self.__current_task_id += 1
        self.__tasks[self.__current_task_id] = task

    def RemoveTask(self, task_id: int) -> None:
        del self.__tasks[task_id]

    def GetTaskById(self, task_id: int) -> Task:
        return self.__tasks[task_id]
    
    def AssignTaskTo(self, task_id: int, employee: Employee) -> None:
        self.__tasks[task_id].AddAssigner(employee)

    def ObserveTaskTo(self, task_id: int, employee: Employee) -> None:
        self.__tasks[task_id].AddObserver(employee)