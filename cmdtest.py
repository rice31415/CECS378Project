import winreg
import ctypes, sys

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False



path = winreg.HKEY_CURRENT_USER

def create_disablecmd_key():
    # try:
        key = winreg.OpenKeyEx(path, r"Software\\Policies\\Microsoft\\Windows")
        newKey = winreg.CreateKey(key,"System")
        winreg.SetValueEx(newKey, "DisableCMD", 0, winreg.REG_DWORD, 0)
        if newKey:
            winreg.CloseKey(newKey)
    # except Exception as e:
    #         print(e)

if is_admin():
    create_disablecmd_key()
else:
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    print("idk")
    create_disablecmd_key()
