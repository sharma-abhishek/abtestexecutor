# abtestexecutor

Django based app to run the testcases and display the status on the webpage.

User can enter his name as requester and select the environment(dummy) to submit (using AJAX) and run the test cases in background (celery and subprocess). Once the test completes, the result is pushed through websocket (implemented using django-channels).

### Stack Description:

The application is completely build with django, django-rest-framework, celery and django-channels (for websocket support). The database is sqlite and the celery and django-channels are used with redis. pytest is used to execute the test cases. 

As django-channels is used for a websocket support, we are using ASGI interface to communicate with our application. daphne is one of ASGI compatible server with support of web sockets. django-channels uses daphne extensively.

### Installation

Please install following packages at system level before proceeding further:

```
sudo apt-get install python-pip
```

Install redis-server in your machine.

```
pip install pytest
```

The application dependencies are listed in the ```requirements.txt``` file.

Below are the steps to configure and install it on your local machine:

- Create a virtualenv to have an isolated virtual environment for this application and to install all the dependencies using the below command:

```virtualenv env```

- Activate the virtualenv using below command:

```source env/bin/activate```

- Go the application root folder where the requirements.txt is and execute following command to install all the dependencies:

```pip install –r requirements.txt```

Once the requirements are installed successfully, execute the commands listed below sequentially from the same folder (where requirements.txt is.)

The below command will create the sqlite data and apply the migrate to create the tables.

```python manage.py migrate```

Start a redis server (if not started already) as a service or in a separate terminal tab and make sure its always running while you use/test this application.

```sudo redis-server```

Once the redis-server is up and running, execute the below commands one by one in new terminal tab and in same virtualenv and directory (where the requirements.txt is).

```daphne abtestexecutor.asgi:channel_layer```

```celery -A abtestexecutor worker -l info```

```python manage.py runworker```

The application should now be up and running on 127.0.0.1:8000




