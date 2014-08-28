# -*-coding:utf-8 -*-
import socket
import struct
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


def packdata(data):
     
    start = DataStruct('bb')
    length = DataStruct('b')
    LAC = DataStruct('H')
    terminal_id = DataStruct('BBBBBBBB')
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
    get_data_type = struct.Struct('bb').unpack(data)
    if get_data_type[0]==104 and get_data_type[1]==104:
        print 'ok'
        return (0,0)
    else:
        return (0,0)
    form_string = start.data_type+length.data_type+LAC.data_type+terminal_id.data_type+info_code.data_type+agreement_code.data_type+\
           datetime.data_type+latitude.data_type+longitude.data_type+speed.data_type+\
           direction.data_type+MNC.data_type+cell_id.data_type+\
           status.data_type+end.data_type
    packed_data = struct.unpack(form_string, data)
    return packed_data

def main():

#    HOST = '127.0.0.1'
#    PORT = 8080
#    BUFSIZ = 1024
#    ADDR = (HOST, PORT)
#
#    tcpSerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#    tcpSerSock.bind(ADDR)
#    tcpSerSock.listen(5)

    while True:
        HOST = '127.0.0.1'
        PORT = 8080
        BUFSIZ = 64
        ADDR = (HOST, PORT)

        tcpSerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcpSerSock.bind(ADDR)
        tcpSerSock.listen(5)
        print 'waiting for connection...'
        tcpCliSock, addr = tcpSerSock.accept()
        print '...connected from:', addr
        while True:
            data = tcpCliSock.recv(BUFSIZ)
            if not data:
                break
            else:
                packed_data = packdata(data)
                if packed_data[0]==104 and packed_data[1]==104:
                    print 'ok'

            tcpCliSock.send('ok')
        tcpCliSock.close()
        tcpSerSock.close()




if __name__ == '__main__':

    main()

