class Sprint:
    def __init__(self, tasks, start_date, end_date):
        self.tasks = tasks
        self.start_date = start_date
        self.end_date = end_date
        self.total_hours = sum(task.estimated_hours for task in tasks)