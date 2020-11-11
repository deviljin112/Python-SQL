# Python-SQL

## PYODBC

- Python Open Database Connectivity
- API for connecting to an SQL Server

![Diagram](PythonSQL.png)

## Lesson Plan

- With is Cursor
- How to use it
- Functions used to interact with SQL Data
- Set up pyodbc
  - `pip install pyodbc`
  - `import pyodbc`

## Establishing a connection

```python
server = "server_name"
database = "database_name"
username = "username"
password = "password"
# Syntax: DRIVER=<driver_name>;SERVER=<server_name>;DATABASE=<database_name>;UID=<username>;PWD=<password>
connection = pyodbc.connect(
    f"DRIVER=ODBC Driver 17 for SQL Server;SERVER={server};DATABASE={database};UID={username};PWD={password}"
)
# Location of you current path => Where to point to on calls
cursor = connection.cursor()
```

## Implementation

Syntax Dictionary:

- `pyodbc` = Module used to interact with SQL.
- `cursor` = Function used to tell SQL what path we want to work in.
- `fetchone` = Selects one single row of data at a time
- `fetchall` = Selects all results at once

### Fetch All Example

Simple example of fetching all details from a specific table in a table. Uses `.fetchall()` to get all the rows and columns.

```python
# .execute() runs the query specified
# .fetchall() gets all the information returned from the query
customer_row = cursor.execute("SELECT * FROM Customers;").fetchall()
print(customer_row)
```

### Iterating through data

Extension from previous example. Here we iterate through each row, and print the results one by one. We can also specify a `WHERE` clause which checks against a `?` argument, this argument is later specified in the `execute()` function and added to the query in order of appearance. I.e. if there are multiple `?` clauses they will be applied from the `execute()` function one by one as they appear in the query.

```python
# Query assigned to a variable
# ? means variable to be stated in the execute function
query = "SELECT CustomerID FROM Customers WHERE City = ?"
# Return value from the SQL query is assigned to a variable
output = cursor.execute(query, "London").fetchall()
# Iterating through the results and printing its content
for i in output:
    print(i[0])
```

### Loop and Control Flow

More advanced implementation that fetches data one by one with `.fetchone()`. It is checked if the row exists and then proceeeds to only print a specific column from the table.

```python
# Combination of loop and control flow to ensure we only iterate through data
# as long as data is available
query = cursor.execute("SELECT * FROM Products;")
while True:
    records = query.fetchone()
    if records is None:
        # When there is no records left, break loop
        break
    print(records.UnitPrice)
```

## Task

- Create a file and a class function
- Establish an SQL Connection with DB
- Create a function that create a table in the DB
- Create a function that prompts user to input data to that table
- Create a file called "PYODBC_TASK.md" => README
- Document steps taken
