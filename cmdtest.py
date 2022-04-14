import winreg
import ctypes, sys
import shutil
import os
from elevate import elevate

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        print("a")
        return False



path = winreg.HKEY_CURRENT_USER

def create_disablecmd_key():
    print("c")
    try:
        key = winreg.OpenKeyEx(path, r"Software\\Policies\\Microsoft\\Windows")
        newKey = winreg.CreateKey(key,"System")
        winreg.SetValueEx(newKey, "DisableCMD", 0, winreg.REG_DWORD, 0)
        print("a")
        if newKey:
            winreg.CloseKey(newKey)
    except Exception as e:
            print(e)

#     #doesn't seem to actually escalate to admin
# if is_admin():
#     create_disablecmd_key()
# else:
#     #ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
#     os.rename("C:\\Windows\\System32\\cmd.exe", "C:\\Windows\\System32\\cme.exe")


elevate() #stuff after it won't run it looks like, maybe needs main function
# print("b")
# create_disablecmd_key()

#shutil.move("C:\\cmd.exe", "C:\\Windows\\System32\\cmd.exe")
