import os
import jwt
import datetime

from dotenv import load_dotenv
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

from database import db_operations

load_dotenv()
routes = Blueprint('routes', __name__)


@routes.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    password = data.get('password')

    if not name or not email or not phone or not password:
        return jsonify({'message': 'Missing information'}), 400

    hashed_password = generate_password_hash(password)

    if db_operations.check_email_exists(email):
        return jsonify({'message': 'Email already exists. Please log in.'}), 400

    db_operations.create_customer(name, email, phone, hashed_password)
    return jsonify({'message': 'Signup successful'}), 201

@routes.route('/login', methods=['POST'])
def login():
    auth = request.get_json()
    email = auth.get('email')
    password = auth.get('password')

    if not email or not password:
        return jsonify({'message': 'Missing email or password'}), 400

    user = db_operations.get_customer_by_email(email)
    if not user or not check_password_hash(user[4], password):
        return jsonify({'message': 'Invalid credentials'}), 401

    token = jwt.encode({'email': email, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)},
                       os.getenv("JWT_SECRET"))  # Change this to your secret key
    return jsonify({'token': token.decode('UTF-8')}), 200
