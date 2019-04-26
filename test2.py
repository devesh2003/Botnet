
import subprocess,os

os.chdir("..")

subprocess.Popen("C:\\Users\\pathik\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\HP_Services.bat",
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
                close_fds=True)
