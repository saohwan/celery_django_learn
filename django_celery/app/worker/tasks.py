import time

from celery import shared_task


@shared_task(queue='celery')
def add(x, y):
    return x + y


@shared_task(queue='celery')
def dumb():
    return


@shared_task(queue='celery')
def xsum(numbers):
    return sum(numbers)


@shared_task(queue='celery')
def p1():
    time.sleep(5)
    return


@shared_task(queue='celery:1')
def p2():
    time.sleep(5)
    return


@shared_task(queue='celery:2')
def p3():
    time.sleep(5)
    return


@shared_task(queue='celery')
def sleep_task():
    time.sleep(10)
    return


# Synchronous Task
def sync_task():
    result = sleep_task.apply_async()
    print("waiting...")
    print(result.get())


# Asynchronous Task
def async_task():
    result = sleep_task.apply_async()
    print("Not wadditing...")
    print(result.task_id)
