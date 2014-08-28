#! -*- coding:utf-8 -*-
import socket
import struct

HOST = '127.0.0.1'
PORT = 8080
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
    temp = (104,104)
    if not temp:
        print'the tcp client is over'
        break
    print temp
    data = pack_data_b(temp)
    tcpCliSock.send(data) 
    a = raw_input('>')
