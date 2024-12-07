import json
import os

# Node class for Linked List
class ProductNode:
    def __init__(self, serial, data):
        self.serial = serial
        self.data = data  # Data is a list containing [name, description, price, quantity]
        self.next = None  # Pointer to the next node

# Linked List class for Products
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


    def delete_product(self, serial):
        current = self.head
        prev = None
        while current:
            if current.serial == serial:
                if prev:
                    prev.next = current.next
                else:
                    self.head = current.next
                return True
            prev = current
            current = current.next
        return False

    def modify_product(self, serial, new_data):
        current = self.head
        while current:
            if current.serial == serial:
                current.data = new_data
                return True
            current = current.next
        return False

    def load_from_file(self, file_path):
            """Loads products from a specified file path."""
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

    def __len__(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count

    def save_to_file(self):
        products_dict = {}
        current = self.head
        while current:
            products_dict[current.serial] = current.data
            current = current.next
        with open("data/products.txt", "w") as pd:
            json.dump(products_dict, pd)
            
def view_products(product_list):
    # Check if the product file exists
    if not os.path.exists("data/products.txt"):
        print("Products file does not exist.")
        return

    with open("data/productindex.txt", "r") as id:
        index_content = id.read().strip()
        index = int(index_content) if index_content else 0
        
        if index == 0:
            print("Store is Empty")
            return

    # Open the products file in read mode
    with open("data/products.txt", "r") as pd:
        try:
            products = json.load(pd)
            for key, value in products.items():
                print("\n\nSerial Number: ", key)
                print("Product Name: ", value[0])
                print("Description: ", value[1])
                print("Price: $", value[2])
                print("Quantity: ", value[3])
        except json.JSONDecodeError:
            print("Error: Unable to read products. The file may be corrupted or empty.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


def add_products(product_list):
    product_name = input("Enter Product Name: ")
    product_description = input("Enter Product Description: ")
    try:
        product_price = float(input("Enter Product Price: "))  # Ensure price is a float
        quantity = int(input("Enter Quantity: "))
    except ValueError:
        print("Invalid input. Please enter numeric values for price and quantity.")
        return

    # Generate a serial number based on the current size of the product list
    serial = str(len(product_list) + 1)  # This will now work

    # Add the product to the list
    product_data = [product_name, product_description, product_price, quantity]
    product_list.add_product(serial, product_data)

    # Optionally, save the updated list back to the file
    # save_products(product_list)
    print("Product added successfully!")

def delete_products(product_list):
    serial = input("Enter Serial Number to delete Product: ")
    if product_list.delete_product(serial):
        product_list.save_to_file()
        print("Product deleted successfully.")
    else:
        print("Product not found.")

def modify_products(product_list):
    serial = input("Enter Serial Number to modify: ")
    current = product_list.head
    while current:
        if current.serial == serial:
            print("Previous Details:")
            print(f"Product Name: {current.data[0]}")
            print(f"Description: {current.data[1]}")
            print(f"Price: {current.data[2]}")
            print(f"Quantity: {current.data[3]}")

            # Get new details from user
            product_name = input("Enter New Name (leave blank to keep current): ") or current.data[0]
            product_description = input("Enter New Description (leave blank to keep current): ") or current.data[1]
            product_price = input("Enter New Price (leave blank to keep current): ")
            product_quantity = input("Enter New Quantity (leave blank to keep current): ")

            new_data = [
                product_name,
                product_description,
                float(product_price) if product_price else current.data[2],
                int(product_quantity) if product_quantity else current.data[3],
            ]
            product_list.modify_product(serial, new_data)
            product_list.save_to_file()
            print("Product modified successfully.")
            return
        current = current.next
    print("Product not found.")

def manage_products():
    product_list = ProductLinkedList()  # Assuming this initializes your product linked list
    product_list.load_from_file("data/products.txt")  # Load existing products

    while True:
        print("\n1. View Products")
        print("2. Add Products")
        print("3. Delete Products")
        print("4. Modify Products")
        print("5. Exit")
        choice = int(input("Enter choice: "))

        if choice == 1:
            view_products(product_list)  # Assuming view_products is defined to take product_list
        elif choice == 2:
            add_products(product_list)  # Correctly passing product_list
        elif choice == 3:
            delete_products(product_list)  # Assuming this function is defined
        elif choice == 4:
            modify_products(product_list)  # Assuming this function is defined
        elif choice == 5:
            print("Exiting product management.")
            break
        else:
            print("Invalid choice. Please try again.")