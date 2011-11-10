#! /usr/bin/python

import socket
MSGLEN=100

class mysocket:
    '''demonstration class only
      - coded for clarity, not efficiency
    '''
    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, host, port):
        self.sock.connect((host, port))

    def mysend(self, msg):
        totalsent = 0
        while totalsent < len(msg):
            sent = self.sock.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent

    def myreceive(self):
        msg = ''
        while 1:
            msg += self.sock.recv(4096)
            if msg=='':
                break
            print msg
            msg=''
s=mysocket()
s.connect("192.168.0.109", 5555)
s.mysend('Cheguei.\n')
s.myreceive()
