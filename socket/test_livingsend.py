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
    temp = (104,104,28,2,2,1,1,1,1,1,1,1,1,3,3,16,4,4,4,4,4,4,5,5,5,5,6,6,6,6,22,7,7,0,8,8,9,9,9,9,10,10)
    if not temp:
        print'the tcp client is over'
        break
    data = pack_data_b(temp)
    tcpCliSock.send(data) 
    data = tcpCliSock.recv(BUFSIZ)
    print data[0],'--',data[1],data[2],'--',data[3],'--',data[4],len(data)
    print struct.unpack('BBBBB',data)
    a = raw_input('>')
    if a == '0':
        break
