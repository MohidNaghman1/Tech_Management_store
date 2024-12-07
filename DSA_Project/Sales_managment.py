import json
import os

def view_sales():
    # Ensure the necessary files exist
    if not os.path.exists("data/sales.txt") or not os.path.exists("data/salesindex.txt"):
        print("Sales data files do not exist.")
        return

    # Read sales data
    with open("data/sales.txt", "r") as fd:
        with open("data/salesindex.txt", "r") as id:
            index_content = id.read().strip()
            index = int(index_content) if index_content else 0
            
            if index == 0:
                print("No Products Sold")
                return
            
            try:
                datadict = json.load(fd)
                total_earnings = 0
                print("\n\nProducts Sold: ")
                
                for key, value in datadict.items():
                    print("\nSale Number: ", key)
                    print("Product Name: ", value[0])
                    print("Quantity: ", value[1])
                    print("Price: $", value[2])
                    total_earnings += int(value[1]) * float(value[2])  # Ensure price is treated as float

                print("\nTotal Earnings: $", total_earnings)
            except json.JSONDecodeError:
                print("Error reading sales data: the file may be corrupted or empty.")
            except Exception as e:
                print(f"An error occurred: {e}")