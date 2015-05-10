# -*-coding:utf-8 -*-
__author__ = 'blues'
from SocketServer import ThreadingTCPServer

from streamhandler import BusStreamRequestHandler
from gps_settings import *

if __name__ == '__main__':

    ADDR = (HOST, PORT)
    ThreadingTCPServer.allow_reuse_address = True
    server = ThreadingTCPServer(ADDR, BusStreamRequestHandler)
    print 'Starting the server at host:' + str(HOST) + ' and port:' + str(PORT)
    server.serve_forever()
