import os
from datetime import timedelta

from flask import Flask
from flask_jwt_extended import JWTManager

from routes.admin_routes import admin_routes, vehicle_routes
from routes.auth_routes import auth_routes
from routes.booking_routes import booking_routes
from schedulers import generate_report, start_scheduler

app = Flask(__name__)
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config['JWT_HEADER_TYPE'] = 'Bearer'
app.config['JWT_HEADER_NAME'] = 'Authorization'
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET")
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=int(os.getenv("JWT_EXPIRE_TIME")))
jwt = JWTManager(app)

app.register_blueprint(auth_routes)
app.register_blueprint(booking_routes)
app.register_blueprint(admin_routes)
app.register_blueprint(vehicle_routes)

# start background task
start_scheduler(generate_report, trigger='cron', hour=0, minute=1)

if __name__ == '__main__':
    app.run(debug=True)
