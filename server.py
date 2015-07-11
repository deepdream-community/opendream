# consider this a stub. need to implement a listener.

import socket
import sys
from time import time

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12345                 # Reserve a port for your service.

s.connect((host, port))
s.send("Hello server!")
f = open('tosend.png','rb')
print 'Sending...'
l = f.read(1024)
while (l):
    print 'Sending...'
    s.send(l)
    l = f.read(1024)
f.close()
print "Done Sending"
print s.recv(1024)
s.close   

import socket
from sendfile import sendfile
def send(filename):
  f = open(filename, "rb")
  blocksize = os.path.getsize(filename)
  sock = socket.socket()
  sock.connect(("127.0.0.1", 8021))
  offset = 0

  while True:
      sent = sendfile(sock.fileno(), f.fileno(), offset, blocksize)
      if sent == 0:
          break  # EOF
      offset += sent

inbound = socket.socket()
inbound.bind(("localhost",9999))
inbound.listen(10) # Acepta hasta 10 conexiones entrantes.

while True:
  sc, address = inbound.accept()

  print address
  i=1
  f = open('/external/'+str(time())+'.jpg','wb') #open in binary
  i=i+1
  while (True):       
  # recibimos y escribimos en el fichero
      l = sc.recv(1024)
      while (l):
        f.write(l)
        l = sc.recv(1024)
  f.close()
  sc.close()

inbound.close()
