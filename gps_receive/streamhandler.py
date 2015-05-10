#! -*- coding:utf-8 -*-
__author__ = 'blues'
import os
import sys
import struct
import urllib
import time
from gps_settings import *

sys.path.append(PROJECT_DIR_PATH)
os.environ['DJANGO_SETTINGS_MODULE'] = 'zq_bus.settings'

from bus.models import *
from SocketServer import StreamRequestHandler
from TerminalDataPacket import *


class BusStreamRequestHandler(StreamRequestHandler):

    packed_data = TerminalDataPacket()
    unpacked_data = ()
    numberof_data_packet = 1
    data_type = -1

    '''
    测试后台输入控制函数
    '''
    @staticmethod
    def debug_log(debug_info):
        now = unicode(time.strftime('%Y/%m/%d-%H:%M:%S', time.localtime(time.time())))
        if GPS_DEBUG:
            if debug_info is not None:
                print u"DEBUG:" + now + u":" + debug_info
            else:
                print u"DEBUG:" + now + u":sorry,no debug info..."
        else:
            return

    '''
    更新车辆坐标
    '''
    @staticmethod
    def update_bus_coordinate(data, bus):
        coordinate = Coordinate(longitude=data['longitude'],
                                latitude=data['latitude'], bus_number=data['bus_number'])
        coordinate.save()
        bus.coordinate = coordinate
        bus.save()

    '''
    注册新车辆
    '''
    @staticmethod
    def register_new_bus(data):
        try:
            coordinate = Coordinate.objects.all()[0]
        except Exception as ex:
            print(u"Exception in register_new_bus:" + str(ex))
            coordinate = Coordinate(longitude=114.233333, latitude=30.5312333)
            coordinate.save()
        route = Route.objects.all()[0]
        stop = Stop.objects.filter(route=route)[0]
        bus = Bus(route=route, stop=stop, coordinate=coordinate, number=data['bus_number'])
        bus.save()
        return bus

    '''
    更新车站
    '''
    @staticmethod
    def update_bus_stop(data, bus):
        stops = Stop.objects.filter(route=bus.route)
        distance = MAX_LENGTH
        for stop in stops:
            temp_distance = ((bus.coordinate.latitude - stop.latitude)**2 +
                             (bus.coordinate.longitude - stop.longitude)**2)
            if distance < temp_distance:
                bus.stop = stop
        bus.save()

    '''
    更新车辆路线
    '''
    @staticmethod
    def update_bus_route(data, bus):

        routes = Route.objects.all()
        for r in routes:
            if (abs(r.special_coordinate.latitude - data['latitude']) < ERROR_VALUE) \
                    and (abs(r.special_coordinate.longitude - data['longitude'] < ERROR_VALUE)):

                bus.route = r
        bus.save()

    '''
    数据流处理主调用函数
    '''
    def handle(self):
        while True:
            try:
                raw_data = self.request.recv(1024).strip()
            except Exception as ex:
                raw_data = ''
                print(u"Exception in receiving:" + str(ex))
                break

            if len(raw_data) == 0:
                self.debug_log(u"the data is empty!")
            else:
                self.debug_log(u"the length of data is " + str(len(raw_data)))
                self.judge_and_pack(raw_data)

    '''
    判断包类型与数据包封装
    '''
    def judge_and_pack(self, raw_data):
        global unpacked_data
        global packed_data
        global numberof_data_packet

        #类型判断句柄字典
        data_type_handler = {
            'gps': 0x10,
            'heartbreak': 0x1a,
            'ip': 0x1b,
            'command': 0x1c,
        }

        #分割成以字节为单位的元组
        raw_data_len = len(raw_data)
        form_string = 'B' * raw_data_len
        try:
            unpacked_data = struct.unpack(form_string, raw_data)
        except Exception as ex:
            print(u"Exception during Unpacking data:" + str(ex))

        #通过数据包长度判断gps数据包个数
        if raw_data_len > 40:
            numberof_data_packet = (raw_data_len + 2)/42
        else:
            numberof_data_packet = 1
        print(u"we got " + str(numberof_data_packet) + u"packets")

        #测试数据包展示
        packet = str()
        for i in range(0, len(raw_data)):
            temp_str = str(hex(unpacked_data[i])).replace('0x', ' ')
            packet += temp_str
        self.debug_log(u"packet is: " + packet)

        #获取数据包类型判断句柄
        protocol_id = unpacked_data[15]
        judge_handler = protocol_id
        self.debug_log(u"the packet's handler is: " + str(judge_handler))

        #获取IMEI号（车辆标识）
        IMEI = str()
        for i in range(5, 13):
            temp_str = str(unpacked_data[i]/16)+str(unpacked_data[i] % 16)
            IMEI += str(temp_str)

        #数据包为GPS数据（可能一次发送多个包）
        if judge_handler == data_type_handler['gps']:
            self.debug_log(u"the packet is GPS Data")

            #获取end_id（最后一个GPS包无end_id）
            '''
            end_id = str()
            try:
                for i in range(40, 42):
                    temp_str = str(hex(unpacked_data[i]))
                    end_id += temp_str

            except IndexError as ex:
                self.debug_log(u"strange gps packet and we will test it! we know: " + str(ex))
            '''

            end_id = '0xd0xa'

            if end_id == '0xd0xa':
                #获取LAC号
                LAC = str()
                for i in range(3, 5):
                    temp_str = str(unpacked_data[i]/16)+str(unpacked_data[i] % 16)
                    LAC += str(temp_str)

                #获取cell_id
                cell_id = str()
                for i in range(34, 36):
                    temp_str = str(unpacked_data[i]/16)+str(unpacked_data[i] % 16)
                    cell_id += str(temp_str)

                for i in range(0, numberof_data_packet):

                    #坐标转换
                    latitude = (unpacked_data[22 + i*42] * (256 ** 3) + unpacked_data[23 + i*42] * (256 ** 2) +
                                unpacked_data[24 + i*42] * 256 + unpacked_data[25 + i*42])
                    latitude = (latitude + 0.0) / (30000*60)
                    longitude = (unpacked_data[26 + i*42] * (256 ** 3) + unpacked_data[27 + i*42] * (256 ** 2) +
                                 unpacked_data[28 + i*42] * 256 + unpacked_data[29 + i*42])
                    longitude = (longitude + 0.0) / (30000*60)

                    #百度地图API
                    transform_url = "http://api.map.baidu.com/geoconv/v1/?coords=" + str(longitude) + \
                                    "," + str(latitude) + "&from=1&to=5&ak=7yTvUeESUHB7GTw9Pb9BRv1U"

                    transform_data = urllib.urlopen(transform_url).read()
                    try:
                        transform_data = eval(transform_data)['result'][0]
                        latitude = transform_data['y']
                        longitude = transform_data['x']

                    except Exception as ex:
                        print(u"Exception after calling API to unpack: " + str(ex))

                    latitude = float(latitude)
                    longitude = float(longitude)

                    #终端状态判断
                    status_dic = {
                        0: 'W&S, not ready',
                        1: 'W&S, ready',
                        2: 'W&N, not ready',
                        3: 'W&N, ready',
                        4: 'E&S, not ready',
                        5: 'E&S, ready',
                        6: 'E&N, not ready',
                        7: 'E&N, ready',
                    }

                    phone_status = unpacked_data[39]
                    print(u"the terminal status:" + unicode(status_dic[phone_status]))

                    #数据包装（暂放内存，为扩展方便）
                    packed_data = GPSDataPacket(0, unpacked_data[2], LAC, IMEI,
                                                unpacked_data[13:15], protocol_id, unpacked_data[16:22], latitude,
                                                longitude, unpacked_data[30], unpacked_data[31:33], unpacked_data[33],
                                                cell_id, phone_status)
                    self.debug_log(u"have packed the GPSData which is " + str(packed_data.packet_length) +
                                   u" bytes long")
                    print(u"the bus' IMEI: " + str(packed_data.IMEI))
                    print(u"the latitude: " + str(latitude))
                    print(u"the longitude: " + str(longitude))

                    #调用数据存储
                    data_for_app = {
                        'bus_number': packed_data.IMEI,
                        'latitude': packed_data.latitude,
                        'longitude': packed_data.longitude,
                    }
                    self.save(data_for_app)
                    self.debug_log(u"have packed the GPSData for app!")
                    print "----------------------------------------"
            else:
                self.debug_log(u"the GPSData packet is not complete,and it will be discarded")
                print "----------------------------------------"

        #数据包为心跳包
        elif judge_handler == data_type_handler['heartbreak']:
            self.debug_log(u"the packet is heartbreak Data")
            content_length = unpacked_data[2]
            if content_length >= 15:
                packet_length = content_length + 3
                self.debug_log(u"packet length is " + str(packet_length))

                #获取end_id
                '''
                end_id = str()
                for i in range(packet_length - 2, packet_length):
                    temp_str = str(hex(unpacked_data[i]))
                    end_id += temp_str
                    self.debug_log(u"the end byte is " + temp_str)
                self.debug_log(u"end id is " + end_id)
                '''

                #if end_id == '0x0d0x0a':
                if True:

                    numberof_satellite = unpacked_data[17]
                    signal_to_noise_ratio = unpacked_data[18:18+numberof_satellite]
                    packed_data = HeartBreakPacket(1, content_length, unpacked_data[3],
                                                   unpacked_data[4], IMEI, unpacked_data[13:15],
                                                   protocol_id, unpacked_data[16], numberof_satellite,
                                                   signal_to_noise_ratio)
                    self.debug_log(u"have packed the HeartBreakData, and ready to send back")
                    print(u"the bus: " + packed_data.IMEI + u" is alive!")

                    #心跳包应答
                    values = (0x54, 0x68, 0x1a, 0x0d, 0x0a)
                    s = struct.Struct('BBBBB')
                    return_data = s.pack(*values)
                    self.debug_log(u"the return data is" + str(values))

                    try:
                        self.request.send(return_data)
                        print(u"heartbreak data has been send back successfully!")
                    except Exception as ex:
                        print(u"Exception during sending the back packet:" + str(ex))

                    print "----------------------------------------"
                else:
                    self.debug_log(u"the heartbreak packet is not complete, and it will be "
                                   u"discarded")
                    print "----------------------------------------"
            else:
                self.debug_log(u"the heartbreak packet is too short!")
                print "----------------------------------------"

        #数据包为IP请求包
        elif judge_handler == data_type_handler['ip']:
            self.debug_log(u"the packet is ip Data")
            print "----------------------------------------"
            pass

        #数据包为指令包
        elif judge_handler == data_type_handler['command']:
            self.debug_log(u"the packet is command Data")
            print "----------------------------------------"
            pass
        else:
            self.debug_log(u"Unknown data type!")
            print "----------------------------------------"

    '''
    数据库存储
    '''
    def save(self, data):
        if Bus.objects.filter(number=data['bus_number']):
            bus = Bus.objects.get(number=data['bus_number'])
        else:
            bus = self.register_new_bus(data)
        self.update_bus_coordinate(data, bus)
        self.update_bus_route(data, bus)
        if bus.route:
            self.update_bus_stop(data, bus)
