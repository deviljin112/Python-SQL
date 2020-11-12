import pyodbc
import csv


# Main class used for connecting to the database
class DatabaseConnect:
    # Initialises the class with `login` and `password` variables
    def __init__(self, login, password):
        # Assigns the default variables for db initialisation
        self.server = "localhost"
        self.database = "movie_task"
        self.username = login
        self.password = password
        # .connect() establishes the connection to db
        self.connection = pyodbc.connect(
            f"DRIVER=ODBC Driver 17 for SQL Server;SERVER={self.server};DATABASE={self.database};UID={self.username};PWD={self.password}"
        )
        # .cursor() instance allows all the query executions
        self.cursor = self.connection.cursor()


class SQLMovies(DatabaseConnect):
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

    def create_table(self, table_name, columns, columns_data):
        query = f"CREATE TABLE {table_name} ({', '.join([f'{str(a)} {b}' for a, b in (zip(columns, columns_data))])})"
        with self.cursor.execute(query):
            print("Created table successfully!")

    def insert_data(self, table_name, columns, data):
        success = True
        for movie in data:
            for i in range(len(movie)):
                if not movie[i].isdigit():
                    if movie[i] == "\\N":
                        movie[i] = "0"
                    else:
                        movie[i] = f"'{movie[i]}'"

                        if "automne" in movie[i]:
                            movie[i].replace("d'a", "da")


                if "sacre" in movie[i]:
                    print(movie)

            query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(movie)})"
            # self.cursor.execute(query)

        if success:
            print("Data Inserted Successfully!")
        else:
            print("Data Insertion Failed... Please try again!")

    def check_alphabetic_input(self, word):
        output_word = []
        for letter in word:
            if letter.isalpha() and letter != "ï":
                output_word.append(letter)
        return "".join(output_word)

    def column_data(self, data):
        column_data = []
        for i in data:
            if i.isdigit():
                column_data.append("INT")
            else:
                column_data.append("VARCHAR(255)")
        return column_data

    def initialisation(self, table_name):
        query = f"SELECT * FROM {table_name}"
        with self.cursor.execute(query):
            row = self.cursor.fetchone()
            if row:
                return True


class UserInteractions(SQLMovies):
    def display(self, table_name):
        query = f"SELECT * FROM {table_name}"
        with self.cursor.execute(query):
            row = self.cursor.fetchone()
            while True:
                if row:
                    print(", ".join(row))
                    row = self.cursor.fetchone()
                else:
                    break

    def find(self, table_name, movie_name):
        query = f"SELECT * FROM {table_name}"
        with self.cursor.execute(query):
            row = self.cursor.fetchone()
            while True:
                if row:
                    if movie_name in row:
                        print(", ".join(row))
                        break
                    else:
                        row = self.cursor.fetchone()
                else:
                    break

    def add_movie(self, table_name, column, data):
        query = (
            f"INSERT INTO {table_name} ({', '.join(column)}) VALUES ({', '.join(data)})"
        )
        with self.cursor.execute(query):
            print("Successfully Insertted The Movie!")


class CSVManager(UserInteractions):
    def get_movie_data(self):
        output = []
        with open("imdbtitles.csv", "r") as movie_data:
            data = csv.reader(movie_data)
            for row in data:
                output.append(row)
        return output


def main():
    table_name = "movies"
    test = CSVManager("dev", "test")

    try:
        previously_executed = test.initialisation(table_name)
    except:
        previously_executed = False

    movies = test.get_movie_data()
    column = movies[0]
    movie_data = movies[1:]
    column_data = test.column_data(movie_data[0])

    if not previously_executed:
        for i in range(len(column)):
            column[i] = test.check_alphabetic_input(column[i])

        try:
            test.create_table(table_name, column, column_data)
        except:
            print("Table exists! Skipping")
        finally:
            test.insert_data(table_name, column, movie_data)

    else:
        while True:
            print(
                """
    What would you like to do?
        - 'Display' all movies
        - 'Add' a movie
        - 'Find' specific movie
        - 'Exit' the program
    """
            )
            choice = input("=> ")

            if choice.lower() == "display":
                test.display(table_name)

            elif choice.lower() == "find":
                movie_name = input("What the movie name?\n=> ")
                test.find(table_name, movie_name)

            elif choice.lower() == "add":
                print(
                    f"""
    Please fill in the following data:
    {", ".join(column)}
    Submitting each column with ENTER
    """
                )
                user_data = []
                for i in range(len(column)):
                    user_input = input("=> ")

                    if "INT" in column_data[i]:
                        user_input = int(user_input)

                    user_data.append(user_input)
            elif choice.lower() == "exit":
                break
            else:
                print("Thats not a valid option!")


if __name__ == "__main__":
    main()