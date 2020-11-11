# PYODBC Task

## Requirements

- `import pyodbc` (`pip install pyodbc`)

## Task 1

```md
Task:

- Create a new file and a class with function to establish connection with pyodbc
- create a function that create a table in the DB
- create a function that prompts user to input data in that table
- create a new file called PYODBC_TASK.md and document the steps to implement the task
```

Solution available [HERE](query_builder.py).

### Break-down

#### Parent class

We create a class that will be our parent class and also act as the initalisation for connection to the database. This class takes 2 user input variables, login and password which is used to connect to the database.

```python
class DatabaseConnect:
    # Initialises the class with `login` and `password` variables
    def __init__(self, login, password):
        # Assigns the default variables for db initialisation
        self.server = "localhost"
        self.database = "pyodbc_task"
        self.username = login
        self.password = password
        # .connect() establishes the connection to db
        self.connection = pyodbc.connect(
            f"DRIVER=ODBC Driver 17 for SQL Server;SERVER={self.server};DATABASE={self.database};UID={self.username};PWD={self.password}"
        )
        # .cursor() instance allows all the query executions
        self.cursor = self.connection.cursor()
```

#### Child class

We then create a child class that inherits this connection. This child class will store all of our functions that we will use later. All the functions follow the same conventions which will be explained with the following example:

```python
def add_row(self, table, rows, values):
    # Table Syntax: <NAME>
    # Rows Syntax: [<NAME>, <NAME>]
    # Values Syntax: ['<VALUE>', '<VALUE>']
    query = f"INSERT INTO {table} ({', '.join(rows)}) VALUES ({', '.join(values)});"
    with self.cursor.execute(query):
        print("Inserted successfully!")
    self.connection.commit()
```

Each function takes in `table` variable as well as arguments either `rows`, `values`, `column`, `argument`. These arguments depend on what the function will do. In the above example we only focusing on `rows` and `values`. Both of these variables are lists. `table` argument is a string that we will use to access a specific table. `rows` contains a list of strings which are names of the rows we want to append data to. While `values` are the corresponding values we want to add to those `rows`.
</br>
Each function has pseudo code syntax explaining what are the inputs for the function, making it easier to visualise how this data is manipulated. `query` variable stores the query that we will be executing. This variable is an f-string meaning it is formatted based on the values provided by the user. It dynamically generates new data requested by the user.
</br>
We then use `with` statement to execute the query. If the execution is successful the function will print a prompt telling us so. Next, we use `.commit()` to submit our changes to the database so they are stored. This step is important as it sends this new data for the database to update otherwise after closing the program we will lose all of our progress and changes.

#### Things to look out for

When making inputs in Python they are automatically assigned into a `string` format. This is mostly the format that we will use for inputting data. However, when inserting data into any table, SQL has specific formatting conventions. String `hello` is not the same as `'hello'` for this reason we need to do some cleaver formatting so that we do not get an error when executing our query. We can see this done in our `add row` logic in `main()` function.

```python
elif choice.lower() == "add row":

    print("What rows would you like to add to?\nSplit rows with a space")
    rows = input("=> ").split(" ")

    values_data = []
    i = 0
    while True:
        if i == len(rows):
            break
        else:
            print(
                "What data would you like to add?\nInput one value at a time.\nSubmit with ENTER."
            )
            values = input("=> ")
            # This f-string is used to match the SQL's formatting conventions
            values_data.append(f"'{values}'")
            i += 1
    database.add_row(table_name, rows, values_data)
```

Third from the bottom line is our clever trick. By making an f-string and adding `'` before and after our variable, what python will do is convert the user inputted string into SQL formatting when appending it into our list of data. Example: if the user inputs `Apple` the program will actually append `'Apple'` instead, which is a valid SQL format for adding new values.
