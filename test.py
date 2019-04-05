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