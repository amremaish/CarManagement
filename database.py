import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()


class DatabaseManager:
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        self.mycursor = self.mydb.cursor()

    def create_tables(self):
        # Create tables if they don't exist
        self.mycursor.execute('''CREATE TABLE IF NOT EXISTS customers (
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                name VARCHAR(255),
                                email VARCHAR(255),
                                phone VARCHAR(20),
                                password VARCHAR(255))''')

        self.mycursor.execute('''CREATE TABLE IF NOT EXISTS vehicles (
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                type VARCHAR(50),
                                available BOOLEAN)''')

        self.mycursor.execute('''CREATE TABLE IF NOT EXISTS bookings (
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                customer_id INT,
                                vehicle_id INT,
                                date_hired DATE,
                                date_returned DATE,
                                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                FOREIGN KEY(customer_id) REFERENCES customers(id),
                                FOREIGN KEY(vehicle_id) REFERENCES vehicles(id))''')

        self.mydb.commit()

    def check_email_exists(self, email):
        self.mycursor.execute("SELECT * FROM customers WHERE email = %s", (email,))
        result = self.mycursor.fetchone()
        if result:
            return True
        else:
            return False

    def get_customer_id_by_email(self, email):
        query = "SELECT * FROM customers WHERE email = %s"
        self.mycursor.execute(query, (email,))
        result = self.mycursor.fetchone()
        if result:
            return result[self.mycursor.column_names.index('id')]
        else:
            return None

    def check_availability(self, vehicle_id, date_hired, date_returned):
        self.mycursor.execute('''SELECT * FROM bookings
                                WHERE vehicle_id = %s AND
                                ((date_hired BETWEEN %s AND %s) OR
                                (date_returned BETWEEN %s AND %s))''',
                              (vehicle_id, date_hired, date_returned, date_hired, date_returned))
        return self.mycursor.fetchone()

    def create_customer(self, name, email, phone, password):
        sql = "INSERT INTO customers (name, email, phone, password) VALUES (%s, %s, %s, %s)"
        val = (name, email, phone, password)
        self.mycursor.execute(sql, val)
        self.mydb.commit()
        return self.mycursor.lastrowid

    def insert_booking(self, customer_id, vehicle_id, date_hired, date_returned):
        self.mycursor.execute('''INSERT INTO bookings (customer_id, vehicle_id, date_hired, date_returned)
                                VALUES (%s, %s, %s, %s)''',
                              (customer_id, vehicle_id, date_hired, date_returned))
        self.mydb.commit()

    def close_connection(self):
        self.mydb.close()


db_operations = DatabaseManager()
db_operations.create_tables()
