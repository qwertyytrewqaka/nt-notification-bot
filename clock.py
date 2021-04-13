from apscheduler.schedulers.blocking import BlockingScheduler
import main

sched = BlockingScheduler()


def timed_job():
    main.main()


sched.add_job(timed_job, 'interval', seconds=10, max_instances=3, jitter=1)


sched.start()
