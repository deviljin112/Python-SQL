# Imports the microsoft driver
import pyodbc

server = "localhost"
database = "Northwind"
username = "dev"
password = "test"
# Syntax: DRIVER=<driver_name>;SERVER=<server_name>;DATABASE=<database_name>;UID=<username>;PWD=<password>
connection = pyodbc.connect(
    f"DRIVER=ODBC Driver 17 for SQL Server;SERVER={server};DATABASE={database};UID={username};PWD={password}"
)
# Location of you current path => Where to point to on calls
cursor = connection.cursor()


# .execute() runs the query specified
# .fetchall() gets all the information returned from the query
customer_row = cursor.execute("SELECT * FROM Customers;").fetchall()
print(customer_row)


# Query assigned to a variable
# ? means variable to be stated in the execute function
query = "SELECT CustomerID FROM Customers WHERE City = ?"
# Return value from the SQL query is assigned to a variable
output = cursor.execute(query, "London")
# Iterating through the results and printing its content
for i in output:
    print(i[0])


# Combination of loop and control flow to ensure we only iterate through data
# as long as data is available
query = cursor.execute("SELECT * FROM Products;")
while True:
    records = query.fetchone()
    if records is None:
        # When there is no records left, break loop
        break
    print(records.UnitPrice)
