#!/usr/bin/env python
# coding: u8

import atexit

from apscheduler.scheduler import Scheduler

import env
env.setup()


sched_master = Scheduler(daemon=False, misfire_grace_time=60 * 20)


@sched_master.interval_schedule(seconds=1)
def send_email_from_redis_queue():
    sched_master.unschedule_job(send_email_from_redis_queue.job)


def start_master():
    atexit.register(lambda: sched_master.shutdown(wait=False))
    sched_master.start()


def init_first():
    """For local development, you'd run this function first!"""
    # call all the schedulers here


if __name__ == '__main__':
    init_first()
