import os
from datetime import datetime
import socket 
from threading import Thread
import threading
import time
import argparse
import multiprocessing as mp
import thread
import subprocess
import codecs
import traceback


       
print_lock = threading.Lock() 

class SocketServer():
    '''
    This class creates a socket server and listens to messages on a specific ip and port.
    '''
    clients = []
    
    def __init__(self, ip='127.0.0.1', port='8080', timer=60):
        '''
        Parameters
        
        ip: int
            Ip to receive messages with web socket.
        port: int
            Port to receive messages with web socket.
        timer: int
            Timer to wait to last messages or close connection with client.
        '''
        self.ip = ip
        self.port = port
        self.timer = timer
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.ip, self.port)) 
        self.socket.listen(5) 

        
        def run(self):
            print ("Server started")
        try:
            self.accept_clients()
        except Exception as ex:
            print (ex)
        finally:
            print ("Server closed")
            for client in self.clients:
                client.close()
            self.socket.close()
            
    def accept_clients(self):
        '''
        Accet client to connect this and create thread to process client.
        '''
        while 1:
            print("Multithreaded Python server : Waiting for connections in IP:", self.ip, " PORT:",self.port)
            print_lock.acquire() 
            (clientsocket, address) = self.socket.accept()
            clientsocket.settimeout(self.timer)
            #Adding client to clients list
            self.clients.append(clientsocket)
            #Client Connected
            self.onopen(clientsocket, address)
            #Receiving data from client
            thread.start_new_thread(self.receive, (clientsocket,address))
            
    def receive(self, client, address):
        '''
        Receive messages from client trough onmessage and onclose
        '''
        data_brute=''
        max_buffer_size = 1024
        try:
            while 1:
                data_brute, port  = client.recvfrom(max_buffer_size)
                if not data_brute:
                    break   
                else:
                    #Message Received
                    self.onmessage(client, data_brute, address)
            self.onclose(client,address, data_brute)
        except Exception:
            traceback.print_exc()       
            #Client Disconnected
            self.onclose(client,address, data_brute)
        
        
    def onopen(self, client, address):
        '''
        Trigger when new client connected.
        '''
        print ("[+] New server socket thread started for " + str(address))

    def onmessage(self, client, message, address):
        '''
        Trigger when response to client with a message.
        '''
        self.save_data(address[0], message)
        MESSAGE = b'\nMessage received by server\n'
        client.send(MESSAGE)  # echo

    def onclose(self, client, address, data):
        '''
        Trigger to print close connection with client.
        '''
        print("Close connection",address, data)
        print_lock.release() 
        #Removing client from clients list
        self.clients.remove(client)
        #Closing connection with client
        client.close()
        #Closing thread
        thread.exit()    
    
    def save_data(self, addr, data):
        '''
        Save in txt and call php function when receive data from client.
        
        Parameters
        ----------
        addr: tuple int (ip,port)
            Address from connected client
            
        data: bytes
            Data send from client to server.
        '''
        #Save data  log adding lines to document.
        log_path = os.path.join('log','log.txt')
        
        if not os.path.isdir('log'):
            os.makedirs('log')
        
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            
        with open(log_path, 'a') as file:
            file.write(dt_string +','+data+'\n')        
                       
def main(ip='127.0.0.1',port=18000): 
    '''
    Funtion principal to create object SocketServer from websocket.
    '''              
    # Multithreaded Python server : TCP Server Socket Program Stub
    SocketServer(ip, port)    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('parameters',
                        type=str, nargs=2,
                        help='ip, port')
    args = parser.parse_args()

    ip = args.parameters[0]
    port = int(args.parameters[1])
    
    server_process = mp.Process(name="{server_socket}",
                                 args=(ip, port),
                                 target=main)
    server_process.start()




