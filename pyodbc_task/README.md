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

## Task 2

```md
**SQL OOP**
_OOP task using pyodbc_
An sql manager for the products table.
create an object that relates only to the products table in the Northwind database. The reason for creating a single object for any table within the database would be to ensure that all functionality we build into this relates to what could be defined as a 'business function'.

As an example the products table, although relating to the rest of the company, will service a particular area of the business in this scenario we will simply call them the 'stock' department.

The stock department may have numerous requirements and it makes sense to contain all the requirements a code actions within a single object.

Create two files nw_products.py & nw_runner.py and then we will move into creating our object.

Our first requirement...
We've had a requirement for the stock department to print out the average value of all of our stock items.

Away we go....

!!!Important Note!!! It would be more efficient to write the SQL query to find the data and compute the value and simply return the value in Python.
```

Solution Available [HERE](sql_manager.py).

### Breakdown

Similarly to the previous task we initalise our connection parent class the same way to establish connection. However, in this task we need to create a child class that will pull the results and calculate the average of all the values in the column. To do that we simply make a query to select those values and iterate over each one and append it to a list. Then sum all the values and divide by how many values are in the list.

```python
class ProductsDB(DatabaseConnect):
    def get_stock_average(self):
        # Empty list for all the units in stock
        stocks_data = []
        # Query for selecting only one column
        query = "SELECT UnitsInStock FROM Products;"
        # Executes the query
        with self.cursor.execute(query):
            # Returns one single row at a time
            row = self.cursor.fetchone()
            # While there is still data available
            while row:
                # Add this data to our table
                stocks_data.append(int(row[0]))
                # Get a new row of data
                row = self.cursor.fetchone()
        # This simply returns the average
        # Add all values and divide by how many there are
        return sum(stocks_data) / len(stocks_data)
```

The return value of this function is a float which is our average.

## Task 3

### SQL Movies CRUD

#### Timings

60 Minutes

#### Summary

Now that you've learned how to connect to the DB using pyodbc you can start abstracting out interaction the db! This is great if you don't like writing sql.

#### Tasks

- CRUD the DB
- Hint: create abstraction and methods to deal with db so you don't have too

#### Acceptance Criteria

- You can get all the movies
- you can search based on title
- you can add movies to DB
</br>
second iteration:

- IMDB CSV <> Py <> SQL
- Summary
- You know how to parse txt files into python.
- You also know how to connect python into the db.
- You also know how to manipulated and change data with python.
</br>
Your task is to move data from text files into the db and from the the db into text files

#### Task

- read the text file and create object
- save object in DB

Load that from DB and create object

- output object to text file

#### Extra

Explore other APIs
</br>
Acceptance Criteria

- able to take in 10 film names in text file and save to db
- able to load data from DB and create text file with names

### Full Breakdown

Similarly to Task 1 and 2 the parent class is the connection initialiser. This class is extended by Table initialiser, which contains all the building queries to create the csv table, insert the data correctly, as well as some essential function that manipulate the data for it to be insertted correctly.

```python
def create_table(self, table_name, columns, columns_data):
    # Zip is used to combine the columns with column_data as one string
    query = f"CREATE TABLE {table_name} ({', '.join([f'{str(a)} {b}' for a, b in (zip(columns, columns_data))])})"
    with self.cursor.execute(query):
        print("Created table successfully!")
    self.cursor.commit()
```

This is an example of one function that combines the column list which contains all the `Column` name with `Column_data`. It uses `zip()` which combines the `columns` each index with `columns_data` index. It returns a tuple of the two values. Example: `columns[0]` value is put together with `columns_data[0]` value creating a tuple as `(a, b)` where `a = columns` and `b = columns_data`.
</br>
The next class is a child of the initialiser class. This class contains all the user interactions like displaying all data, finding specific movie, and adding a movie to the database.

```python
# Finds selected movie
def find(self, table_name, movie_name):
    # Selects all data
    query = f"SELECT * FROM {table_name}"
    with self.cursor.execute(query):
        row = self.cursor.fetchone()
        while row:
            # Iterates through all rows and checks if the movie name is inside of the list
            if movie_name in row:
                print(f"{', '.join([str(a) for a in row])}")
                break
            else:
                row = self.cursor.fetchone()
```

This function pulls all the fields from the database, then checks if the `movie_name` is anywhere in the row, as the title can be within either `originalTitle` or `primaryTitle`. Once found, it returns the entire row, in a more user-friendly string and breaks the loop to save resources if there is a lot of data in the table.
</br>
Last class is the CSV loader. This class opens the .csv file, and by using the `csv` module it iterates over each row which is then returned as a list.

```python
class CSVManager(UserInteractions):
    def get_movie_data(self):
        output = []
        with open("imdbtitles.csv", "r") as movie_data:
            data = csv.reader(movie_data)
            for row in data:
                output.append(row)
        return output
```

The remaining code is mostly prints and inputs for user interactions with ifs to control which function is called and executed. There is also some stealthly executed function which trigger the above classes to initialise and prepare the program for the user.
