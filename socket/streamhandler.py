#! -*- coding:utf-8 -*-
import traceback
import socket
import struct
import MySQLdb
import os
import sys
import urllib

PROJECT_DIR_PATH = '/www/zq_bus/web'
sys.path.append(PROJECT_DIR_PATH)
os.environ['DJANGO_SETTINGS_MODULE'] = 'zq_bus.settings'

from lib.hexadecimal_deal import DataStruct
from zq_bus import settings
from bus.models import *

from SocketServer import ThreadingTCPServer, StreamRequestHandler


class BusStreamRequestHandler(StreamRequestHandler):

    packed_data = str()

    def judge_data_type(self):
        
        '''
        判断包类型
        '''

        if self.packed_data[0]==104 and self.packed_data[1]==104:
            pass
#            print 'ok'
        elif self.packed_data[0]==0 and self.packed_data[1]==0:
            response_str = 'bbbbb'
            response_data = struct.pack(response_str, 84, 104, 26, 13, 10)
            self.request.sendall(response_data)
            print 'return right'
        else:
            pass
    def update_bus_coordinate(self, data, bus):
        '''
        更新车辆坐标
        '''

        coordinate = Coordinate(longitude=data['longitude'],
        latitude=data['latitude'],bus_number=data['bus_number'])
        coordinate.save()
        bus.coordinate = coordinate
        bus.save()

    def update_bus_stop(self, data, bus):
        '''
        更新车站
        '''

        MAX_LENGTH = 21000000

        stops = Stop.objects.filter(route=bus.route)
        distance = MAX_LENGTH
        for stop in stops:
            temp_distance = ((bus.coordinate.latitude - stop.latitude)**2+\
               (bus.coordinate.longitude - stop.longitude)**2)
            if distance < temp_distance:
                bus.stop = stop
        bus.save()

    def update_bus_route(self, data, bus):
        '''
        更新车辆路线
        '''

        ERROR_VALUE =0.00007

        routes = Route.objects.all()
        for r in routes:
            if (abs(r.special_coordinate.latitude - data['latitude'])<ERROR_VALUE)\
                and (abs(r.special_coordinate.longitude -
                data['longitude']<ERROR_VALUE)):

                bus.route = r
        bus.save()

    def register_new_bus(self,data):
#        if SpecialCoordinate.objects.filter(route_name='TEST'):
#            special_coordinate = SpecialCoordinate.objects.get(route_name='TEST')
#        else:
#            special_coordinate = SpecialCoordinate(longitude=114.332141, latitude=30.520142, route_name='TEST')
#            special_coordinate.save()
#
#        if Route.objects.filter(final_stop="TEST2"):
#            route = Route.objects.get(departure_stop='TEST1', final_stop='TEST2',special_coordinate = special_coordinate)
#        else:
#            route = Route.objects.get(final_stop='TEST2')
#            route.save()
#
#        if Stop.objects.filter(name='TEST'):
#            stop = Stop.objects.get(name='TEST')
#        else:
#            stop = Stop(name='TEST', route=route, longitude=114.233333, latitude=30.520212)
#            stop.save()
        try:
            coordinate = Coordinate.objects.all()[0]
        except:
            coordinate =Coordinate(longitude = 114.233333,latitude = 30.5312333)
            coordinate.save()
        route = Route.objects.all()[0]
        stop = Stop.objects.filter(route=route)[0]
        bus = Bus(route=route, stop=stop, coordinate=coordinate, number=data['bus_number'])
        bus.save()
        return bus

    def save(self, data):
        '''
        数据库存储
        '''
        bus = str()
        try:
            if Bus.objects.filter(number=data['bus_number']):
	        bus = Bus.objects.get(number=data['bus_number'])
            else:
		bus = self.register_new_bus(data)
            self.update_bus_coordinate(data, bus)
            self.update_bus_route(data, bus)
            if bus.route:
                self.update_bus_stop(data, bus)
        except:
            pass

    def temp_save(self, data):
        test_coordinate = TestCoordinate(latitude=data['latitude'], longitude=data['longitude'])
        test_coordinate.save()
        print 'time:', test_coordinate.time, '; lat:', test_coordinate.latitude, '; lont:', test_coordinate.longitude


    def packdata(self, data):

        start = DataStruct('bb')
        length = DataStruct('b')
        LAC = DataStruct('H')
        terminal_id = DataStruct('bbbbbbbb')
        info_code = DataStruct('h')
        agreement_code = DataStruct('b')
        datetime = DataStruct('bbbbbb')
        latitude = DataStruct('bbbb')
        longitude = DataStruct('bbbb')
        speed = DataStruct('b')
        direction = DataStruct('bb')
        MNC = DataStruct('b')
        cell_id = DataStruct('h')
        status = DataStruct('bbbb')
        end = DataStruct('bb')
        if len(data)==0:
            return (0, 0)
        if data[0] == 'h' and data[1] == 'h':
            print 'ok'
        else:
            return (0, 0)
        if data[2] == '%':
            print 'position_update'
        else:
            print 'live_confirm'
            return (0, 0)

        form_string = 'B' * len(data) 
        try:
            packed_data = struct.unpack(form_string, data)
        except:
            return (0, 0)
        bus_number = str()
        for i in range(5, 13):
            temp_str = str(packed_data[i]/16)+str(packed_data[i]%16)
            bus_number += str(temp_str)

        latitude = packed_data[22] * (256 ** 3) + packed_data[23] * (256 ** 2) + packed_data[24] * 256 + packed_data[25]
        latitude = (latitude + 0.0) / (30000*60)
        longitude = packed_data[26] * (256 ** 3) + packed_data[27] * (256 ** 2) + packed_data[28] * 256 + packed_data[29]
        longitude = (longitude + 0.0) / (30000*60)

#       百度地图API
        transform_url = "http://api.map.baidu.com/geoconv/v1/?coords=" + str(longitude) + \
                     "," + str(latitude) + "&from=1&to=5&ak=7yTvUeESUHB7GTw9Pb9BRv1U"

        print transform_url
        transform_data = urllib.urlopen(transform_url).read()
#        print transform_data
        try:
            transform_data = eval(transform_data)['result'][0]
            latitude = transform_data['y']
            longitude = transform_data['x']
        except:
            print 'error'
#       高德地图API
#        transform_url = "http://api.zdoz.net/transgps.aspx?"+ \
#        "lat=" + str(latitude) + "&lng=" + str(longitude)
#        print transform_url
#        transform_data = urllib.urlopen(transform_url).read()
#        print transform_data
#        try:
#            transform_data = eval(transform_data)
#            latitude = transform_data['Lng']
#            longitude = transform_data['Lat']
#        except:
#            print 'error'
        latitude =  float(latitude)
        longitude = float(longitude)

        data = {
            'bus_number': bus_number,
            'latitude': latitude,
            'longitude': longitude,
        }
        print data

        #存储更新坐标数据
        self.save(data)

        #测试坐标数据
        self.temp_save(data)

        return packed_data


    def handle(self):

        while True:
            try:
                data = self.request.recv(1024)
                temp_data = ""
                if len(data)==0:
                    temp_data += data
                else:
         	    print "len(data): %d" % (len(data))
	            print data
		    self.packed_data = self.packdata(data)
		    self.judge_data_type()
            except:
                traceback.print_exc()
                break
