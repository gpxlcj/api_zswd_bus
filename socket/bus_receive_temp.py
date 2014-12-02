# -*-coding:utf-8 -*-
import socket
import struct
import MySQLdb
import os, sys
import urllib

'''
HOST = '0.0.0.0'
PORT = 8080
BUFSIZ = 1024

address = (HOST, PORT)
tcpSerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpSerSock.bind(address)
tcpSerSock.listen(5)
'''
class DataStruct:

    data_type = ''
    def __init__(self, temp_type):
        data_type = temp_type
def update_bus_coordinate(data,bus):
    coordinate = Coordinate(longitude=data['longitude'],
    latitude=data['latitude'],bus_number=data['bus_number'])
    coordinate.save()
    bus.coordinate = coordinate
    bus.save()

def update_bus_stop(data, bus):

    MAX_LENGTH = 21000000

    stops = Stop.objects.filter(route=bus.route)
    distance = MAX_LENGTH
    for stop in stops:
        temp_distance = ((bus.coordinate.latitude - stop.latitude)**2+\
               (bus.coordinate.longitude - stop.longitude)**2)
        if distance < temp_distance:
            bus.stop = stop
    bus.save()
       
def update_bus_route(data, bus):
    ERROR_VALUE =0.000006

    routes = Route.objects.all()
    for r in routes:
        if (abs(r.special_coordinate.latitude - data['latitude'])<ERROR_VALUE)\
            and (abs(r.special_coordinate.longitude -
            data['longitude']<ERROR_VALUE)):

            bus.route = r
    bus.save()


def datasave(data):
    try:
        try:
            bus = Bus.objects.get(number= data['bus_number'])
        except:
            route = Route.objects.get(id=1)
            bus = Bus(number = data['bus_number'], route=route)
        update_bus_coordinate(data, bus)
        update_bus_route(data, bus)
        update_bus_stop(data, bus)
        print 'update success'
    except:
        pass        

def packdata(data):
     
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
    MNC =DataStruct('b')
    cell_id = DataStruct('h')
    status = DataStruct('bbbb')
    end = DataStruct('bb')
    print data,type(data)
    if data[0]=='h' and data[1]=='h':
        print 'ok'
    else:
        return (0,0)
    if data[2]=='%':
        print 'second'
    else:
        return (0,0)
    
    form_string = 'B'*len(data)
    print form_string
    packed_data = struct.unpack(form_string, data)
  #  data_save()
    print packed_data
    bus_number = ''
    for i in range(5,13):
        bus_number += str(packed_data[i])

    latitude = packed_data[22]*(256**3)+packed_data[23]*(256**2)+packed_data[24]*256+packed_data[25]
    latitude = (latitude+0.0)/30000
    longitude = packed_data[26]*(256**3)+packed_data[27]*(256**2)+packed_data[28]*256+packed_data[29]
    longitude = (longitude+0.0)/30000
    transform_url = "http://api.map.baidu.com/geoconv/v1/?coords="+str(longitude)+\
    str(latitude)+","+str(longitude)+"&from=1&to=5&ak=7yTvUeESUHB7GTw9Pb9BRv1U"
    print transform_url
    transform_data = urllib.urlopen(transform_url).read()
    print transform_data
    try:
        transform_data = eval(transform_data)['result'][0]
        latitude = transform_data['y']
        longitude = transform_data['x'] 
    except:
        print 'error'
    data = {
            'bus_number':bus_number,
            'latitude':latitude,
            'longitude':longitude,
        }
    print data
#    datasave(data)
    return packed_data

def main():

    HOST = '127.0.0.1'
    PORT = 8080
    BUFSIZ = 1024
    ADDR = (HOST, PORT)

    tcpSerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpSerSock.bind(ADDR)
#    tcpSerSock.listen(5)

    while True:
#        HOST = '127.0.0.1'
#        PORT = 8080
#        BUFSIZ = 64
#        ADDR = (HOST, PORT)
#        tcpSerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#        tcpSerSock.bind(ADDR)
        tcpSerSock.listen(5)
        print 'waiting for connection...'
        tcpCliSock, addr = tcpSerSock.accept()
        print '...connected from:', addr
        try:
            while True:
                data = tcpCliSock.recv(BUFSIZ)
                if not data:
                    break
                else:
                    packed_data = packdata(data)
                    if packed_data[0]==104 and packed_data[1]==104:
                        print 'ok'
            tcpCliSock.close()
        except:
            tcpCliSock.close()
    tcpSerSock.close()

from SocketServer import ThreadingTCPServer, StreamRequestHandler
import traceback

class BusStreamRequestHandler(StreamRequestHandler):
    def handle(self):
        while True:
            try:
#                data = self.rfile.readline()
                data = self.request.recv(1024)
                print len(data)
                print "receive from (%r):%r" %(self.client_address, data)
                packed_data = packdata(data)
                if packed_data[0]==104 and packed_data[1]==104:
                    print 'ok'
                elif packed_data[0]==0 and packed_data[1]==0:
                    num = len(data)
                    format_str = 'B' * num
                    ans_num = struct.unpack(format_str, data)
                    print '------------------------------------------\n'
                    print ans_num
                    print '------------------------------------------\n'
                    response_str = 'BBBBB'
                    response_data = struct.pack(response_str, 84, 104, 26, 13, 10)
                    print response_data
                    self.request.sendall(response_data)
                else:
                    pass
            except:
                traceback.print_exc()
                break





if __name__ == '__main__':
    PROJECT_DIR_PATH = '/www/zq_bus/web'
    sys.path.append(PROJECT_DIR_PATH)
    os.environ['DJANGO_SETTINGS_MODULE'] = 'zq_bus.settings'
    from zq_bus import settings
    from bus.models import *
    HOST = '0.0.0.0'
    PORT = 8080
    BUFSIZ = 1024
    ADDR = (HOST, PORT)
    server = ThreadingTCPServer(ADDR, BusStreamRequestHandler)
    server.serve_forever()
#    main()
