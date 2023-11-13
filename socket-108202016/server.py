"""
Title: chat room server
Author: 張家菖
Date: 2022-11-19
ID: 108202016
Key: python, socket, tcp, GUI(tkinter), muliti-thread
"""
import socket
import threading


def ClientThread(clientSocket, clientAddress):
    while True:
        # 接收 client 訊息
        message = clientSocket.recv(1024).decode("utf-8")
        print("*" + clientAddress[0] + "*@" +
              str(clientAddress[1]) + ": " + message)

        # 對其他 clients 廣播
        for client in clients:
            if client is not clientSocket:
                client.send(
                    ("*" + clientAddress[0] + "*@" + str(clientAddress[1]) + ": " + message).encode("utf-8"))

        # 收到 EXIT 即關閉該名 client
        if (message == 'EXIT'):
            clients.remove(clientSocket)
            print("*" + clientAddress[0] + "*@" +
                  str(clientAddress[1]) + " disconnected!!")
            break
    clientSocket.close()


HOST = input("IP: ")
PORT = int(input("PORT(1000~65535): "))
# Check Port range
while(PORT > 65535 or PORT < 1000):
    PORT = int(input("Choose another PORT(1000~65535): "))

# AF_INET: IPv4
# SOCK_STREAM: TCP
hostSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hostSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
hostSocket.bind((HOST, PORT))

# 伺服器開始監聽
# Client-limit -> 5
hostSocket.listen(5)
print('Server IP and Port: %s @%s' % (HOST, PORT))
print('Waiting for Connection...')

# Record all clients
clients = set()
while True:
    # conn 是過來的訊息數據
    # addr 則是對方的IP資料
    # 等待並接受連線
    conn, addr = hostSocket.accept()
    # 增加一名 client
    clients.add(conn)
    print("Connected by: ",
          addr[0] + ":" + str(addr[1]))
    # 一位 client ;一個 thread
    thread = threading.Thread(target=ClientThread, args=(conn, addr))
    thread.start()
