#! /usr/bin/python
# coding=UTF8

import socket
import thread
import threading
import bat

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind(('', 5555))
server.listen(5)

def main(server,to):
  tu = bat.Bat(server, to)
  tu.go()
  
try:
  print "waiting for client"
  clientsocket, address = server.accept()
  print "connection accepted from "+str(address)
  thread.start_new_thread( main, (clientsocket, 100) )
  msg = ''
  while True:
      msg += clientsocket.recv(4096)
      if msg!='':
        print msg
      msg=''
except KeyboardInterrupt:
  print "sai daqui"
  server.close()
  

server.close()
