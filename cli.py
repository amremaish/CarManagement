import sys
from getpass import getpass  # For secure password input
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash
from database import db_operations

load_dotenv()


def create_admin_user():
    # Collect user inputs for admin creation
    name = input("Enter name: ")
    email = input("Enter email: ")
    phone = input("Enter phone: ")
    password = getpass("Enter password: ")
    hashed_password = generate_password_hash(password)
    if db_operations.check_email_exists(email):
        print('Email already exists.')
        return
    db_operations.create_user(name, email, phone, hashed_password)
    print("Admin user created successfully!")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <action>")
        sys.exit(1)

    action = sys.argv[1]

    if action == 'create_admin':
        create_admin_user()
    else:
        print("Invalid action.")
