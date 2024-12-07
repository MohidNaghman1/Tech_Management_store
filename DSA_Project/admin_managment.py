from employee_managment import manage_employees
from Product_manage import manage_products
from Sales_managment import view_sales  # Assuming you have a sales manaxgement module

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
                    print("\n1. Manage Products")
                    print("2. View Sales")
                    print("3. Manage Employees")
                    print("4. Exit")
                    choice = int(input("Enter choice: "))
                    if choice == 1:
                        manage_products()  # Assuming this function is defined in product_management.py
                    elif choice == 2:
                        view_sales()  # Assuming this function is defined in sales_management.py
                    elif choice == 3:
                        manage_employees()  # Defined in employee_management.py
                    elif choice == 4:
                        print("Exiting admin panel.")
                        break
                    else:
                        print("Invalid choice. TRY AGAIN")
                break
            else:
                print("Wrong Password")
        else:
            print("Wrong Email")