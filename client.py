import socket, time
from threading import Thread

HOST = input('Input host address: ')
PORT = 8000
BUFSIZE = 1024
ADDR = (HOST, PORT)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(ADDR)

def receive():
	while True:
		try:
			msg = client_socket.recv(BUFSIZE)
			print(msg.decode("utf-8"))
		except OSError:
			break

receive_thread = Thread(target=receive, daemon=True)
receive_thread.start()
while True:
	try:
		msg = input()
		if msg != "":
			client_socket.send(msg.encode("utf-8"))
		if msg == "!!quit":
			break
	except:
		client_socket.send(("!!quit").encode("utf-8"))
		break

client_socket.close()
