from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger


def saludar():
    print('hola')


scheduler = BlockingScheduler()
scheduler.add_job(
    func=saludar,
    trigger=CronTrigger.from_crontab('* * * * *')
)

scheduler.start()
scheduler.start()
