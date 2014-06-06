#! -*- coding:utf-8 -*-

from random import randint,choice
import re
import md5

from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.utils import simplejson
from django.core.mail import send_mail

from bus2.models import *
from bus2.json import render_json, return_positiondata

MYERROR = {'status':'0'}
MYSUCCESS = {'status':'1'}

#建立新的车辆设备
def buildnewbus(request):
    if request.method == 'POST':
        if request.POST.get('bus_id'):
            newbus_id = int(request.POST.get('bus_id'))
            nowposition = NowPosition(longitude = 0, latitude =0, time = 0)
            nowposition.save()
            newbus = Bus(bus_id = newbus_id,bus_nowposition = nowposition,bus_type = 0)
            newbus.save()
            return render_json(MYSUCCESS)
        else:
            return render_json(MYERROR)
    else:
        return render_json(MYERROR)

#即时获取车辆位置
def getbusposition(request,test):
    if request.method == 'POST':
        if request.POST.get('bus_id'):
            newbus_id = request.POST.get('bus_id')
        else:
            return render_json(MYERROR)
        if request.POST.get('latitude'):
            try:
                new_latitude = float(request.POST.get('latitude'))
            except:
                return render_json(MYERROR)
        else:
            return render_json(MYERROR)
        if request.POST.get('longitude'):
            try:
                new_longitude = float(request.POST.get('longitude'))
            except:
                return render_json(MYERROR)
        else:
            return render_json(MYERROR)
        if request.POST.get('time'):
            new_time = request.POST.get('time')
        else:
            return render_json(MYERROR)
#        if request.POST.get('excalibur'):
#            try:
#                post_hash = request.POST.get('excalibur')
#                new_hash = md5.new()
#                new_hash.update(new_time[len(new_time)-6:])
#                new_hash_value = new_hash.hexdigest()
#                new_hash.update(str(new_hash_value))
#                new_hash_value = new_hash.hexdigest()
#                if str(new_hash_value)==post_hash:
#                    pass
#                else:
#                    return render_json(MYERROR)
#            except:
#                return render_json(MYERROR)
#        else:
#            return render_json(MYERROR)
        if request.POST.get('accuracy'):
            new_accuracy = float(request.POST.get('accuracy'))
        else:
            new_accuracy = 0.0
        if request.POST.get('speed'):
            new_speed = float(request.POST.get('speed'))
        else:
            new_speed = 0.0
        new_nowposition = NowPosition(latitude = new_latitude, longitude = new_longitude, time = new_time)
        new_nowposition.save()
        try:
            bus = Bus.objects.get(bus_id = newbus_id)
            position = Position(latitude = bus.bus_nowposition.latitude, longitude = bus.bus_nowposition.longitude, time = bus.bus_nowposition.time)
            position.save()
            bus.bus_position.add(position)
            bus.bus_nowposition.delete()
            bus.bus_nowposition = new_nowposition
            bus.bus_speed = new_speed
            bus.bus_accuracy = new_accuracy
            bus.save()
            return render_json(MYSUCCESS)
        except:
            return render_json(MYERROR)
    else:
        return render_json(MYERROR)
#改变汽车设备的名称
def editbusname(request):
    if request.method == 'POST':
        if request.POST.get('bus_id'):
            newbus_id = request.POST.get('bus_id')
        else:
            return render_json(MYERROR)
        if request.POST.get('bus_type'):
            newbus_type = int(request.POST.get('bus_type'))
        else:
            return render_json(MYERROR)
        try:
            bus = Bus.objects.get(bus_id = newbus_id)
            bus.bus_type = newbus_type
            bus.save()
            return render_json(MYSUCCESS)
        except:
            return render_json(MYERROR)
    else:
        return render_json(MYERROR)
