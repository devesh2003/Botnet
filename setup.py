from cx_Freeze import setup,Executable
import os

os.environ['TCL_LIBRARY'] = r'C:\\Python27\\tcl\\tk8.5'
os.environ['TK_LIBRARY'] = r'C:\\Python27\\tcl\\tk8.5'

setup(name="bot",version="1.0",executables = [Executable("bot.py")])
