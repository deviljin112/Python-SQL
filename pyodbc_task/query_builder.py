import pyodbc


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


class DBManagement(DatabaseConnect):
    def create_table(self, table, columns):
        # Table Syntax: <NAME>
        # Column Syntax: <NAME> <DATATYPE>, <NAME2> <DATATYPE2>
        # Variable query stores our query, f-string allows to create dynamic queries
        query = f"CREATE TABLE {table} ({', '.join(columns)});"
        # Executes the query, and if successful prints the prompt
        with self.cursor.execute(query):
            print("Table Created Successfully")
        # .commit() is used to save the changes and upload them to DB
        self.connection.commit()

    def delete_table(self, table):
        # Table Syntax: <NAME>
        query = f"DROP TABLE {table};"
        with self.cursor.execute(query):
            print("Table Dropped Successfully!")
        self.connection.commit()

    def add_row(self, table, rows, values):
        # Table Syntax: <NAME>
        # Rows Syntax: [<NAME>, <NAME>]
        # Values Syntax: ['<VALUE>', '<VALUE>']
        query = f"INSERT INTO {table} ({', '.join(rows)}) VALUES ({', '.join(values)});"
        with self.cursor.execute(query):
            print("Inserted successfully!")
        self.connection.commit()

    def delete_row(self, table, column, argument):
        # Table Syntax: <NAME>
        # Column Syntax: <COLUMN>
        # Argument Syntax: <ARGUMENT>
        query = f"DELETE FROM {table} WHERE {column} = ?;"
        with self.cursor.execute(query, argument):
            print("Deleted successfully!")
        self.connection.commit()

    def update_row(self, table, value_1, argument_1, value_2, argument_2):
        # Table Syntax: <NAME>
        # Value 1 + 2 Syntax: '<VALUE>'
        # Argument 1 + 2 Syntax: <ARGUMENT>
        query = f"UPDATE {table} SET {value_1} = ? WHERE {value_2} = ?;"
        with self.cursor.execute(query, argument_1, argument_2):
            print("Updated the record successfully!")
        self.connection.commit()

    def display_data(self, table):
        # Table Syntax: <NAME>
        query = f"SELECT * FROM {table};"
        with self.cursor.execute(query):
            # Since `SELECT` query returns the list of rows
            # .fetchone() returns a single row of data
            row = self.cursor.fetchone()
            # While there is data in that row
            while row:
                # We want to print that row
                print(f"{str(row)}")
                # Fetch a fresh row for next iteration
                row = self.cursor.fetchone()


def main():
    login = input("Login: ")
    password = input("Password: ")
    table_name = input("Table Name: ")

    # Creates an instance of the database
    database = DBManagement(login, password)
    while True:
        print(
            """
What would you like to do?
    - 'Create Table'
    - 'Delete Table'
    - 'Add Row'
    - 'Delete Row'
    - 'Update Row' (currently not working)
    - 'Display Data'
    - 'Exit'
        """
        )

        choice = input("=> ")
        if choice.lower() == "create table":

            column_data = []
            while True:
                print(
                    "Please provide column data.\nSyntax: COLUMN_NAME DATA_TYPE\nOr say 'return' to stop adding data."
                )
                column = input("=> ")

                if column.lower() == "return":
                    break
                else:
                    column_data.append(column)
            database.create_table(table_name, column_data)

        elif choice.lower() == "delete table":

            database.delete_table(table_name)

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
                    values_data.append(f"'{values}'")
                    i += 1
            database.add_row(table_name, rows, values_data)

        elif choice.lower() == "delete row":

            column_name = input("Row Name: ")
            value_name = input("Value Name: ")
            database.delete_row(table_name, column_name, value_name)

        elif choice.lower() == "update row":

            row_name = input("Column to update: ")
            value_name = input("New Value: ")
            column_name = input("Which Column to look for: ")
            where_value = input("What Value to look for: ")

            database.update_row(
                table_name, row_name, f"'{value_name}'", column_name, f"'{where_value}'"
            )

        elif choice.lower() == "display data":

            database.display_data(table_name)

        elif choice.lower() == "exit":
            break


if __name__ == "__main__":
    main()