import mysql.connector
from mysql.connector import Error

from config import host, user, password, database

class Database:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def get_database():
        return Database(host=host, user=user, password=password, database=database)

    def _connect(self):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            return connection
        except Error as e:
            print(f"Error connecting to the database: {e}")
            return None

    def select(self, query, params=None):
        """Executes a SELECT query and returns the results."""
        connection = self._connect()
        if not connection:
            return None
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, params)
            results = cursor.fetchall()
            return results
        except Error as e:
            print(f"Error executing SELECT query: {e}")
            return None
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def execute(self, query, params=None):
        """Executes an INSERT, UPDATE, or DELETE query."""
        connection = self._connect()
        if not connection:
            return None
        try:
            cursor = connection.cursor()
            cursor.execute(query, params)
            connection.commit()
            print(f"Query executed successfully. Rows affected: {cursor.rowcount}")
            return cursor.rowcount
        except Error as e:
            print(f"Error executing query: {e}")
            return None
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

# Example usage:
# if __name__ == "__main__":
#     db = Database(host="localhost", user="root", password="", database="rapidremit")

    # # SELECT Example
    # select_query = "SELECT * FROM user WHERE userId = %s"
    # select_params = (1,)
    # results = db.select(select_query, select_params)
    # if results:
    #     for row in results:
    #         print(row)

    # # INSERT Example
    # insert_query = "INSERT INTO user (userId, name) VALUES (%s, %s)"
    # insert_params = (1, "test")
    # db.execute(insert_query, insert_params)

    # UPDATE Example
    # update_query = "UPDATE user SET userName = %s WHERE userId = %s"
    # update_params = ("test", 1)
    # db.execute(update_query, update_params)

#     # DELETE Example
#     delete_query = "DELETE FROM your_table WHERE id = %s"
#     delete_params = (1,)
#     db.execute(delete_query, delete_params)
