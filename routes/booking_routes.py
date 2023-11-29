from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, JWTManager
from database import db_operations
import datetime

booking_routes = Blueprint('booking_routes', __name__)


@booking_routes.route('/make_booking', methods=['POST'])
@jwt_required()
def make_booking():
    current_user_email = get_jwt_identity()
    user = db_operations.get_user_by_email(current_user_email)
    if not user:
        return jsonify({'message': 'Customer not found or unauthorized'}), 401

    data = request.get_json()
    vehicle_id = data.get('vehicle_id')
    date_hired = data.get('date_hired')
    date_returned = data.get('date_returned')

    if not all([vehicle_id, date_hired, date_returned]):
        return jsonify({'message': 'Missing parameters'}), 400

    try:
        date_hired = datetime.datetime.strptime(date_hired, '%Y-%m-%d')
        date_returned = datetime.datetime.strptime(date_returned, '%Y-%m-%d')
    except ValueError:
        return jsonify({'message': 'Invalid date format. Use YYYY-MM-DD'}), 400

    if date_hired >= date_returned:
        return jsonify({'message': 'Invalid date range. date_hired must be before date_returned'}), 400

    # date range validations
    max_booking_duration = datetime.timedelta(days=7)  # Maximum allowed booking duration (7 days)
    if (date_returned - date_hired) > max_booking_duration:
        return jsonify({'message': 'Maximum booking duration exceeded (7 days limit)'}), 400

    if db_operations.check_availability(vehicle_id, date_hired, date_returned):
        return jsonify({'message': 'Vehicle is not available for the selected dates'}), 400

    customer_id = db_operations.get_user_id_by_email(current_user_email)

    db_operations.insert_booking(customer_id, vehicle_id, date_hired.date(), date_returned.date())
    return jsonify({'message': 'Booking successful'})
