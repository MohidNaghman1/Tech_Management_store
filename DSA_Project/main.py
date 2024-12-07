from admin_managment import admin  # Importing the admin management function
from customer_managment import customer  # Importing the customer function
from employee_managment import manage_employees # Importing the employee function

def main():
    print("\n\nWelcome to Mohid Tech Store")
    while True:
        print("1. Admin")
        print("2. Customer")
        print("3. Employees")
        print("4. Exit")
        
        try:
            choice = int(input("Enter choice: "))
            if choice == 1:
                admin()  # Call the admin management function
            elif choice == 2:
                customer()  # Call the customer interaction function
            elif choice == 3:
                manage_employees()  # Call the employee management function
            elif choice == 4:
                print("Thank you for visiting!")
                break  # Exit the program
            else:
                print("Invalid choice. Please try again.")  # Handle invalid input
        except ValueError:
            print("Invalid input. Please enter a number.")  # Handle non-integer input

if __name__ == "__main__":
    main()  # Start the application