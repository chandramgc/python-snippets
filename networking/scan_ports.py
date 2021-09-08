from socket import AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR, socket
import re
import subprocess
from datetime import datetime
import sys

def socket_scan():
    # Clear the screen
    subprocess.call('clear', shell=True)

    # Ask for input
    #remoteServer    = input("Enter a remote host to scan:")
    remoteServerIP  = "127.0.0.1"

    # Print a nice banner with information on which host we are about to scan
    print("-" * 60)
    print("Please wait, scanning remote host", remoteServerIP)
    print("-" * 60)

    # Check what time the scan started
    t1 = datetime.now()

    # Using the range function to specify ports (here it will scans all ports between 1 and 1024)

    # We also put in some error handling for catching errors
    ports_list = []
    try:
        for port in range(135,65536):  
            sock = socket(AF_INET, SOCK_STREAM)
            result = sock.connect_ex((remoteServerIP, port))
            if result == 0:
                print("Port {}: 	 Open".format(port))
                ports_list.append(port)
            sock.close()
        print("Total count of port found: " + str(len(ports_list)))
    except KeyboardInterrupt:
        print("You pressed Ctrl+C")
        sys.exit()

    except Exception as err:
        print("Couldn't connect to server")
        print(err)
        sys.exit()

    # Checking the time again
    t2 = datetime.now()

    # Calculates the difference of time, to see how long it took to run the script
    total =  t2 - t1

    # Printing the information to screen
    print('Scanning Completed in: ', total)

def check_socket():
    socket_list = []

    host_ip ="127.0.0.1"
    for port_number in range(1025,65536):
        try:
            socket_list.append(create_socket(host_ip,port_number))
        except Exception: 
            pass 
    print(socket_list)

def create_socket(ip,port):
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server_socket.bind((ip,port))
    server_socket.listen(1)
    return server_socket

def check_open():
    port = 0
    host_ip ="127.0.0.1"
    while port < 65536:
        is_connection = is_open(host_ip,port)
        if is_connection:
            print(f'{host_ip}:{port} open\n')
        port += 1

def is_open(ip,port) -> bool:
   s = socket(AF_INET, SOCK_STREAM)
   try:
      s.connect((ip, int(port)))
      s.shutdown(2)
      return True
   except:
      return False

def get_active_ports():
    process = subprocess.run(['netstat', '-n'], capture_output=True)
    report = process.stdout.decode().splitlines()
    ports = set()
    for i in report[4:]:
        ports.add(re.split(':(?!.*:)', re.split('\s+', i)[2])[1])
    return ports

def open_socket():
    port = 0
    host_ip ="127.0.0.1"
    connected = False
    while port < 65536:
        try:
            try:
                socket_obj = socket(AF_INET, SOCK_STREAM, 0)
            except:
                print("Could not open socket !")
                break
            socket.connect(host_ip,port)
            connected = True
        except ConnectionRefusedError:
            connected = False
        finally:
            if(connected and port != socket.getsockname()[1]):
                print(f'{host_ip}:{port} open\n')
                port += 1
                socket.close()

if __name__ == '__main__':
    socket_scan()