import time    # used for timeout on script
import socket    # need modle to open sockets
import threading  # we want to multi thread
from os import close
from queue import Queue # queue management

#set defualt timout in seconds (float)
socket.setdefaulttimeout(.55)

# LOCK threat during print to get cleaner outputs
thread_lock = threading.Lock()

# get target IP or host name as input from user

target_IP = input("Please enter target IP :  ")
port_start = int(input("Please enter the target port to start (Eg- 01) "))
port_stop = int(input("Please enter the target port to stop (Eg- 65535) "))

try:
    t_ip = socket.gethostbyname(target_IP)
    print("Scanning Host for Open Ports", t_ip)
except socket.gaierror:
    print("invalid host name. please enter a valid IP or domain")
    exit(1)

def portscan(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #create socket object
    s.settimeout(0.55) # set timeout for each connection attempt

    try:
        s.connect((t_ip, port))

        #dont let the thread screw up printing
        with thread_lock:
            print(f"Port{port} is open")

        s.close() # CLOSE THE SOCKET CONNECTION

    except:
        pass

    #thread function that pulls worker from the queue and processes
def threader():
    while True:
        worker = q.get()
        portscan(worker)
        q.task_done()

#create queue and threader
q = Queue()

# start time
startTime = float(time.time())

# start 200 threads
for _ in range(200):
    t = threading.Thread(target=threader)
    t.daemon = True  # Classifies as deamon so they die when main dies
    t.start()

# add port range to Q
for worker in range(port_start, port_stop, + 1):
    q.put(worker)

#  wait for port to terminate
q.join()

ctime = float(time.time())
runtime = ctime - startTime
print(f"Run Time{runtime :.2f}")


# # Print final time reports
# runtime = float("%0.2f" % time.time() - startTime)
# print("RUN TIME : ", runtime, "seconds")