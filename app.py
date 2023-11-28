from flask import Flask

from routes import routes
from schedulers import generate_report, start_scheduler

app = Flask(__name__)

app.register_blueprint(routes)

# start background task
start_scheduler(generate_report, trigger='cron', hour=0, minute=1)

if __name__ == '__main__':
    app.run(debug=True)
