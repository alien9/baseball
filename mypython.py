import socket

mySocket = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )

mySocket.bind ( ( '', 5555 ) )

mySocket.listen ( 5 )

while True:
  channel, details = mySocket.accept()
  print 'We have opened a connection with', details
  txt = channel.recv ( 100 )
  print txt
  channel.send ( "This is a response test - attempt 1\0" )
  #channel.close()
