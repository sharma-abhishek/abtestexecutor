# abtestexecutor

Django based app to run the testcases and display the status on the webpage.

User can enter his name as requester and select the environment(dummy) to submit (using AJAX) and run the test cases in background (celery and subprocess). Once the test completes, the result is pushed through websocket (implemented using django-channels).

### Stack Description:

The application is completely build with django, django-rest-framework, celery and django-channels (for websocket support). The database is sqlite and the celery and django-channels are used with redis. pytest is used to execute the test cases. 

As django-channels is used for a websocket support, we are using ASGI interface to communicate with our application. daphne is one of ASGI compatible server with support of web sockets. django-channels uses daphne extensively.




