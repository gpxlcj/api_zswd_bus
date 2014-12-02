#! -*- coding:utf-8 -*-
import socket
import struct

HOST = '115.29.17.73'
PORT = 12333
BUFSIZ = 1024
ADDR = (HOST,PORT)

tcpCliSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpCliSock.connect(ADDR)
def pack_data_b(data):
    buf_data = ''
    for i in data:
        buf_data += struct.pack('b', i)
    return buf_data
while True:
    temp = (104,104,37,2,2,1,1,1,1,1,1,1,1,3,3,16,4,4,4,4,4,4,5,5,5,5,6,6,6,6,22,7,7,0,8,8,9,9,9,9,10,10)
    if not temp:
        print'the tcp client is over'
        break
    data = pack_data_b(temp)
    tcpCliSock.send(data) 
    print len(data)
    a = raw_input('>')
    if a == '0':
        break
