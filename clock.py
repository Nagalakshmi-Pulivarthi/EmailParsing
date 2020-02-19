from apscheduler.schedulers.blocking import BlockingScheduler
from emailapp import ProcessEmail
import os

hours=os.environ['Schedule'].split(":")[0]
mins=os.environ['Schedule'].split(":")[1]

sched = BlockingScheduler()
@sched.scheduled_job('cron', day_of_week='mon-fri', hour=hours,minute=mins)
def scheduled_job():
    print('Starting the job:')
    ProcessEmail()
    print('Job executed successfullys.')


sched.start()