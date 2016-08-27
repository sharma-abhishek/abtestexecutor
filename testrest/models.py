

from django.db import models
from constants import PASS, FAIL, IN_PROGRESS

# Create your models here.


# Class that holds TestExecution Status 
class TaskExecution(models.Model):
    STATUS_CHOICES = (
        (PASS, 'Pass'),
        (FAIL, 'Fail'),
        (IN_PROGRESS, 'In Progress'),
    )
    requester = models.CharField(max_length=30)
    environment_id = models.PositiveSmallIntegerField()
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=IN_PROGRESS)
    log = models.TextField(blank=True, null=True)