
from celery import shared_task
from runner import execute_test


@shared_task
def schedule_test_execution(task_execution):
    return execute_test(task_execution)



    



