from apscheduler.schedulers.blocking import BlockingScheduler
import main

sched = BlockingScheduler()


def timed_job():
    main.main()


sched.add_job(timed_job, 'interval', max_instances=3, seconds=10, jitter=1)


sched.start()
