# -*-coding:utf-8 -*-
import socket
import struct
import MySQLdb
import os, sys


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
        bus = Bus.objects.get(number= data['bus_number'])
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
#    get_data_type = struct.Struct('bb').unpack(data)
    if data[0]=='h' and data[1]=='h':
        print 'ok'
    else:
        return (0,0)
    if data[2]=='%':
        print 'second'
    else:
        return (0,0)
    
#    form_string = start.data_type+length.data_type+LAC.data_type+terminal_id.data_type+info_code.data_type+agreement_code.data_type+\
#           datetime.data_type+latitude.data_type+longitude.data_type+speed.data_type+\
#           direction.data_type+MNC.data_type+cell_id.data_type+\
#           status.data_type+end.data_type
    form_string = 'b'*42
    print form_string
    packed_data = struct.unpack(form_string, data)
  #  data_save()
    print packed_data
    bus_number = ''
    for i in range(5,13):
        bus_number += str(packed_data[i])
    latitude = packed_data[22]*(256**3)+packed_data[23]*(256**2)+packed_data[24]*256+packed_data[25]
    latitude = (latitude+0.0)/3000
    longitude = packed_data[26]*(256**3)+packed_data[27]*(256**2)+packed_data[28]*256+packed_data[29]
    longitude = (longitude+0.0)/3000
    data = {
            'bus_number':bus_number,
            'latitude':latitude,
            'longitude':longitude,
        }
    print data
    datasave(data)
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



if __name__ == '__main__':
    PROJECT_DIR_PATH = '/home/gpxlcj/zq_project/zq_bus'
    sys.path.append(PROJECT_DIR_PATH)
    os.environ['DJANGO_SETTINGS_MODULE'] = 'zq_bus.settings'
    from zq_bus import settings
    from bus.models import *
    main()

