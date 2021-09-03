from apscheduler.schedulers.blocking import BlockingScheduler

# Main cronjob function.
from crons import printHello

# Create an instance of scheduler and add function.
scheduler = BlockingScheduler()
scheduler.add_job(printHello, "interval", seconds=30)

scheduler.start()