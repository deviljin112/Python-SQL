import pyodbc


class DatabaseConnect:
    def __init__(self, login, password):
        self.server = "localhost"
        self.database = "pyodbc_task"
        self.username = login
        self.password = password
        self.connection = pyodbc.connect(
            f"DRIVER=ODBC Driver 17 for SQL Server;SERVER={server};DATABASE={database};UID={username};PWD={password}"
        )
        self.cursor = connection.cursor()


class DBManagement(DatabaseConnect):
    def create_table(self, table, columns):
        # Column Syntax: <NAME> <DATATYPE>, <NAME2> <DATATYPE2>
        query = f"CREATE TABLE {table} ({', '.join(columns)};"
        with self.cursor.execute(query):
            print("Table Created Successfully")
        self.connection.commit()

    def delete_table(self, table):
        query = f"DROP TABLE {table};"
        with self.cursor.execute(query):
            print("Table Dropped Successfully!")
        self.connection.commit()

    def add_row(self, table, rows, values):
        query = f"INSERT INTO {table} ({', '.join(rows)}) VALUES ({', '.join(values)};"
        with self.cursor.execute(query):
            print("Inserted successfully!")
        self.connection.commit()

    def delete_row(self, table, value, argument):
        query = f"DELETE FROM {table} WHERE {value} = ?;"
        with self.cursor.execute(query, argument):
            print("Deleted successfully!")
        self.connection.commit()

    def update_row(self, table, value_1, argument_1, value_2, argument_2):
        query = f"UPDATE {table} SET {value_1} = ? WHERE {value_2} = ?;"
        with self.cursor.execute(query, argument_1, argument_2):
            print("Updated the record successfully!")
        self.connection.commit()

    def display_data(self, table):
        query = f"SELECT * FROM {table};"
        with self.cursor(query):
            row = self.cursor.fetchone()
            while row:
                print(f"{str(row[0])}")
                row = self.cursor.fetchone()


def main():
    login = input("Login: ")
    password = input("Password: ")

    database = DBManagement(login, password)

    choice = input("What would you like to do?\n=> ")
    if choice.lower() == "create table":
        table_name = input("Table Name: ")
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
        table_name = input("Table Name: ")
        database.delete_table(table_name)

    elif choice.lower() == "add row":
        table_name = input("Table Name: ")
        print("What rows would you like to add to?\nSplit rows with a space")
        rows = input("=> ").split(" ")



    elif choice.lower() == "delete row":
        pass

    elif choice.lower() == "display data":
        pass


if __name__ == "__main__":
    main()