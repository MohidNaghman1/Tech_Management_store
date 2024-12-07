import json
import os
def view_products():
    with open("data/products.txt","a+") as pd:
        with open("data/productindex.txt","r") as id:
            pd.seek(0)
            index = int(id.read())
            if index == 0:
                print("Store is Empty")
            else:
                products = json.load(pd)
                for key,value in products.items():
                    print("\n\nSerial Number: ",key)
                    print("Product Name: ",value[0])
                    print("Description: ",value[1])
                    print("Price: ",value[2])
                    print("Quantity: ",value[3])
def add_products():
    with open("data/products.txt","a+") as pd:
        with open("data/productsindex.txt","a+") as i:
            i.seek(0)
            pd.seek(0)
            index = int(i.read())
            if(index != 0):
                datadict = json.load(pd)
            else:
                datadict = dict()
            listdata = list()
            product_name = input("Enter Product name: ")
            product_description = input("Enter Product Discription: ")
            product_price = input("Enter Product Price: ")
            product_Quantity = input("Enter Quantity: ")
            listdata.append(product_name)
            listdata.append(product_description)
            listdata.append(product_price)
            listdata.append(product_Quantity)
            index += 1
            datadict[index] = listdata
            pd.seek(0)
            pd.truncate()
            json.dump(datadict,pd)
            i.seek(0)
            i.truncate()
            i.write(str(index))

def delete_products():
    # Ensure the products file exists
    if not os.path.exists("data/products.txt"):
        print("No products available to delete.")
        return
    

    with open("data/products.txt", "r+") as pd:
        with open("data/productsindex.txt", "r+") as i:
            # Load the current index
            i.seek(0)
            index_content = i.read().strip()
            index = int(index_content) if index_content else 0
            
            if index == 0:
                print("Store is Empty")
                return
            
            while True:
                view_products()  # Show current products
                num = input("Enter Serial Number to delete Product (or press Enter to cancel): ")

                # Check if the user wants to cancel
                if num == "":
                    print("Deletion canceled.")
                    return

                try:
                    num = int(num)
                    if num > 0 and str(num) in pd.read():
                        pd.seek(0)  # Go back to the start of the file
                        datadict = json.load(pd)
                        del datadict[str(num)]
                        index -= 1
                        i.seek(0)
                        i.truncate()
                        i.write(str(index))

                        # Rebuild the dictionary with updated keys
                        tempdict = {}
                        tempindex = 1
                        for key in datadict.keys():
                            tempdict[tempindex] = datadict[key]
                            tempindex += 1

                        pd.seek(0)
                        pd.truncate()
                        json.dump(tempdict, pd)

                        print("Successfully deleted Product")
                        break
                    else:
                        print("\nInvalid Serial Number")
                except ValueError:
                    print("Please enter a valid number or press Enter to cancel.")
            

def modify_products():
    # Ensure the products file exists
    if not os.path.exists("data/products.txt"):
        print("No products available to modify.")
        return

    with open("data/products.txt", "r+") as pd:
        # Load existing products
        products = json.load(pd) if os.path.getsize("data/products.txt") > 0 else {}
        
        if not products:
            print("\nStore is Empty")
            return
        
        view_products()  # Show current products

        while True:
            serial = input("Enter Serial Number to modify details: ")
            if serial in products:
                print("Previous Details: ")
                print(f"Product Name: {products[serial][0]}")
                print(f"Description: {products[serial][1]}")
                print(f"Price: {products[serial][2]}")
                print(f"Quantity: {products[serial][3]}")

                # Get new details from user
                product_name = input("Enter New Name (leave blank to keep current): ")
                product_description = input("Enter New Description (leave blank to keep current): ")
                product_price = input("Enter New Price (leave blank to keep current): ")
                product_quantity = input("Enter New Quantity (leave blank to keep current): ")

                # Update only if new values are provided
                if product_name: 
                    products[serial][0] = product_name
                if product_description:
                    products[serial][1] = product_description
                if product_price:
                    products[serial][2] = float(product_price)  # Ensure price is a float
                if product_quantity:
                    products[serial][3] = int(product_quantity)  # Ensure quantity is an int

                # Write updated products back to the file
                pd.seek(0)
                pd.truncate()
                json.dump(products, pd)

                print("\nChanges Successfully Done")
                break
            else:
                print("Invalid Serial Number. Try again.")
def manage_product():
    while(True):
        print("1. View Products")
        print("2. Add Products")
        print("3. Delete Products")
        print("4. Modify Products")
        print("5. Exit")
        choice = int(input("Enter choice: "))
        if(choice==1):
            view_products()
        elif(choice==2):
            add_products()
        elif(choice==3):
            delete_products()
        elif(choice==4):
            modify_products()
        else:
            break
def view_sales():
    with open("data/sales.txt","r") as fd:
        with open("data/salesindex.txt","r") as id:
            id.seek(0)
            index = int(id.read())
            if index==0:
                print("No Products Sold")
            else:
                datadict = json.load(fd)
                totalearnings = 0
                print("\n\nProducts Sold: ")
                for key,value in datadict.items():
                    print("\nSale Number: ",key)
                    print("Product Name: ",value[0])
                    print("Quantity: ",value[1])
                    print("Price: ",value[2])
                    totalearnings += int(value[1])*int(value[2])
                print("\nTotal Earnings: ",totalearnings)

def view_employees():
    hired_file_path = "data/hired_employees.txt"
    
    # Check if the hired employees file exists
    if not os.path.exists(hired_file_path):
        print("No employees found.")
        return

    with open(hired_file_path, "r") as fd:
        if os.path.getsize(hired_file_path) == 0:
            print("Currently No Employees")
            return
        
        try:
            datadict = json.load(fd)
            if not datadict:
                print("Currently No Employees")
                return
            
            print("Current Employees:")
            for key, value in datadict.items():
                print("Employee Name: ", key)
                print("Qualification: ", value[0])
                print("Skills: ", value[1])
                print()  # For better readability
        except json.JSONDecodeError:
            print("Error: Hired employees file is corrupted or contains invalid JSON.")
def hire_employees():
    if not os.path.exists("data/employees_application.txt"):
        print("No employee applications found.")
        return

    with open("data/employees_application.txt", "r+") as ed:
        if os.path.getsize("data/employees_application.txt") == 0:
            print("No employee applications to process.")
            return

        try:
            employees = json.load(ed)
        except json.JSONDecodeError:
            print("Error: Employees file is corrupted or contains invalid JSON.")
            return

        view_applications()  # Show current applications
        
        if not employees:
            print("No applications available.")
            return
        
        employee_name = input("Enter Employee Name to Accept or Reject Application: ").strip()

        # Normalize input for case-insensitive comparison
        normalized_employees = {name.lower(): name for name in employees.keys()}
        
        if employee_name.lower() in normalized_employees:
            actual_name = normalized_employees[employee_name.lower()]
            decision = input("Enter 1 to Accept and -1 to Reject: ")
            if decision == '1':
                print(f"{actual_name} has been accepted.")
                hire_employee(actual_name, employees[actual_name])
                del employees[actual_name]  # Remove from applications
                # Update the applications file
                ed.seek(0)
                ed.truncate()
                json.dump(employees, ed)
            elif decision == '-1':
                print(f"{actual_name} has been rejected.")
                del employees[actual_name]  # Remove from applications
                # Update the applications file
                ed.seek(0)
                ed.truncate()
                json.dump(employees, ed)
            else:
                print("Invalid input, please enter 1 or -1.")
        else:
            print("Employee not found in the application list.")

def hire_employee(name, details):
    # Logic to store accepted employees (could be a different file or structure)
    hired_file_path = "data/hired_employees.txt"
    
    if not os.path.exists(hired_file_path):
        with open(hired_file_path, "w") as hf:
            json.dump({}, hf)  # Initialize with an empty JSON object

    with open(hired_file_path, "r+") as hf:
        hired_employees = json.load(hf)
        
        # Add the employee details to the hired list
        hired_employees[name] = details
        
        # Write back to the hired employees file
        hf.seek(0)
        hf.truncate()
        json.dump(hired_employees, hf)

    print(f"{name} has been successfully hired.")

def fire_employees():
    hired_file_path = "data/hired_employees.txt"
    
    # Check if the hired employees file exists
    if not os.path.exists(hired_file_path):
        print("No employees found.")
        return

    with open(hired_file_path, "r+") as fd:
        if os.path.getsize(hired_file_path) == 0:
            print("Currently No Employees")
            return
        
        try:
            employees = json.load(fd)
        except json.JSONDecodeError:
            print("Error: Hired employees file is corrupted or contains invalid JSON.")
            return

        while True:
            name = input("Enter Employee Name to Fire (or press Enter to cancel): ").strip()
            
            if not name:  # Check if the input is empty
                print("Fire employee canceled.")
                return
            
            if name in employees:
                del employees[name]  # Remove the employee from the dictionary
                fd.seek(0)
                fd.truncate()  # Clear the file
                json.dump(employees, fd)  # Write the updated list back to the file
                print("\nEmployee Fired Successfully")
                break
            else:
                print("Invalid Name, Try Again")
def view_applications():
    with open("data/employees_application.txt","a+") as fd:
        with open("data/employees_applicationindex.txt","a+") as id:
            id.seek(0)
            index = int(id.read())
            if index == 0:
                print("No Applications")
            else:
                fd.seek(0)
                data = json.load(fd)
                for key,value in data.items():
                    print("\nEmployee Name: ",key)
                    print("Qualification: ",value[0])
                    print("Skills: ",value[1])
def manage_employees():
    while(True):
        print("1. View Employees")
        print("2. Hire Employees")
        print("3. Fire Employees")
        print("4. View Applications")
        print("5. Exit")
        choice = int(input("Enter choice: "))
        if(choice==1):
            view_employees()
        elif(choice==2):
            hire_employees()
        elif(choice==3):
            fire_employees()
        elif(choice==4):
            view_applications()
        elif(choice==5):
            break
        else:
            print("Invalid choice. TRY AGAIN")
def admin():
    with open("data/password.txt", "r") as fd:
        original_email = fd.readline().strip()  # Remove any leading/trailing whitespace
        original_password = fd.readline().strip()  # Remove any leading/trailing whitespace

    while True:
        input_email = input("Enter Email: ").strip()  # Remove any extra spaces/newlines
        if input_email == original_email:
            input_password = input("Enter Password: ").strip()  # Remove any extra spaces/newlines
            if input_password == original_password:
                while True:
                    print("1. Manage Products")
                    print("2. View Sales")
                    print("3. Manage Employees")
                    print("4. Exit")
                    choice = int(input("Enter choice: "))
                    if choice == 1:
                        manage_product()
                    elif choice == 2:
                        view_sales()
                    elif choice == 3:
                        manage_employees()
                    elif choice == 4:
                        break
                    else:
                        print("Invalid choice. TRY AGAIN")
                break
            else:
                print("Wrong Password")
        else:
            print("Wrong Email")


def buy_product():
    # Ensure all necessary files exist and are initialized
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

    # Reading the products and sales files
    with open("data/products.txt", "r") as fd:
        products = json.load(fd) if os.path.getsize("data/products.txt") > 0 else {}

    # Reading the products index file
    with open("data/productsindex.txt", "r") as i:
        index_content = i.read().strip()
        index = int(index_content) if index_content else 0

    if index == 0:
        print("No products available.")
        return
    
    view_products()

    total_bill = 0  # Initialize total bill

    # Processing purchases
    while True:
        serial = input("Enter Product Serial Number: ")
        if serial in products:
            while True:
                try:
                    quantity = int(input("Enter Quantity: "))
                except ValueError:
                    print("Please enter a valid number for quantity.")
                    continue

                listdata = products[serial]
                original_quantity = int(listdata[3])

                if original_quantity == 0:
                    print("Out of Stock")
                    return

                if quantity <= original_quantity:
                    # Ensure the price is treated as a float
                    product_price = float(listdata[2])  # Convert price to float
                    order_price = product_price * quantity
                    total_bill += order_price  # Update the total bill

                    # Read sales index
                    with open("data/salesindex.txt", "r+") as si:
                        sales_index_content = si.read().strip()
                        sales_index = int(sales_index_content) if sales_index_content else 0

                        # Update sales dictionary
                        with open("data/sales.txt", "r") as sd:
                            salesdict = json.load(sd) if os.path.getsize("data/sales.txt") > 0 else {}
                        
                        saleslist = [listdata[0], quantity, product_price]
                        sales_index += 1
                        salesdict[sales_index] = saleslist

                    # Write back the updated sales and sales index
                    with open("data/sales.txt", "w") as sd:
                        json.dump(salesdict, sd)

                    # Update product quantity
                    listdata[3] = original_quantity - quantity
                    products[serial] = listdata

                    # Write back the updated products
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
        else:
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

def employees():
    with open("data/employees_application.txt", "a+") as fd:
        with open("data/employees_applicationindex.txt", "a+") as ed:
            # Move to the beginning of the file
            ed.seek(0)
            # Read the index
            index_content = ed.read().strip()

            # Initialize index based on file content
            if index_content == "":
                index = 0
                applications = dict()  # Start with an empty dictionary
            else:
                index = int(index_content)
                fd.seek(0)
                if os.path.getsize("data/employees_application.txt") > 0:
                    applications = json.load(fd)
                else:
                    applications = dict()  # If the file is empty, initialize to an empty dict

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
                    applications[name] = listdata
                    index += 1

                    # Update the index file
                    ed.seek(0)
                    ed.truncate()
                    ed.write(str(index))
                    
                    # Update the applications file
                    fd.seek(0)
                    fd.truncate()
                    json.dump(applications, fd)
                elif choice == 2:
                    name = input("Enter name to withdraw: ")
                    if name in applications:
                        del applications[name]
                        index -= 1

                        # Update the index file
                        ed.seek(0)
                        ed.truncate()
                        ed.write(str(index))
                        
                        # Update the applications file
                        fd.seek(0)
                        fd.truncate()
                        json.dump(applications, fd)
                    else:
                        print("No Record Found")
                else:
                    break
def main():
    print("\n\nMohid Tech Store")
    while(True):
        print("1. Admin")
        print("2. Customer")
        print("3. Employees")
        print("4. Exit")
        choice = int(input("Enter choice: "))
        if(choice==1):
            admin()
        elif(choice==2):
            customer()
        elif(choice==3):
            employees()
        elif(choice==4):
            break
        else:
            print("Invalid choice. TRY AGAIN")
if __name__ == "__main__":
    main()