# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import ensure_csrf_cookie
from testrest.models import TaskExecution


def index(request):
    context = RequestContext(request)
    try:
        context["results"] = TaskExecution.objects.all().order_by('-start_time')
    except TaskExecution.DoesNotExist:
        pass
    return render_to_response('index.html', context)


def detail(request, test_id):
    context = RequestContext(request)
    try:
        context['test_detail'] = TaskExecution.objects.get(id=test_id)
    except TaskExecution.DoesNotExist:
        pass

    return render_to_response('detail.html', context)
