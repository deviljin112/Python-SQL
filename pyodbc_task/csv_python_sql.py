import pyodbc

# Main class used for connecting to the database
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


# Load CSV File
# Iterate over data to make it SQL Ready
# Constructor to push to SQL Table
# Automated display of specified data