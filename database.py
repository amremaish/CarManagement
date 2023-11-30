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
        self.mycursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                name VARCHAR(255),
                                email VARCHAR(255),
                                phone VARCHAR(20),
                                password VARCHAR(255),
                                is_admin BOOLEAN DEFAULT FALSE)''')

        self.mycursor.execute('''CREATE TABLE IF NOT EXISTS vehicles (
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                type VARCHAR(50),
                                available BOOLEAN)''')

        self.mycursor.execute('''CREATE TABLE IF NOT EXISTS bookings (
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                user_id INT,
                                vehicle_id INT,
                                date_hired DATE,
                                date_returned DATE,
                                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                FOREIGN KEY(user_id) REFERENCES users(id),
                                FOREIGN KEY(vehicle_id) REFERENCES vehicles(id))''')

        self.mydb.commit()

    def check_email_exists(self, email):
        self.mycursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        result = self.mycursor.fetchone()
        if result:
            return True
        else:
            return False

    def get_user_by_email(self, email):
        query = "SELECT * FROM users WHERE email = %s"
        self.mycursor.execute(query, (email,))
        return self.mycursor.fetchone(), self.mycursor.column_names

    def get_user_by_id(self, user_id):
        query = "SELECT * FROM users WHERE id = %s"
        self.mycursor.execute(query, (user_id,))
        user = self.mycursor.fetchone()
        if user:
            user_info = {
                'id': user[0],
                'name': user[1],
                'email': user[2],
                'phone': user[3],
                'is_admin': user[5]
            }
            return user_info
        else:
            return None

    def update_customer(self, customer_id, name, email, phone, password):
        update_query = '''
            UPDATE users
            SET name = %s, email = %s, phone = %s, password = %s
            WHERE id = %s
        '''
        values = (name, email, phone, password, customer_id)
        try:
            self.mycursor.execute(update_query, values)
            self.mydb.commit()
        except mysql.connector.Error as err:
            print("Error updating customer:", err)
            self.mydb.rollback()

    def delete_customer(self, customer_id):
        delete_query = "DELETE FROM user WHERE id = %s"
        try:
            self.mycursor.execute(delete_query, (customer_id,))
            self.mydb.commit()
        except mysql.connector.Error as err:
            print("Error deleting customer:", err)
            self.mydb.rollback()

    def get_vehicle_by_id(self, vehicle_id):
        query = "SELECT * FROM vehicles WHERE id = %s"
        self.mycursor.execute(query, (vehicle_id,))
        return self.mycursor.fetchone()

    def create_vehicle(self, vehicle_type, available):
        sql = "INSERT INTO vehicles (type, available) VALUES (%s, %s)"
        val = (vehicle_type, available)
        self.mycursor.execute(sql, val)
        self.mydb.commit()

    def update_vehicle(self, vehicle_id, vehicle_type, available):
        sql = "UPDATE vehicles SET type = %s, available = %s WHERE id = %s"
        val = (vehicle_type, available, vehicle_id)
        self.mycursor.execute(sql, val)
        self.mydb.commit()

    def delete_vehicle(self, vehicle_id):
        sql = "DELETE FROM vehicles WHERE id = %s"
        val = (vehicle_id,)
        self.mycursor.execute(sql, val)
        self.mydb.commit()

    def check_availability(self, vehicle_id, date_hired, date_returned):
        self.mycursor.execute('''SELECT * FROM bookings
                                WHERE vehicle_id = %s AND
                                ((date_hired BETWEEN %s AND %s) OR
                                (date_returned BETWEEN %s AND %s))''',
                              (vehicle_id, date_hired, date_returned, date_hired, date_returned))
        return self.mycursor.fetchone()

    def create_user(self, name, email, phone, password):
        sql = "INSERT INTO users (name, email, phone, password) VALUES (%s, %s, %s, %s)"
        val = (name, email, phone, password)
        self.mycursor.execute(sql, val)
        self.mydb.commit()
        return self.mycursor.lastrowid

    def get_bookings_for_day(self, date):
        query = "SELECT * FROM bookings WHERE DATE(created_at) = %s"
        self.mycursor.execute(query, (date,))
        bookings = self.mycursor.fetchall()
        columns = [i[0] for i in self.mycursor.description]
        result = []

        for booking in bookings:
            booking_dict = dict(zip(columns, booking))
            result.append(booking_dict)
        return result

    def insert_booking(self, user_id, vehicle_id, date_hired, date_returned):
        self.mycursor.execute('''INSERT INTO bookings (user_id, vehicle_id, date_hired, date_returned)
                                VALUES (%s, %s, %s, %s)''',
                              (user_id, vehicle_id, date_hired, date_returned))
        self.mydb.commit()

    def close_connection(self):
        self.mydb.close()


db_operations = DatabaseManager()
db_operations.create_tables()
