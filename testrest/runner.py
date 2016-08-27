import logging
import os
import subprocess
from datetime import datetime
from constants import PASS, FAIL
from django.conf import settings
from notify import send_notification

logger = logging.getLogger(__name__)


base_location = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# hardcoded test files, as of now.
# TODO: walk through tests directory to read all the files programatically
def get_test_files():
    test_files = [os.path.join(base_location, 'testrest/tests/test_1.py'),
    os.path.join(base_location, 'testrest/tests/test_2.py'),
    os.path.join(base_location, 'testrest/tests/test_3.py'),
    os.path.join(base_location, 'testrest/tests/test_4.py')]
    return test_files


def execute_test(task_execution):
    # Get all the test files to execute
    test_files = get_test_files()
   
    try:
        # open a suprocess to execute all test cases with py.test
        process_output = subprocess.check_output("py.test -s -vv %s" % ' '.join(test_files),
                                         stderr=subprocess.STDOUT,
                                         shell=True)
        # if there is no error, set the task execution status to PASS
        task_execution.status = PASS
    except subprocess.CalledProcessError as e:
        # set the error to process_outut in case of suprocess error
        process_output = e.output
        # mark the status as FAIL
        task_execution.status = FAIL

    # update the log field of the model with the process output
    task_execution.log = process_output
    # set the end_time of the task
    task_execution.end_time = datetime.now()
    # update the model with the status.
    task_execution.save()
    # send notification over websocket
    send_notification({'id' : task_execution.id, 
                'requester' : task_execution.requester, 'environment_id' : task_execution.environment_id,
                'status' : task_execution.status, 'log' : task_execution.log})