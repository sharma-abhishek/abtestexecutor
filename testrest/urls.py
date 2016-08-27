from django.conf.urls import include, url

from rest_framework import routers

from testrest.views import TaskExecutionViewSet

router = routers.DefaultRouter()

router.register(r'execute', TaskExecutionViewSet)

urlpatterns = router.urls