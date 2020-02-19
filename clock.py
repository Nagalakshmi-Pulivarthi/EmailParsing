from apscheduler.schedulers.blocking import BlockingScheduler
from emailapp import ProcessEmail

sched = BlockingScheduler()
@sched.scheduled_job('cron', day_of_week='mon-fri', hour=8,minute=45)
def scheduled_job():
    print('Starting the job:')
    ProcessEmail()
    print('Job executed successfullys.')

sched.start()