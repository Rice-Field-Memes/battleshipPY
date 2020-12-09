import os
import sys

import time
import socket
import threading
import select

from pynput import keyboard
import colorama
from colorama import Style, Cursor
colorama.init()

pos = lambda y, x: Cursor.POS(x, y)

class Msgs:
    def __init__(self):
        self.height = 10
        self.messageQueue = []
        self.inpt = ""
    def write(self):
        os.system("cls")
        for i,x in enumerate(self.messageQueue):
            sys.stdout.write(pos(max(0,self.height-len(self.messageQueue))+i,0))
        sys.stdout.write(pos(10,0) + ">" + self.inpt)
        sys.stdout.flush()
msgs = Msgs()

def on_press(key):
    try:
        msgs.inpt+=key.char
        msgs.write()
    except AttributeError:
        if key == keyboard.Key.backspace:
            msgs.inpt = msgs.inpt[:-1]
            msgs.write()
        elif key == keyboard.Key.enter and msgs.inpt == "":
            sendMsg()

def sendMsg():
    """
    conn.send(message.encode())
    msgs.messageQueue.append(msgs.inpt)
    msgs.inpt=""
    msgs.write()
    """
    pass
def recvMsg(client_socket):
    try:
        
        # Receive our "header" containing message length, it's size is defined and constant
        message_header = client_socket.recv(HEADER_LENGTH)

        # If we received no data, client gracefully closed a connection, for example using socket.close() or socket.shutdown(socket.SHUT_RDWR)
        if not len(message_header):
            return False

        # Convert header to int value
        message_length = int(message_header.decode('utf-8').strip())

        # Return an object of message header and message data
        return {'header': message_header, 'data': client_socket.recv(message_length)}

    except:

        # If we are here, client closed connection violently, for example by pressing ctrl+c on his script
        # or just lost his connection
        # socket.close() also invokes socket.shutdown(socket.SHUT_RDWR) what sends information about closing the socket (shutdown read/write)
        # and that's also a cause when we receive an empty message
        return False
def recvThread():
    while True:
        global sockets_list
        read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
        msgs.write()
        for notified_socket in read_sockets:
            # If notified socket is a server socket - new connection, accept it
            if notified_socket == server_socket:
                print("is")
                # Accept new connection
                # That gives us new socket - client socket, connected to this given client only, it's unique for that client
                # The other returned object is ip/port set
                client_socket, client_address = server_socket.accept()

                # Client should send his name right away, receive it
                user = recvMsg(client_socket)

                # If False - client disconnected before he sent his name
                if user is False:
                    continue

                # Add accepted socket to select.select() list
                sockets_list.append(client_socket)

                # Also save username and username header
                clients[client_socket] = user

                print('Accepted new connection from {}:{}, username: {}'.format(*client_address, user['data'].decode('utf-8')))

            # Else existing socket is sending a message
            else:
                print("isnt")

                # Receive message
                message = recvMsg(notified_socket)

                # If False, client disconnected, cleanup
                if message is False:
                    print('Closed connection from: {}'.format(clients[notified_socket]['data'].decode('utf-8')))

                    # Remove from list for socket.socket()
                    sockets_list.remove(notified_socket)

                    # Remove from our list of users
                    del clients[notified_socket]

                    continue

                # Get user by notified socket, so we will know who sent the message
                user = clients[notified_socket]
                msgs.messageQueue.append(message)
                print(f'Received message from {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')

                # Iterate over connected clients and broadcast message
                for client_socket in clients:

                    # But don't sent it to sender
                    if client_socket != notified_socket:

                        # Send user and message (both with their headers)
                        # We are reusing here message header sent by sender, and saved username header send by user when he connected
                        client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])

        # It's not really necessary to have this, but will handle some socket exceptions just in case
        for notified_socket in exception_sockets:

            # Remove from list for socket.socket()
            sockets_list.remove(notified_socket)

            # Remove from our list of users
            del clients[notified_socket]
        
#        message = conn.recv(1024)
#        message = message.decode()
#        print("\n" + client + ':' + message)

if __name__ == "__main__":
    os.system("cls")
    s_ip = "127.0.0.1"

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    host_name = socket.gethostname()
    HEADER_LENGTH = 10
    port = 8080
 
    server_socket.bind((s_ip, port))
    print("Binding successful!")

    name = "server"

    server_socket.listen()

    sockets_list = [server_socket]
    clients = {}
 
    #conn, add = server_socket.accept()

    #print("Received connection from ", add[0])
    #print('Connection Established. Connected From: ',add[0])
 
    #client = (conn.recv(1024)).decode()
    #print(client + ' has connected.')
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    msgs.write()
    rt = threading.Thread(target=recvThread)
    #st.start()
    rt.start()
    print("hi")

    #server_socket.listen(1)
 
    #conn2, add2 = server_socket.accept()
 
    #print("Received connection from ", add2[0])
    #print('Connection Established. Connected From: ',add2[0])
 
    