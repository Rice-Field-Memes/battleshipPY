import time, socket, sys
 
socket_server = socket.socket()
server_host = socket.gethostname()
ip = socket.gethostbyname(server_host)
sport = 8080
HEADER_LENGTH = 10
 
print('This is your IP address:',ip)
server_host = input('Enter server IP address: ')
if server_host == "": server_host = "127.0.0.1"

name = input('Enter Client name: ').encode('utf-8')

socket_server.connect((server_host, sport))
 
socket_server.send(f"{len(name):<{HEADER_LENGTH}}".encode('utf-8') + name)
#server_name = socket_server.recv(1024)
#server_name = server_name.decode()

#print('Connected to server {0} at {1}'.format(server_name,server_host))
while True:
    #message = (socket_server.recv(1024)).decode()
    #print(server_name, ":", message)
    message = input("> ").encode('utf-8')
    socket_server.send(f"{len(message):<{HEADER_LENGTH}}".encode('utf-8') + message)