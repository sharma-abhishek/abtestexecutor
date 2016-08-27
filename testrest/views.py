

from rest_framework import viewsets, status
from rest_framework.response import Response
from models import TaskExecution
from serializers import TaskExecutionSerializer
from tasks import schedule_test_execution
import constants as RunningStatus

class TaskExecutionViewSet(viewsets.ModelViewSet):
    model = TaskExecution
    serializer_class = TaskExecutionSerializer
    queryset = TaskExecution.objects.all()


    def create(self, request):
        
        # read requester from request payload if pass, else set it to None        
        requester = request.POST.get('requester', None)

        # read environment_id from request payload if pass, else set it to None`
        environment_id = request.POST.get('environment_id', None)

        # check if requester exists, if not return bad request
        if not requester:
            return Response({'message' : 'Invalid Requester'}, status = status.HTTP_400_BAD_REQUEST)

        # check if environment_id exists, if not return bad request
        if not environment_id:
            return Response({'message' : 'Invalid Environment ID'}, status = status.HTTP_400_BAD_REQUEST)

        # trying to find task_execution_object whose running status is in progress
        task_execution_object = TaskExecution.objects.filter(environment_id=environment_id, status = RunningStatus.IN_PROGRESS)

        # if task_execution_object found, then return bad request for already running task under a specific environment
        if task_execution_object:
            return Response({'message' : 'Test execution is in progress under this environment'}, status = status.HTTP_400_BAD_REQUEST)

        # Create an entry for task execution with passed requester and environment_id and set the running status to IN_PROGRESS
        task_execution = TaskExecution(requester=requester, environment_id = environment_id, status = RunningStatus.IN_PROGRESS)
        
        # save the task_execution object in db
        task_execution.save()

        #call a celery task to open a subprocess for task execution
        schedule_test_execution.delay(task_execution)

        # preparing json to send data.
        result = { 'id' : task_execution.id, 'requester' : task_execution.requester, 
                   'environment_id' : task_execution.environment_id, 'start_time' : task_execution.start_time,
                   'status'  :task_execution.status}

        # Return successful response indicating that task execution request is accepted under this environment.        
        return Response({'message' : 'Test execution request accepted', 'result' : result}, status = status.HTTP_201_CREATED)




