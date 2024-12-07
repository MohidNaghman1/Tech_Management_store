import json
import os
from Product_manage import view_products  # Assuming this function is defined in product_management.py

class ProductNode:
    def __init__(self, serial, data):
        self.serial = serial
        self.data = data  # Data is a list containing [name, description, price, quantity]
        self.next = None

class ProductLinkedList:
    def __init__(self):
        self.head = None

    def add_product(self, serial, data):
        new_node = ProductNode(serial, data)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def load_from_file(self, file_path):
        if os.path.exists(file_path):
            with open(file_path, "r") as fd:
                if os.path.getsize(file_path) == 0:
                    return
                try:
                    products = json.load(fd)
                    for serial, details in products.items():
                        self.add_product(serial, details)
                except json.JSONDecodeError:
                    print("Error: Product file is corrupted or contains invalid JSON.")


def view_products():
    # Check if the product file exists
        if not os.path.exists("data/products.txt"):
            print("Products file does not exist.")
            return

        # Open the products file in read mode
        with open("data/products.txt", "r") as pd:
            try:
                products = json.load(pd)

                if not products:
                    print("Store is Empty")
                    return

                for serial, value in products.items():
                    print("\n\nSerial Number: ", serial)
                    print("Product Name: ", value[0])
                    print("Description: ", value[1])
                    print("Price: $", value[2])
                    print("Quantity: ", value[3])
            except json.JSONDecodeError:
                print("Error: Unable to read products. The file may be corrupted or empty.")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
def buy_product():
    # Initialize necessary files and read products
    files_to_initialize = [
        ("data/products.txt", "{}"),
        ("data/sales.txt", "{}"),
        ("data/productsindex.txt", "0"),
        ("data/salesindex.txt", "0")
    ]
    
    for file_path, initial_content in files_to_initialize:
        if not os.path.exists(file_path):
            with open(file_path, "w") as f:
                f.write(initial_content)

    product_list = ProductLinkedList()
    product_list.load_from_file("data/products.txt")

    # Check for available products
    current = product_list.head
    if not current:
        print("No products available.")
        return

    total_bill = 0  # Initialize total bill
    view_products()  # Display available products

    # Processing purchases
    while True:
        serial = input("Enter Product Serial Number: ")
        current = product_list.head
        while current:
            if current.serial == serial:
                while True:
                    try:
                        quantity = int(input("Enter Quantity: "))
                    except ValueError:
                        print("Please enter a valid number for quantity.")
                        continue

                    original_quantity = int(current.data[3])

                    if original_quantity == 0:
                        print("Out of Stock")
                        return

                    if quantity <= original_quantity:
                        product_price = float(current.data[2])  # Convert price to float
                        order_price = product_price * quantity
                        total_bill += order_price  # Update the total bill

                        # Read sales index
                        with open("data/salesindex.txt", "r+") as si:
                            sales_index_content = si.read().strip()
                            sales_index = int(sales_index_content) if sales_index_content else 0

                            # Update sales dictionary
                            with open("data/sales.txt", "r") as sd:
                                salesdict = json.load(sd) if os.path.getsize("data/sales.txt") > 0 else {}
                            
                            saleslist = [current.data[0], quantity, product_price]
                            sales_index += 1
                            salesdict[sales_index] = saleslist

                        # Write back the updated sales and sales index
                        with open("data/sales.txt", "w") as sd:
                            json.dump(salesdict, sd)

                        # Update product quantity
                        current.data[3] = original_quantity - quantity

                        # Write back the updated products
                        products = {}
                        current_node = product_list.head
                        while current_node:
                            products[current_node.serial] = current_node.data
                            current_node = current_node.next
                        with open("data/products.txt", "w") as fd:
                            json.dump(products, fd)

                        # Update sales index
                        with open("data/salesindex.txt", "w") as si:
                            si.write(str(sales_index))

                        print("\nThanks for Shopping")
                        print(f"Total Bill: ${total_bill:.2f}")  # Print total bill
                        return  # Exit after successful purchase
                    else:
                        print("Not enough Stock, Try Again")
                break
            current = current.next
        print("Invalid Serial Number")

def customer():
    while True:
        print("\nWelcome to Mohid Tech Store")
        print("1. View Products")
        print("2. Start Shopping")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            view_products()  # Call the function to view products
        elif choice == '2':
            buy_product()  # Call the function to start shopping
        elif choice == '3':
            print("Thank you for visiting!")
            break
        else:
            print("Invalid choice, please try again.")

class EmployeeApplicationNode:
    def __init__(self, name, details):
        self.name = name
        self.details = details  # Details is a list containing [qualification, skills]
        self.next = None

class EmployeeApplicationLinkedList:
    def __init__(self):
        self.head = None

    def add_application(self, name, details):
        new_node = EmployeeApplicationNode(name, details)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def load_from_file(self, file_path):
        if os.path.exists(file_path):
            with open(file_path, "r") as fd:
                if os.path.getsize(file_path) == 0:
                    return
                try:
                    applications = json.load(fd)
                    for name, details in applications.items():
                        self.add_application(name, details)
                except json.JSONDecodeError:
                    print("Error: Applications file is corrupted or contains invalid JSON.")

def employees():
    application_list = EmployeeApplicationLinkedList()
    application_list.load_from_file("data/employees_application.txt")

    while True:
        print("1. Apply for Job")
        print("2. Withdraw Proposal")
        print("3. Exit")
        choice = int(input("Enter choice: "))
        if choice == 1:
            name = input("Enter Name: ")
            qualification = input("Enter Qualifications: ")
            skills = input("Enter Skills: ")
            listdata = [qualification, skills]
            application_list.add_application(name, listdata)

            # Update the applications file
            applications = {}
            current = application_list.head
            while current:
                applications[current.name] = current.details
                current = current.next
            with open("data/employees_application.txt", "w") as fd:
                json.dump(applications, fd)

        elif choice == 2:
            name = input("Enter name to withdraw: ")
            current = application_list.head
            previous = None
            found = False

            while current:
                if current.name == name:
                    if previous:
                        previous.next = current.next
                    else:
                        application_list.head = current.next
                    found = True
                    break
                previous = current
                current = current.next
            
            if found:
                # Update the applications file
                applications = {}
                current = application_list.head
                while current:
                    applications[current.name] = current.details
                    current = current.next
                with open("data/employees_application.txt", "w") as fd:
                    json.dump(applications, fd)
                print("Application withdrawn successfully.")
            else:
                print("No Record Found")
        else:
            break