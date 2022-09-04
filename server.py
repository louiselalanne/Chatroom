import socket
from threading import Thread

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    #(addr family IPV4, TCP socket)

ip_address='127.0.0.1'
port=8000

server.bind((ip_address,port))
server.listen()

list_clients=[]
nicknames=[]

print('Server is running...')

def broadcast(message, connection):
    for clients in list_clients:
        if clients!=connection:
            try:
             clients.send(message.encode('utf-8'))
            except:
                remove (clients)
                

def remove(connection):
    if connection in list_clients:
        list_clients.remove(connection)


def remove_nickname(nickname):
    if nickname in nicknames:
        nicknames.remove(nickname)


def clientthread(conn, nickname):
    conn.send("Welcome to this chatroom ╰(*°▽°*)╯".encode('utf-8'))
    while True:
        try:
            message = conn.recv(2048).decode('uft-8') #just 2048 bits
            if message:
                print(message)
                broadcast(message,conn)
            else:
                remove(conn)
                remove_nickname(nickname)
        except:
            continue

while True:
    #This accept() method accepts any connection request made to the server and returns 2 parameters -
        #1. The socket object of the client that is trying to connect
        #2. Their IP Address and Port number in the form of a tuple
    conn, addr=server.accept()
    conn.send('NICKNAME'.encode('utf-8'))
    nickname=conn.recv(2048).decode('utf-8')
    list_clients.append(conn)
    nicknames.append(nickname)

    message='> {} joined!'.format(nickname)
    print(message)
    broadcast(message, conn)

    new_thread=Thread(target=clientthread,args=(conn,addr))
    new_thread.start()
