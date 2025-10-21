import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        connection=mysql.connector.connect(
            host='localhost',
            user='root',
            password='Root@123',
            database='banking_app'
        )
        return connection
    except Error as e:
        print(f"Error:{e}");
        return None
def close_connection(connection):
    if connection and connection.is_connected():
        connection.close()