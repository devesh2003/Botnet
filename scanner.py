import nmap
import socket

nm = nmap.PortScanner()
local_ip = socket.gethostbyname(socket.gethostname)
print(local_ip)
