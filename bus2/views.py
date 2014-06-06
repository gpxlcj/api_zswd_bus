#! -*- coding:utf-8 -*-

from random import randint,choice
import re

from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.utils import simplejson
from django.core.mail import send_mail

from bus2.models import *
from bus2.json import render_json, return_positiondata

from poststatus import RenRenParser 

def test(request):
    return render_to_response('bus.html',locals())
    return render_to_response('register.html',locals())

#用户车辆信息接收
def userreceive(request):
    if request.method=="GET":
        return return_positiondata(request)
    return render_json({'status':'0'})
#树洞测试
def renren(request):
    if request.method=="POST":
        if request.POST.get('content'):
            content = u''+request.POST.get('content')
            renrenp = RenRenParser('gpxlcj@gmail.com','gg101224')
            content = content.encode('utf-8')
            renrenp.login()
            renrenp.publish(content)
        return HttpResponse("发布成功")
    return render_to_response('shudong.html')

