import json
import os

# Node class for Linked List
class EmployeeNode:
    def __init__(self, name, details):
        self.name = name
        self.details = details  # Details is a list containing [qualification, skills]
        self.next = None  # Pointer to the next node

# Linked List class for Employees
class EmployeeLinkedList:
    def __init__(self):
        self.head = None

    def add_employee(self, name, details):
        new_node = EmployeeNode(name, details)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def display_employees(self):
        current = self.head
        if not current:
            print("Currently No Employees")
            return
        print("Current Employees:")
        while current:
            print("Employee Name: ", current.name)
            print("Qualification: ", current.details[0])
            print("Skills: ", current.details[1])
            current = current.next

    def delete_employee(self, name):
        current = self.head
        prev = None
        while current:
            if current.name == name:
                if prev:
                    prev.next = current.next
                else:
                    self.head = current.next
                return True
            prev = current
            current = current.next
        return False

    def load_from_file(self, file_path):
        if os.path.exists(file_path):
            with open(file_path, "r") as fd:
                if os.path.getsize(file_path) == 0:
                    return
                try:
                    employees = json.load(fd)
                    for name, details in employees.items():
                        self.add_employee(name, details)
                except json.JSONDecodeError:
                    print("Error: Hired employees file is corrupted or contains invalid JSON.")

    def save_to_file(self, file_path):
        employees_dict = {}
        current = self.head
        while current:
            employees_dict[current.name] = current.details
            current = current.next
        with open(file_path, "w") as fd:
            json.dump(employees_dict, fd)

def view_employees(employee_list):
    employee_list.display_employees()

def hire_employees(employee_list):
    application_file = "data/employees_application.txt"
    
    if not os.path.exists(application_file):
        print("No employee applications found.")
        return

    with open(application_file, "r+") as ed:
        if os.path.getsize(application_file) == 0:
            print("No employee applications to process.")
            return

        try:
            applications = json.load(ed)
        except json.JSONDecodeError:
            print("Error: Employees application file is corrupted or contains invalid JSON.")
            return

        view_applications()

        if not applications:
            print("No applications available.")
            return
        
        employee_name = input("Enter Employee Name to Accept or Reject Application: ").strip()
        normalized_applications = {name.lower(): name for name in applications.keys()}
        
        if employee_name.lower() in normalized_applications:
            actual_name = normalized_applications[employee_name.lower()]
            decision = input("Enter 1 to Accept and -1 to Reject: ")
            if decision == '1':
                print(f"{actual_name} has been accepted.")
                employee_list.add_employee(actual_name, applications[actual_name])
                del applications[actual_name]  
                ed.seek(0)
                ed.truncate()
                json.dump(applications, ed)
            elif decision == '-1':
                print(f"{actual_name} has been rejected.")
                del applications[actual_name]  
                ed.seek(0)
                ed.truncate()
                json.dump(applications, ed)
            else:
                print("Invalid input, please enter 1 or -1.")
        else:
            print("Employee not found in the application list.")

def fire_employees(employee_list):
    hired_file_path = "data/hired_employees.txt"
    
    if not os.path.exists(hired_file_path):
        print("No employees found.")
        return

    employee_list.load_from_file(hired_file_path)

    while True:
        name = input("Enter Employee Name to Fire (or press Enter to cancel): ").strip()
        
        if not name:  
            print("Fire employee canceled.")
            return
        
        if employee_list.delete_employee(name):
            employee_list.save_to_file(hired_file_path)
            print("\nEmployee Fired Successfully")
            break
        else:
            print("Invalid Name, Try Again")

def view_applications():
    application_file = "data/employees_application.txt"
    index_file = "data/employees_applicationindex.txt"
    
    with open(application_file, "a+") as fd:
        with open(index_file, "a+") as id:
            id.seek(0)
            index = int(id.read())
            if index == 0:
                print("No Applications")
            else:
                fd.seek(0)
                data = json.load(fd)
                for key, value in data.items():
                    print("\nEmployee Name: ", key)
                    print("Qualification: ", value[0])
                    print("Skills: ", value[1])

def manage_employees():
    employee_list = EmployeeLinkedList()
    employee_list.load_from_file("data/hired_employees.txt")

    while True:
        print("1. View Employees")
        print("2. Hire Employees")
        print("3. Fire Employees")
        print("4. View Applications")
        print("5. Exit")
        choice = int(input("Enter choice: "))
        if choice == 1:
            view_employees(employee_list)
        elif choice == 2:
            hire_employees(employee_list)
        elif choice == 3:
            fire_employees(employee_list)
        elif choice == 4:
            view_applications()
        elif choice == 5:
            break
        else:
            print("Invalid choice. TRY AGAIN")