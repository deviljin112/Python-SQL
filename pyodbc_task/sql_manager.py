import pyodbc


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


class ProductsDB(DatabaseConnect):
    def get_stock_average(self):
        stocks_data = []
        query = "SELECT UnitsInStock FROM Products;"
        with self.cursor.execute(query):
            row = self.cursor.fetchone()
            while row:
                stocks_data.append(int(row[0]))
                row = self.cursor.fetchone()
        return sum(stocks_data) / len(stocks_data)


def main():
    db = ProductsDB()
    print(f"Average Units In Stock: {db.get_stock_average()}")


if __name__ == "__main__":
    main()