import socket
import datetime
import struct

HOST = '0.0.0.0'
PORT = 22333
ADD = (HOST, PORT)
BUFFERSIZE = 1024

TcpSerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
TcpSerSocket.bind(ADD)
TcpSerSocket.listen(10)

TcpCliSocket, addr = TcpSerSocket.accept()
print "receive from ", str(addr)
while True:
    data = TcpCliSocket.recv(BUFFERSIZE)
    if data:
        print data
    else:
        print data[1]
    response_str = 'BBBBB'
    response_data = struct.pack(response_str, 84, 104, 26, 0 ,10)
    TcpCliSocket.send(response_data)
