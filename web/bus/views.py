#!-*- coding:utf-8 -*-

from django.http import HttpResponse, Http404
from django.shortcuts import render, render_to_response
from models import Coordinate, Route, Bus, Stop
from lib.build_json import render_to_json, return_status
from zq_bus.settings import OUT_WORK_STATUS

RECEIVE_BUS_ID = 'id'
RECEIVE_BUS_LATITUDE = 'latitude'
RECEIVE_BUS_LONGITUDE = 'longitude'

MAX_NUM = 100000

'''
校车GPS发射端
'''



#更新路线


def update_bus_route(request):

    if request.method == 'POST':
        latitude = request.POST.get(RECEIVE_BUS_LATITUDE)
        longitude = request.POST.get(RECEIVE_BUS_LONGITUDE)
        routes = Route.objects.all()
        for r in routes:
            if (abs(r.special_coordinate.latitude - latitude) <= 0.000006) \
                and (abs(r.special_coordinate.longitude - longitude) <= 0.000006):
                Bus.objects.get(request.POST.get(RECEIVE_BUS_ID)).route = r
        else:
            pass
        status = return_status(1)

    elif request.method == 'GET':
        latitude = request.GET.get(RECEIVE_BUS_LATITUDE)
        longitude = request.GET.get(RECEIVE_BUS_LONGITUDE)
        routes = Route.objects.all()
        for r in routes:
            if (abs(r.special_coordinate.latitude - latitude) <= 0.000006) \
                and (abs(r.special_coordinate.longitude - longitude) <= 0.000006):
                Bus.objects.get(request.GET.get(RECEIVE_BUS_ID)).route = r
        else:
            pass
        status = return_status(1)
    else:
        status = return_status(0)
        return render_to_json(status)

#更新校车所属站点


def update_bus_stop(request, bus, latitude, longitude):

    try:
        stops = Stop.objects.filter(route=bus.route)
        distance = (bus.coordinate.latitude - bus.stop.latitude)**2 + \
                   (bus.coordinate.longitude - bus.stop.latitude)**2
        for stop in stops:
            temp_distance = (bus.coordinate.latitude - stop.latitude)**2 + \
                            (bus.coordinate.longitude - stop.longitude)**2
            if temp_distance<distance:
                bus.stop = stop
                break
        else:
            bus.stop = bus.stop
        status = return_status(1)
    except:
        status = return_status(0)
        return render_to_json(status)


#更新校车位置


def update_bus_position(request):
    if request.method == 'POST':
        try:
            bus = Bus.objects.get(number=request.POST.get(RECEIVE_BUS_ID))
            bus.update_position(request)
            update_bus_route(request)
            update_bus_stop(request)
            status = return_status(1)
            return render_to_json(status)
        except:
            status = return_status(0)
            return render_to_json(status)
    elif request.method == 'GET':
        try:
            bus = Bus.objects.get(number=request.GET.get(RECEIVE_BUS_ID))
            bus.update_position(request)
            update_bus_route(request)
            update_bus_stop(request)
            status = return_status(1)
            return render_to_json(status)
        except:
            status = return_status(0)
            return render_to_json(status)
    else:
        status = return_status(0)
        return render_to_json(status)

'''
APP接收端
'''

#返回校车数据
def get_bus_info(request):
    if request.method == 'POST':
        try:
            route_id = int(request.POST.get('route_id'))
            route = Route.objects.get(id=route_id)
            buses = Bus.objects.filter(route=route)
            data = dict()
            a = list()
            num = 0
            for i in buses:
                temp = {
                    'id': i.number,
                    'route_id': route_id,
                    'longitude': i.coordinate.longitude,
                    'latitude': i.coordinate.latitude,
                    'stop': i.stop.name,
                    'arrive_time': i.stop.arrive_time,
                }
                a.append(temp)
                num += 1
            data = {
                'status': 1,
                'bus_info': a,
                'num': num,
            }
            return render_to_json(data)
        except:
            status = return_status(0)
            return render_to_json(status)
    elif request.method == 'GET':
        try:
            route_id = int(request.GET.get('route_id'))
            route = Route.objects.get(id=route_id)
            buses = Bus.objects.filter(route=route)
            data = dict()
            a = list()
            num = 0
            for i in buses:
                temp = {
                    'id': i.id,
                    'route_id': route_id,
                    'longitude': i.coordinate.longitude,
                    'latitude': i.coordinate.latitude,
                    'stop': i.stop.name,
                    'arrive_time': i.stop.arrive_time,
                }
                num += 1
                a.append(temp)
            data = {
                'status': 1,
                'bus_info': a,
            'num': num,
            }
            return render_to_json(data)
        except:
            status = return_status(0)
            return render_to_json(status)
    else:
        status = {
            'status': 0
        }
        return render_to_json(status)


#获取所在位置


def return_user_position(request):
    if request.method == 'POST':
        try:
            latitude = float(request.POST.get('latitude'))
            longitude = float(request.POST.get('longitude'))
            route_id = int(request.POST.get('route_id'))
            route = Route.objects.get(id=route_id)
            stops = Stop.objects.filter(route=route)
            distance = MAX_NUM
            data = dict()
            if stops.exists():
                stop = stops[0]
            for i in stops:
                temp_distance = (i.latitude - latitude)**2+(i.longitude - longitude)**2
                if temp_distance < distance:
                    distance = temp_distance
                    stop = i
            stop_name = stop.name
            stop_longitude = stop.longitude
            stop_latitude = stop.latitude
            stop_arrive_time = stop.arrive_time
            data = {
                'status': 1,
                'name': stop_name,
                'longitude': stop_longitude,
                'latitdue': stop_latitude,
                'arrive_time': stop_arrive_time,
            }
            return render_to_json(data)
        except:
            status = return_status(0)
            return render_to_json(status)

    elif request.method == 'GET':
        try:
            latitude = float(request.GET.get('latitude'))
            longitude = float(request.GET.get('longitude'))
            route_id = int(request.GET.get('route_id'))
            route = Route.objects.get(id=route_id)
            stops = Stop.objects.filter(route=route)
            distance = MAX_NUM
            data = dict()
            if stops.exists():
                stop = stops[0]
            else:
                status = return_status(0)
                return render_to_json({'dde':11})
            for i in stops:
                temp_distance = (i.latitude - latitude)**2+(i.longitude - longitude)**2
                if temp_distance < distance:
                    distance = temp_distance
                    stop = i
            stop_name = stop.name
            stop_longitude = stop.longitude
            stop_latitude = stop.latitude
            stop_arrive_time = stop.arrive_time
            data = {
                'status': 1,
                'name': stop_name,
                'longitude': stop_longitude,
                'latitdue': stop_latitude,
                'arrive_time': stop_arrive_time,
            }
            return render_to_json(data)
        except:
            status = return_status(0)
            return render_to_json(status)
    else:
        status = return_status(0)
        return render_to_json(status)

#返回线路

def return_route(request):
    try:
        routes = Route.objects.all()
        route_list = list()
        for i in routes:
            route = {
                'id': i.id,
                'departure': i.departure_stop,
                'final': i.final_stop,
            }
            route_list.append(route)
        data = {
            'route_list':route_list
        }
        return render_to_json(data)
    except:
        status = return_status(0)
        return render_to_json(status)
