import socket 

host = '127.0.0.1'
port = 8080
BUFFER_SIZE = 1024 
MESSAGE = 'Hola'
 
tcpClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
tcpClient.connect((host, port))

tcpClient.send(MESSAGE)     
data = tcpClient.recv(BUFFER_SIZE)
print ("Response:", data)


