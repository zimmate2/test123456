import socket
import os

#Week 5 define connecting
def connecting():
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("10.3.0.128", 8080))
    s.listen(1)
    print("=" * 60)
    print(" TCP TUNING THE CONNECTION ATTEMPTS")
    print("=" * 60)
    print('[+] Listenign for income TCP connection on port 8080')
    conn, addr = s.accept()
    print('[+]We got a connection from', addr)

    while True:
        print("=" * 60)
        command = input("Shell> ")
        if 'terminate' in command:
            conn.send('terminate'.encode())
            break
        else:
            conn.send(command.encode())
            print(conn.recv(5000).decode())


def connect():
    my_socket = socket.socket()
    my_socket.bind(("10.3.0.0",8080))
    my_socket.listen(1)
    connection,addres = my_socket.accept()
    print("Connection established successfully",addres)

    while True:
        command = input("Shell> : ")
        if "terminate" in command:
            connection.send("terminate".encode())
            connection.close()
            break
        else:
            connection.send(command.encode())
            response = connection.recv(5000). decode()
            print(response)

def main():
    connecting()

main()