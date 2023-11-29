from dotenv import load_dotenv
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash

from database import db_operations

load_dotenv()
auth_routes = Blueprint('routes', __name__)


@auth_routes.route('/signup', methods=['POST'])
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
        return jsonify({'message': 'Email already exists.'}), 400

    db_operations.create_user(name, email, phone, hashed_password)
    return jsonify({'message': 'Signup successful'}), 201


@auth_routes.route('/login', methods=['POST'])
def login():
    auth = request.get_json()
    email = auth.get('email')
    password = auth.get('password')

    if not email or not password:
        return jsonify({'message': 'Missing email or password'}), 400

    user, cols = db_operations.get_user_by_email(email)

    if not user or not check_password_hash(user[cols.index('password')], password):
        return jsonify({'message': 'Invalid credentials'}), 401

    access_token = create_access_token(identity=email)
    return jsonify({'access_token': access_token}), 200
