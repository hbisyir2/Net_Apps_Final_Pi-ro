import socket
import pickle
import select

sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock1.bind(('', 8000))
sock2.bind(('', 8001))

sock1.listen(3)
sock2.listen(3)

socket_list = (sock1, sock2)

while True:
    ready, _, _ = select.select(socket_list, [], [])

    for sock in ready:
        conn, addr = sock.accept()
        data = conn.recv(256)
        print("Message: ", data)

    # print(pickle.loads(data))

    # conn.sendall(reply)

conn.close()
sock.close()
