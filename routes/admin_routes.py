from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash

from database import db_operations

admin_routes = Blueprint('admin_routes', __name__)
vehicle_routes = Blueprint('vehicle_routes', __name__)


def is_admin():
    user, cols = db_operations.get_user_by_email(get_jwt_identity())
    return user[cols.index('is_admin')] == 1


@admin_routes.route('/admin/customers', methods=['POST'])
@jwt_required()
def create_customer():
    if not is_admin():
        return jsonify({'message': 'Unauthorized access'}), 403

    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    password = data.get('password')

    if not all([name, email, phone, password]):
        return jsonify({'message': 'Missing information'}), 400

    hashed_password = generate_password_hash(password)

    if db_operations.check_email_exists(email):
        return jsonify({'message': 'Email already exists.'}), 400

    db_operations.create_user(name, email, phone, hashed_password)
    return jsonify({'message': 'Customer created'}), 201


@admin_routes.route('/admin/customers/<int:customer_id>', methods=['GET'])
@jwt_required()
def get_customer_by_id(customer_id):
    if not is_admin():
        return jsonify({'message': 'Unauthorized access'}), 403

    customer = db_operations.get_user_by_id(customer_id)
    if not customer:
        return jsonify({'message': 'Customer not found'}), 404

    return jsonify({'customer': customer}), 200


@admin_routes.route('/admin/customers/<int:customer_id>', methods=['PUT'])
@jwt_required()
def update_customer(customer_id):
    if not is_admin():
        return jsonify({'message': 'Unauthorized access'}), 403

    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    password = data.get('password')

    if not all([name, email, phone, password]):
        return jsonify({'message': 'Missing information'}), 400

    hashed_password = generate_password_hash(password)
    db_operations.update_customer(customer_id, name, email, phone, hashed_password)
    return jsonify({'message': 'Customer updated'}), 200


@admin_routes.route('/admin/customers/<int:customer_id>', methods=['DELETE'])
@jwt_required()
def delete_customer(customer_id):
    if not is_admin():
        return jsonify({'message': 'Unauthorized access'}), 403

    db_operations.delete_customer(customer_id)
    return jsonify({'message': 'Customer deleted'}), 200


@vehicle_routes.route('/admin/vehicles', methods=['POST'])
@jwt_required()
def create_vehicle():
    if not is_admin():
        return jsonify({'message': 'Unauthorized access'}), 403

    data = request.get_json()
    vehicle_type = data.get('type')
    available = data.get('available')

    if not all([vehicle_type, available]):
        return jsonify({'message': 'Missing information'}), 400

    db_operations.create_vehicle(vehicle_type, available)
    return jsonify({'message': 'Vehicle created'}), 201


@vehicle_routes.route('/admin/vehicles/<int:vehicle_id>', methods=['GET'])
@jwt_required()
def get_vehicle_by_id(vehicle_id):
    if not is_admin():
        return jsonify({'message': 'Unauthorized access'}), 403

    vehicle = db_operations.get_vehicle_by_id(vehicle_id)
    if not vehicle:
        return jsonify({'message': 'Vehicle not found'}), 404

    return jsonify({'vehicle': vehicle}), 200


@vehicle_routes.route('/admin/vehicles/<int:vehicle_id>', methods=['PUT'])
@jwt_required()
def update_vehicle(vehicle_id):
    if not is_admin():
        return jsonify({'message': 'Unauthorized access'}), 403

    data = request.get_json()
    vehicle_type = data.get('type')
    available = data.get('available')

    if not all([vehicle_type, available]):
        return jsonify({'message': 'Missing information'}), 400

    db_operations.update_vehicle(vehicle_id, vehicle_type, available)
    return jsonify({'message': 'Vehicle updated'}), 200


@vehicle_routes.route('/admin/vehicles/<int:vehicle_id>', methods=['DELETE'])
@jwt_required()
def delete_vehicle(vehicle_id):
    if not is_admin():
        return jsonify({'message': 'Unauthorized access'}), 403

    db_operations.delete_vehicle(vehicle_id)
    return jsonify({'message': 'Vehicle deleted'}), 200
