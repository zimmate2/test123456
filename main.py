import socket
import uuid
from colorama import Fore, Style
import os
import time
import psutil

def GetInternetconnectivity():
    try:
        socket.create_connection(("8.8.8.8", 53))
        print("Internet is connected")
    except OSError:
        print("NO INTERNET CONNECTION")


def GetMACAddress():
    print(f"MAC Address: {':'.join(f'{(uuid.getnode() >> i) & 0xff:02x}' for i in range(0,48,8))}")

def GetHostandFQDN():
    print(f"Hostname: {socket.gethostname()}")
    print(f"Fully Quallified Domain Name: {socket.getfqdn()}")

def GetActiveNetworkInterface():
    print(f"Active Network Interface: {list(psutil.net_if_addrs().keys())}")

def SystemUptime():
    print(f"System Uptime: {time.time() - psutil.boot_time(): .2f8} seconds")

def GetNumberOfCores():
    print(f"CPU Cores: {os.cpu_count()}")

def GetRAMsize():
    print(f"Total RAM: { psutil.virtual_memory().total / (1024 **3): 2f} GB")

def GetDiskSpace():
    disk = psutil.disk_usage('/')
    print(f"TOTAL DISK SPACE: {disk.total / (1024 **3): 2f}: GB")
    print(f"FREE SPACE: {disk.free /(1024 **3): 2f}: GB")

def GetCurrentUser():
    print("Current User",os.getlogin())

def GetSystemTimezone():
    print("Timezone", time.timezone)

def check_if_port_is_used():
    try:
        port = int(input("Enter the Port Number:  "))
        ip = input("Enter the IP address:  ")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((ip, port))
        sock.close()
        if result == 0:
            print("Port is in use")
        else:
            print("Port is available")
    except ValueError:
        print("Invalid port number, input valid port.")
    except Exception as e:
        print(f"error occurred: {e}")

def main():
    while True:
        print(Fore.CYAN + """
     ███████╗██╗███╗   ███╗███╗   ███╗     ██████╗ ██████╗ ██████╗ ███████╗
     ╚══███╔╝██║████╗ ████║████╗ ████║    ██╔════╝██╔═══██╗██╔══██╗██╔════╝
       ███╔╝ ██║██╔████╔██║██╔████╔██║    ██║     ██║   ██║██║  ██║█████╗  
      ███╔╝  ██║██║╚██╔╝██║██║╚██╔╝██║    ██║     ██║   ██║██║  ██║██╔══╝  
     ███████╗██║██║ ╚═╝ ██║██║ ╚═╝ ██║    ╚██████╗╚██████╔╝██████╔╝███████╗
     ╚══════╝╚═╝╚═╝     ╚═╝╚═╝     ╚═╝     ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝                                                                        
   """ + Style.RESET_ALL)
        print(Style.BRIGHT + Fore.MAGENTA + "Welcome To Cyber App" + Style.RESET_ALL)
        print(Fore.BLUE + "1: Check If Port Is Used" + Style.RESET_ALL)
        print("2: Get Current User")
        print("3: Get System Timezone")
        print("4: Get Disk Space")
        print("5: Get RAM Size")
        print("6: Exit")
        print("7: CPU cores")
        print("8: Get System Uptime")
        print("9: Get Active Network Interface")
        print("10: Get Host Name and FQDN")
        print("11: Get MAC Address")
        print("12: check internet connection")

        try:
            choice = int(input("Enter Your Choice: "))
            if choice ==1:
                check_if_port_is_used()

            elif choice == 2:
                GetCurrentUser()

            elif choice == 3:
                GetSystemTimezone()

            elif choice == 4:
                GetDiskSpace()

            elif choice == 5:
                GetRAMsize()

            elif choice == 6:
                print("Exiting the application. Goodbye")
                break

            elif choice == 7:
                GetNumberOfCores()

            elif choice == 8:
                SystemUptime()

            elif choice == 9:
                GetActiveNetworkInterface()
                time.sleep(3)

            elif choice == 10:
                GetHostandFQDN()
                time.sleep(3)

            elif choice == 11:
                GetMACAddress()
                time.sleep(5)

            elif choice == 12:
                GetInternetconnectivity()
                time.sleep(3)


            else:
                print("Invalid choice. Please try again")

        except ValueError:
            print("Invalid input, please pick a number")

        except Exception as e:
            print(f"An unexpected error has occured: {e}")
main()
