import pyodbc


# Main class for connecting to the database
class DatabaseConnect:
    def __init__(self):
        self.server = "localhost"
        self.database = "Northwind"
        self.username = "dev"
        self.password = "test"
        self.connection = pyodbc.connect(
            f"DRIVER=ODBC Driver 17 for SQL Server;SERVER={self.server};DATABASE={self.database};UID={self.username};PWD={self.password}"
        )
        self.cursor = self.connection.cursor()


# Child class for the user expected functionality
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


def main():
    # Creates an instance of the child class
    db = ProductsDB()
    # Prints the average
    print(f"Average Units In Stock: {db.get_stock_average()}")


if __name__ == "__main__":
    main()