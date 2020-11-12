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


# This class is used for initialising the db with provided csv file
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

    # This method creates the initial table with columns and column types based on the data in the fields
    def create_table(self, table_name, columns, columns_data):
        # Zip is used to combine the columns with column_data as one string
        query = f"CREATE TABLE {table_name} ({', '.join([f'{str(a)} {b}' for a, b in (zip(columns, columns_data))])})"
        with self.cursor.execute(query):
            print("Created table successfully!")
        self.cursor.commit()

    # Inserts the initial data into the table
    def insert_data(self, table_name, columns, data):
        # Boolean to track whether there was an issue with inserting the query
        success = True
        # Iterates through each movie list (data is a list of lists)
        for movie in data:
            # Iterates through each value in the list
            for i in range(len(movie)):
                # Checks if the provided value matches the data type
                if not movie[i].isdigit():
                    # Replaces any inconsitencies or `N/A` fields to the right type
                    if movie[i] == "\\N":
                        movie[i] = "0"
                    else:
                        # Formats the input into SQL Format
                        movie[i] = f"'{movie[i]}'"

            # Creates the query
            query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(movie)})"
            # Attempts to execute the query and catch any errors
            try:
                self.cursor.execute(query)
            except:
                # If error occurs sets boolean to False and breaks the loop
                success = False
                break
        # If no error occured commits the changes to be saved
        if success:
            print("Data Inserted Successfully!")
            self.cursor.commit()
        # Else it will print the message and not submit the changes
        else:
            print("Data Insertion Failed... Please try again!")

    # Due to formatting in CSV is that some strings contain special characters
    # This function removes them so that its uniform
    def check_alphabetic_input(self, word):
        output_word = []
        for letter in word:
            # Checks if letter is in the alphabet
            if letter.isalpha() and letter != "ï":
                # Adds that letter to a list
                output_word.append(letter)
        # Concatinates back to a word
        return "".join(output_word)

    # This is the generator of column data types
    def column_data(self, data):
        column_data = []
        # Loops though each field in the list
        for i in data:
            # Checks if its data has number or not
            if i.isdigit():
                # Adds INT data type if its a numbers
                column_data.append("INT")
            else:
                # If String data type is set to VARCHAR
                column_data.append("VARCHAR(255)")
        # Returns the list of Data Types
        return column_data

    # Initialisation method checks if there is any data in the table
    # If the table is empty it will initialise either creating or inserting into the table
    def initialisation(self, table_name):
        query = f"SELECT * FROM {table_name}"
        with self.cursor.execute(query):
            row = self.cursor.fetchone()
            if row:
                return True


# Class that focuses on User Interacting with the database
class UserInteractions(SQLMovies):
    # Displays all data from the table
    def display(self, table_name):
        query = f"SELECT * FROM {table_name}"
        with self.cursor.execute(query):
            row = self.cursor.fetchone()
            while row:
                print(f"{', '.join([str(a) for a in row])}")
                row = self.cursor.fetchone()

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

    # Adds the movie into the list
    def add_movie(self, table_name, column, data):
        query = (
            f"INSERT INTO {table_name} ({', '.join(column)}) VALUES ({', '.join(data)})"
        )
        with self.cursor.execute(query):
            print("Successfully Insertted The Movie!")

        self.cursor.commit()


# This class focuses on importing CSV into Python List
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
    # Initialises the class
    test = CSVManager("dev", "test")

    # Attempts to check if the "movies" table exists
    try:
        previously_executed = test.initialisation(table_name)
    except:
        previously_executed = False

    # Stores all the csv movies in one variable
    movies = test.get_movie_data()
    # Sets the columns list to one variable
    column = movies[0]
    # Makes a lists of lists which contain the movie information
    movie_data = movies[1:]
    # Calls the function to create Column Data Type list
    column_data = test.column_data(movie_data[0])

    # Checks if all the strings are alphabetic and not symbols
    for i in range(len(column)):
        column[i] = test.check_alphabetic_input(column[i])

    # If the table doesnt exist or there is no data, perform initalisation
    if not previously_executed:

        # Attempts to create a table if it doesnt exist
        try:
            test.create_table(table_name, column, column_data)
        except:
            print("Table exists! Skipping")
        # Runs insertion regardless if table was created or it exists
        finally:
            # If there is no data in the table create it from CSV file
            if not previously_executed:
                test.insert_data(table_name, column, movie_data)

    # User Main Menu
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
            # Logic for adding new row to the DB
            # Iterates as many times as there are columns in the table
            for i in range(len(column)):
                print(column[i], column_data[i])
                user_input = input("=> ")

                # Makes the string an integer if the column is INT
                if "INT" in column_data[i]:
                    user_input = int(user_input)

                # Turns the input into SQL format
                user_input = f"'{user_input}'"

                user_data.append(user_input)

            test.add_movie(table_name, column, user_data)
        elif choice.lower() == "exit":
            break
        else:
            print("Thats not a valid option!")


if __name__ == "__main__":
    main()