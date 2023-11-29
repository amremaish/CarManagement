import os
import sys
import mysql.connector
from getpass import getpass  # For secure password input
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash

load_dotenv()


def create_admin_user():
    try:
        # Collect user inputs for admin creation
        name = input("Enter name: ")
        email = input("Enter email: ")
        phone = input("Enter phone: ")
        password = getpass("Enter password: ")

        # Establish connection to your MySQL database
        mydb = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )

        mycursor = mydb.cursor()

        insert_query = '''
            INSERT INTO users (name, email, phone, password, is_admin)
            VALUES (%s, %s, %s, %s, %s)
        '''

        hashed_password = generate_password_hash(password)

        mycursor.execute(insert_query, (name, email, phone, hashed_password, True))
        mydb.commit()

        print("Admin user created successfully!")

    except mysql.connector.Error as err:
        print("Error creating admin user:", err)

    finally:
        # Close database connection
        if 'mydb' in locals() and mydb.is_connected():
            mycursor.close()
            mydb.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <action>")
        sys.exit(1)

    action = sys.argv[1]

    if action == 'create_admin':
        create_admin_user()
    else:
        print("Invalid action.")
