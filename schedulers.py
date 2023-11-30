from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, time
from database import db_operations


def generate_report():
    today = datetime.now().date().strftime('%Y-%m-%d')
    bookings = db_operations.get_bookings_for_day(today)

    print(f"Bookings for {today}:")
    for booking in bookings:
        print(booking)


def start_scheduler(scheduler_fun, trigger='cron', hour=0, minute=1):
    scheduler = BackgroundScheduler()
    scheduler.add_job(scheduler_fun, trigger, hour=hour, minute=minute)
    scheduler.start()
