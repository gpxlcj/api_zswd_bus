#! -*- coding:utf-8 -*-
from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.utils import simplejson
from bus2.models import *

def render_json(dict):

    json = simplejson.dumps(dict, ensure_ascii = False)
    mimetype = 'application/json'
    return HttpResponse(json, mimetype = mimetype)

#返回用户车辆设备位置
def return_positiondata(request):
    position = []
    for i in Bus.objects.all():
        newlongitude = i.bus_nowposition.longitude
        newlatitude = i.bus_nowposition.latitude
        position.append({'bus_id':i.bus_id,'bus_type':i.bus_type,'longitude':newlongitude,'latitude':newlatitude,'accuracy':i.bus_accuracy,'speed':i.bus_speed})
    return render_json({'position':position})

