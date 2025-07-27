from apscheduler.schedulers.background import BackgroundScheduler
from .update import is_date_end


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(is_date_end, 'cron', hour=12, minute=00)
    scheduler.start()