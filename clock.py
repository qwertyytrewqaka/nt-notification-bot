from apscheduler.schedulers.blocking import BlockingScheduler
import main
import constants

sched = BlockingScheduler()


def timed_job():
    main.main()

sched.add_job(timed_job, 'interval', seconds=20, jitter=1)


sched.start()
