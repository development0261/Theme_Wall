from crontab import CronTab
cron = CronTab(user='root')
job = cron.new(command=)
job.minute.every(1)
cron.write()

def printHello():
    print("Hello")

printHello()