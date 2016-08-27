from channels import Group
from json import dumps

import logging
logger = logging.getLogger(__name__)


def send_notification(msg):
    logger.info('send_notification. notification = %s', msg)
    Group("notifications").send({'text': dumps(msg)})


