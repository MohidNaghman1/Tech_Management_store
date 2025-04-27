import mysql.connector
from mysql.connector import Error

# Function to connect to the database
def create_connection():
    print("Attempting to connect to the database...")
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',  # Host where your MySQL server is running
            user='root',        # MySQL username (should be 'root')
            password='mohid708@',  # Your MySQL password
            database='store_management',  # Your database name
            auth_plugin='mysql_native_password'  # Force using the native password authentication plugin
        )
        if connection.is_connected():
            print("Connection successful")
            return connection
    except Error as e:
        print(f"Error while connecting: {e}")
        return None

# Function to close the connection
def close_connection(connection):
    if connection.is_connected():
        connection.close()
        print("Connection closed")

# Function to execute a query (DML queries like INSERT, UPDATE, DELETE)
def execute_query(query, params=None):
    print("Executing query...")
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute(query, params) if params else cursor.execute(query)
            connection.commit()
            print("Query executed successfully")
        except Error as e:
            print(f"Error executing query: {e}")
        finally:
            cursor.close()
            close_connection(connection)
    else:
        print("No connection available to execute the query.")

# Function to fetch data from a query (SELECT queries)
def fetch_data(query, params=None):
    print("Fetching data...")
    connection = create_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute(query, params) if params else cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f"Error fetching data: {e}")
            return None
        finally:
            cursor.close()
            close_connection(connection)
    else:
        print("No connection available to fetch data.")
        return None

# Example of using the functions:
if __name__ == "__main__":
    # Example DML operation: Inserting data into the products table
    insert_query = """
        INSERT INTO products (name, description, price, quantity)
        VALUES (%s, %s, %s, %s)
    """
    data = ("Product 1", "Description of Product 1", 25.99, 100)
    execute_query(insert_query, data)

    # Example SELECT operation: Fetching data from products table
    select_query = "SELECT * FROM products"
    products = fetch_data(select_query)
    if products:
        print("Fetched Products:")
        for product in products:
            print(product)
