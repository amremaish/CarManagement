from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash

from database import db_operations

admin_routes = Blueprint('admin_routes', __name__)


# Helper function to check if the current user is an admin
def is_admin():
    current_user = get_jwt_identity()
    # Replace this logic with your actual admin check logic based on the user role or any other criterion.
    return current_user.get('role') == 'admin' if current_user else False


# Admin route for creating a customer (POST /admin/customers)
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


# Admin route for getting all customers (GET /admin/customers)
@admin_routes.route('/admin/customers', methods=['GET'])
@jwt_required()
def get_all_customers():
    if not is_admin():
        return jsonify({'message': 'Unauthorized access'}), 403

    customers = db_operations.get_all_customers()
    if not customers:
        return jsonify({'message': 'No customers found'}), 404

    return jsonify({'customers': customers}), 200


# Admin route for updating a customer by ID (PUT /admin/customers/<customer_id>)
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


# Admin route for deleting a customer by ID (DELETE /admin/customers/<customer_id>)
@admin_routes.route('/admin/customers/<int:customer_id>', methods=['DELETE'])
@jwt_required()
def delete_customer(customer_id):
    if not is_admin():
        return jsonify({'message': 'Unauthorized access'}), 403

    db_operations.delete_customer(customer_id)
    return jsonify({'message': 'Customer deleted'}), 200

# Similarly, implement CRUD routes for vehicles following a similar structure as above for customers.
# ...

# Add this blueprint to your app
# app.register_blueprint(admin_routes)
