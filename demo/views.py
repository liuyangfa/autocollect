# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import sys

from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from django.apps import apps
from models import Physical, Items
from tasks import collectdata

reload(sys)
sys.setdefaultencoding('utf-8')


User

def welcome(request):
    pList = Physical.objects.all()
    # print pList
    messages.add_message(request, level=messages.INFO, message="成功了")
    print apps.get_app_config('demo').models
    return render(request, 'index.html', {"lists": pList})
    # return HttpResponse(Items.objects.all().filter(id=10))
    # if request.user.is_authenticated():
    #     return HttpResponse("当前用户登录了")
    # else:
    #     return HttpResponse("没有登录" + html)


def index(request, id):
    print id
    if id == None:
        return HttpResponse(json.dumps({'ERROR': '没有传入值'}))
    else:
        data = list(Items.objects.order_by('-id').filter(i_parent=id).all().values())
        return HttpResponse(json.dumps(data), content_type='application/json')


def getdata(request):
    requestset = Physical.objects.filter(type="1")
    result = collectdata.delay(requestset)
    physical = Physical.objects.filter(type="1").all()
    return HttpResponse(json.dumps({"result": result.id}))
