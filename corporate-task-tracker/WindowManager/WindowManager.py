import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
from TasksManager.TasksManager import TaskManager
from Task.Task import Task
from Employee.Employee import Employee
from Sprint.Sprint import Sprint
from SprintManager.SprintManager import SprintManager


class WindowManager(tk.Tk):    
    def __init__(self, root_title: str = "", root_geometry: str = "1200x800", is_main_window: int = False) -> None:
        self.__is_main_window = is_main_window
        
        super().__init__()

        self.title(root_title)
        self.geometry(root_geometry)

        self.task_manager = TaskManager()
        self.sprint_manager = SprintManager()

        self.padx = 10
        self.pady = 10

        self.add_task_window_scale_x = 3
        self.add_task_window_scale_y = 3

        self.default_button_color = "#efd982"
        self.click_button_color = "#a79032"

        self.columns_items = {"Id": 0, "Title": 1, "Description": 2, "Hours": 3, "Cost": 4, "Assigners": 5, "Observers": 6, "Status": 7}

        if self.__is_main_window:
            self.__CreateMainWindowWidgets()

    def UpdateWindow(self):
        self.mainloop()

    def __TaskValidator(self, title, description, estimated_hours, cost) -> bool:
        if not title or not description or not estimated_hours or not cost:
            messagebox.showerror("Error", "Fill all fields")
            return False
        
        try:
            float(estimated_hours)
            float(cost)
        except ValueError:
            messagebox.showerror("Error", "Estimated hours and Cost should be float numbers")
            return False
        
        return True

    def __CreateTask(self, add_task_window):
        title = add_task_window.title_entry.get()
        description = add_task_window.desc_entry.get()
        estimated_hours = add_task_window.time_entry.get()
        cost = add_task_window.cost_entry.get()
        
        if not self.__TaskValidator(title, description, estimated_hours, cost):
            add_task_window.destroy()
            return

        task = Task(title, description, float(estimated_hours), float(cost))
        
        try:
            self.task_list.insert("", "end", values=(self.task_manager.GetCurrentId() + 1, task.title, task.description, task.estimated_hours, task.cost, task.assigners, task.observers, task.status))
        except:
            messagebox.showerror("Error", "Unexpected error, try again")
            add_task_window.destroy()
        
        self.task_manager.AddTask(task)
        add_task_window.destroy()

    def __AddTaskButton(self):
        # ================================ Add Task Window And Widgets ================================ #
        add_task_window = WindowManager(root_geometry=str(int(self.winfo_width() / self.add_task_window_scale_x)) + "x" + str(int(self.winfo_height() / self.add_task_window_scale_y)) + "+" + str(self.winfo_x()) + "+" + str(self.winfo_y()))
        
        frame = tk.Frame(add_task_window, borderwidth=1, relief="solid", padx=self.padx, pady=self.pady)
        frame.pack(anchor="center", fill="both")

        add_task_window.title_entry = tk.Entry(frame)
        add_task_window.title_entry.insert(0, "Task Title")
        add_task_window.title_entry.pack(fill="both", padx=self.padx, pady=self.pady)

        add_task_window.desc_entry = tk.Entry(frame, textvariable="Task Description")
        add_task_window.desc_entry.insert(0, "Task Description")
        add_task_window.desc_entry.pack(fill="both", padx=self.padx, pady=self.pady)

        add_task_window.time_entry = tk.Entry(frame, textvariable="Task Estimated Hours")
        add_task_window.time_entry.insert(0, "Task Estimated Hours")
        add_task_window.time_entry.pack(fill="both", padx=self.padx, pady=self.pady)

        add_task_window.cost_entry = tk.Entry(frame, textvariable="Task Cost")
        add_task_window.cost_entry.insert(0, "Task Cost")
        add_task_window.cost_entry.pack(fill="both", padx=self.padx, pady=self.pady)

        # ================================ Create Task Button ================================ #
        add_task_window.create_task_button = tk.Button(frame, text="Create Task", font=("Ariel", 10), bg=self.default_button_color, command = lambda: self.__CreateTask(add_task_window))
        add_task_window.create_task_button.pack(fill="both", padx=self.padx, pady=self.pady)

        add_task_window.UpdateWindow()

    def __RemoveTaskButton(self):
        selected_item = self.task_list.selection()
        
        if len(selected_item) == 0:
            return
        
        task_id = self.task_list.item(selected_item)["values"][0]
        self.task_manager.RemoveTask(task_id)
        self.task_list.delete(selected_item)

    def __AddEmployee(self, add_employee_window, isAssigner = True):
        add_employee_window.employee = Employee(add_employee_window.employee_name.get(), add_employee_window.employee_surname.get())

        if not add_employee_window.employee.name and not add_employee_window.employee.surname:
            add_employee_window.destroy()
            messagebox.showerror("Error", "Fill one of the fields")
            return

        selected_item = self.task_list.selection()
        
        if len(selected_item) == 0:
            messagebox.showerror("Error", "Task was not selected")
            add_employee_window.destroy()
            return

        task_id = self.task_list.item(selected_item)["values"][0]

        if isAssigner:
            self.task_manager.AssignTaskTo(task_id, add_employee_window.employee)
        else:
            self.task_manager.ObserveTaskTo(task_id, add_employee_window.employee)

        employees_result = ""

        if isAssigner:
            for emp in self.task_manager.GetTaskById(task_id).assigners:
                employees_result += emp.name + " " + emp.surname + ';'
        else:
            for emp in self.task_manager.GetTaskById(task_id).observers:
                employees_result += emp.name + " " + emp.surname + ';'


        if isAssigner:
            self.task_list.item(selected_item, values=(self.task_list.item(selected_item, "values")[0], 
                                                    self.task_list.item(selected_item, "values")[1], 
                                                    self.task_list.item(selected_item, "values")[2], 
                                                    self.task_list.item(selected_item, "values")[3], 
                                                    self.task_list.item(selected_item, "values")[4], 
                                                    employees_result,
                                                    self.task_list.item(selected_item, "values")[6], 
                                                    self.task_list.item(selected_item, "values")[7]))
        else:
            self.task_list.item(selected_item, values=(self.task_list.item(selected_item, "values")[0], 
                                                    self.task_list.item(selected_item, "values")[1], 
                                                    self.task_list.item(selected_item, "values")[2], 
                                                    self.task_list.item(selected_item, "values")[3], 
                                                    self.task_list.item(selected_item, "values")[4], 
                                                    self.task_list.item(selected_item, "values")[5], 
                                                    employees_result,
                                                    self.task_list.item(selected_item, "values")[7]))

        add_employee_window.destroy()

    def __AddEmployeeButton(self, isAsigner = True):
        add_employee_window = WindowManager(root_geometry=str(int(self.winfo_width() / self.add_task_window_scale_x)) + "x" + str(int(self.winfo_height() / self.add_task_window_scale_y)) + "+" + str(self.winfo_x()) + "+" + str(self.winfo_y()))

        frame = tk.Frame(add_employee_window, borderwidth=1, relief="solid", padx=self.padx, pady=self.pady)
        frame.pack(anchor="center", fill="both")

        add_employee_window.employee_name = tk.Entry(frame)
        add_employee_window.employee_name.insert(0, "Employee Name")
        add_employee_window.employee_name.pack(fill="both", padx=self.padx, pady=self.pady)

        add_employee_window.employee_surname = tk.Entry(frame)
        add_employee_window.employee_surname.insert(0, "Employee Surname")
        add_employee_window.employee_surname.pack(fill="both", padx=self.padx, pady=self.pady)
        
        # ================================ Add Employee Button ================================ #
        add_employee_window.add_employee_button = tk.Button(frame, text="Add Employee", font=("Ariel", 10), bg=self.default_button_color, command = lambda: self.__AddEmployee(add_employee_window, isAsigner))
        add_employee_window.add_employee_button.pack(fill="both", padx=self.padx, pady=self.pady)

        add_employee_window.UpdateWindow()

    def __ChangeStatus(self, change_status_window):
        selected_item = self.task_list.selection()
        
        if len(selected_item) == 0:
            messagebox.showerror("Error", "Task was not selected")
            change_status_window.destroy()
            return
        
        self.task_list.item(selected_item, values=(self.task_list.item(selected_item, "values")[0], 
                                                    self.task_list.item(selected_item, "values")[1], 
                                                    self.task_list.item(selected_item, "values")[2], 
                                                    self.task_list.item(selected_item, "values")[3], 
                                                    self.task_list.item(selected_item, "values")[4], 
                                                    self.task_list.item(selected_item, "values")[5],
                                                    self.task_list.item(selected_item, "values")[6], 
                                                    change_status_window.combobox.get()))
        
        change_status_window.destroy()

    def __ChangeStatusButton(self):
        change_status_window = WindowManager(root_geometry=str(int(self.winfo_width() / self.add_task_window_scale_x)) + "x" + str(int(self.winfo_height() / self.add_task_window_scale_y)) + "+" + str(self.winfo_x()) + "+" + str(self.winfo_y()))

        frame = tk.Frame(change_status_window, borderwidth=1, relief="solid", padx=self.padx, pady=self.pady)
        frame.pack(anchor="center", fill="both")

        change_status_window.options = ["In Work", "Stopped", "Finished"]

        change_status_window.selected_option = tk.StringVar(frame)
        change_status_window.selected_option.set(change_status_window.options[0])
         
        change_status_window.combobox = ttk.Combobox(frame, textvariable=tk.StringVar(value=change_status_window.options[1]), values=change_status_window.options)
        change_status_window.combobox.pack(fill="both", padx=self.padx, pady=self.pady)

        # ================================ Change State Button ================================ #
        change_status_window.change_status_window = tk.Button(frame, text="Change Status", font=("Ariel", 10), bg=self.default_button_color, command = lambda: self.__ChangeStatus(change_status_window))
        change_status_window.change_status_window.pack(fill="both", padx=self.padx, pady=self.pady)

        change_status_window.UpdateWindow()

    def __CreateSprint(self, sprint_window):
        selected_indices = sprint_window.tasks_listbox.curselection()
        if not selected_indices:
            messagebox.showerror("Error", "Tasks were not selected")
            sprint_window.destroy()
            return
        
        selected_tasks = [self.task_manager.GetTaskById(index + 1) for index in selected_indices]
        
        start_date = sprint_window.start_date_entry.get()
        end_date = sprint_window.end_date_entry.get()

        if not start_date or not end_date:
            messagebox.showerror("Error", "Enter date")
            sprint_window.destroy()
            return

        try:
            start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
            end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Enter valid dates in YYYY-MM-DD format")
            sprint_window.destroy()
            return

        sprint = Sprint(selected_tasks, start_date, end_date)
        self.sprint_manager.AddSprint(sprint)

        sprint_info = f"Sprint created with {len(sprint.tasks)} tasks\n"
        sprint_info += f"Total Estimated Hours: {sprint.total_hours}\n"
        sprint_info += f"Start Date: {sprint.start_date}\n"
        sprint_info += f"End Date: {sprint.end_date}"


        tasks_titles = "; ".join([task.title for task in selected_tasks])
        self.sprint_list.insert("", "end", values=(tasks_titles, sprint.start_date, sprint.end_date))
        messagebox.showinfo("Sprint Created", sprint_info)
        
        sprint_window.destroy()

        return sprint

    def __CreateSprintButton(self):
        sprint_window = WindowManager(root_geometry=str(int(self.winfo_width() / self.add_task_window_scale_x)) + "x" + str(int(self.winfo_height())) + "+" + str(self.winfo_x()) + "+" + str(self.winfo_y()))
        
        frame = tk.Frame(sprint_window, borderwidth=1, relief="solid", padx=self.padx, pady=self.pady)
        frame.pack(anchor="center", fill="both")

        # ================================ Task Selection ================================ #
        sprint_window.selected_tasks = []
        sprint_window.tasks_listbox = tk.Listbox(frame, selectmode="multiple")
        
        for task in self.task_manager.GetAllTasks().values():
            sprint_window.tasks_listbox.insert(tk.END, task.title)

        sprint_window.tasks_listbox.pack(fill="both", padx=self.padx, pady=self.pady)

        # ================================ Sprint Dates ================================ #
        sprint_window.start_date_entry = tk.Entry(frame)
        sprint_window.start_date_entry.insert(0, "Start Date (YYYY-MM-DD)")
        sprint_window.start_date_entry.pack(fill="both", padx=self.padx, pady=self.pady)

        sprint_window.end_date_entry = tk.Entry(frame)
        sprint_window.end_date_entry.insert(0, "End Date (YYYY-MM-DD)")
        sprint_window.end_date_entry.pack(fill="both", padx=self.padx, pady=self.pady)

        # ================================ Create Sprint Button ================================ #
        sprint_window.create_sprint_button = tk.Button(frame, text="Create Sprint", font=("Ariel", 10), bg=self.default_button_color, command=lambda: self.__CreateSprint(sprint_window))
        sprint_window.create_sprint_button.pack(fill="both", padx=self.padx, pady=self.pady)

    def __ChangeButtonColor(self, button: tk.Button, color: str):
        button["bg"] = color

    def __CreateMainWindowWidgets(self):
        # ================================ Frame For Table ================================ #
        self.frame_table = tk.Frame(self, borderwidth=1, relief="solid", padx=self.padx, pady=self.pady)
        self.frame_table.pack()

        # ================================ Tasks Table ================================ #
        self.task_list = ttk.Treeview(self.frame_table, columns=("Id", "Title", "Description", "Hours", "Cost", "Assigners", "Observers", "Status"), show="headings")
        
        vsb = ttk.Scrollbar(self.frame_table, orient="vertical", command=self.task_list.yview)
        vsb.pack(side='right', fill='y')

        self.task_list.configure(yscrollcommand=vsb.set)

        hsb = ttk.Scrollbar(self.frame_table, orient="horizontal", command=self.task_list.xview)
        hsb.pack(side='bottom', fill='x')

        self.task_list.configure(yscrollcommand=vsb.set)

        self.task_list.heading("Id", text="Task Id")
        self.task_list.heading("Title", text="Task Title")
        self.task_list.heading("Description", text="Task Description")
        self.task_list.heading("Hours", text="Task Estimated Hours")
        self.task_list.heading("Cost", text="Task Cost")
        self.task_list.heading("Status", text="Task Status")
        self.task_list.heading("Assigners", text="Assigners")
        self.task_list.heading("Observers", text="Observers")

        self.task_list.pack(anchor="ne")

        # ================================ Add Tasks Button ================================ #
        self.add_task_button = tk.Button(self.frame_table, text="Add Task", font=("Ariel", 10), command=self.__AddTaskButton)
        self.__ChangeButtonColor(self.add_task_button, self.default_button_color)
        
        self.add_task_button.pack(fill="both")

        # ================================ Remove Tasks Button ================================ #
        self.remove_task_button = tk.Button(self.frame_table, text="Remove Task", font=("Ariel", 10), command=self.__RemoveTaskButton)
        self.__ChangeButtonColor(self.remove_task_button, self.default_button_color)
        
        self.remove_task_button.pack(fill="both")

        # ================================ Add Asigner Button ================================ #
        self.add_assigner_button = tk.Button(self.frame_table, text="Add Assigner To Selected Task", font=("Ariel", 10), command=self.__AddEmployeeButton)
        self.__ChangeButtonColor(self.add_assigner_button, self.default_button_color)
        
        self.add_assigner_button.pack(fill="both")

        # ================================ Add Observer Button ================================ #
        self.add_observer_button = tk.Button(self.frame_table, text="Add Observer To Selected Task", font=("Ariel", 10), command= lambda: self.__AddEmployeeButton(False))
        self.__ChangeButtonColor(self.add_observer_button, self.default_button_color)
        
        self.add_observer_button.pack(fill="both")

        # ================================ Change Status Button ================================ #
        self.change_status_button = tk.Button(self.frame_table, text="Change Status For Selected Task", font=("Ariel", 10), command=self.__ChangeStatusButton)
        self.__ChangeButtonColor(self.change_status_button, self.default_button_color)
        
        self.change_status_button.pack(fill="both")

        # ================================ Frame For Sprint ================================ #
        self.frame_sprint = tk.Frame(self, borderwidth=1, relief="solid", padx=self.padx, pady=self.pady)
        self.frame_sprint.pack()

        # ================================ Create Sprint Button ================================ #
        self.create_sprint_button = tk.Button(self.frame_table, text="Create Sprint", font=("Ariel", 10), command=self.__CreateSprintButton)
        self.__ChangeButtonColor(self.create_sprint_button, self.click_button_color)
        self.create_sprint_button.pack(fill="both")

        columns = ("Tasks", "Start", "End")
        self.sprint_list = ttk.Treeview(self.frame_sprint, columns=columns, show="headings")

        self.sprint_list.heading("Tasks", text="Sprint Tasks")
        self.sprint_list.heading("Start", text="Start Date")
        self.sprint_list.heading("End", text="End Date")

        self.sprint_list.pack(fill="both", expand=True)

        vsb = ttk.Scrollbar(self.frame_sprint, orient="vertical", command=self.sprint_list.yview)
        vsb.pack(side='right', fill='y')

        self.task_list.configure(yscrollcommand=vsb.set)

        hsb = ttk.Scrollbar(self.frame_sprint, orient="horizontal", command=self.sprint_list.xview)
        hsb.pack(side='bottom', fill='x')