import socket, time
from threading import Thread

#HOST = input("Input server address: ")
HOST = '0.0.0.0'
PORT = 8000
BUFSIZE = 1024
ADDR = (HOST, PORT)
MAX_USERS = 5

clients = {}

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(ADDR)

def accept_incoming_connections():
    while True:
        client, client_addr = server.accept()
        itsatime = time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime())
        print(itsatime+" :: [ "+client_addr[0]+" ] connected")
        client.send(("GREETINGS!\nType your name and press enter!").encode("utf-8"))
        Thread(target=handle_client, args=(client,)).start()

def set_name(client):
    name_set = False
    while name_set == False:
        name = client.recv(BUFSIZE).decode("utf-8")
        if name in clients.values():
            used_name_msg = 'This name is already used. Please enter another name'
            client.send(used_name_msg.encode("utf-8"))
        else:            
            name_set = True

    welcome = 'Welcome, '+name+'! Type !!quit to exit.'
    client.send(welcome.encode("utf-8"))
    msg = name+' has joined the chat!'
    clients[client] = name
    broadcast(msg, client)

def close_con(client):
    client.close()
    broadcast("[[ USER HAS LEFT THE CHAT ]]", client)
    del clients[client]

def handle_client(client):
    set_name(client)
    while True:
        try:
            msg = client.recv(BUFSIZE)
            decoded_msg = msg.decode("utf-8")
            if decoded_msg != "!!quit":
                print(clients[client] + " :: " + decoded_msg)
                broadcast(decoded_msg, client)
            else:
                close_con(client)
                break
        except OSError:
            close_con(client)
            break

def broadcast(msg, client=None):
    for c in clients:
        if c != client:
            c.send(("["+clients[client]+"] :: "+msg).encode("utf-8"))

if __name__ == "__main__":
    server.listen(MAX_USERS)
    print("[ Server started ]")
    accept_thread = Thread(target=accept_incoming_connections, daemon = True)
    accept_thread.start()
    while True:
        comand = input()
        if comand == 'stop':
            break
#    accept_thread.join()
    server.close()