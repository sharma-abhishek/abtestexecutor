from rest_framework import serializers
from models import TaskExecution

# Create your views here.


class TaskExecutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskExecution
        fields = ('id', 'requester', 'start_time', 'end_time', 'status', 'environment_id')