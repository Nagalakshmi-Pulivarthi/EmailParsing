from apscheduler.schedulers.blocking import BlockingScheduler
from emailapp import ProcessEmail
import os

schedule= os.environ['Schedule']
print('Schedule:' + schedule)
hours=schedule.split(':')[0]
mins=schedule.split(':')[1]

print('hours:' + hours)
print('mins:' + mins)

sched = BlockingScheduler()

@sched.scheduled_job('cron', day_of_week='mon-fri', hour=hours,minute=mins, , timezone='America/New_York')
def scheduled_job():
    print('Starting the job:')
    ProcessEmail()
    print('Job executed successfullys.')

sched.start()
