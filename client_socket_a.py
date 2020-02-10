import socket 


# +

host = '127.0.0.1'
port = 1111
BUFFER_SIZE = 2000 
MESSAGE = b'$\xff\xff\xff\xff\x00\x00\x12730030707797681\xc9\xaa\xbb\x93\x08'
 
tcpClientB = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
tcpClientB.connect((host, port))

tcpClientB.send(MESSAGE)     
data = tcpClientB.recv(BUFFER_SIZE)
print ("Response:", data)

#tcpClientB.close() 
# -




