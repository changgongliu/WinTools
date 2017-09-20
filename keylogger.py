from ctypes import *
import pythoncom
import pyHook
import win32clipboard

user32 = windll.user32
kernel32 = windll.kernel32
psapi = windll.psapi
current_windon = None
def get_current_process():
    #获取前台窗口的句柄
    hwnd = user32.GetForeGroundwindow()

    # 获取进程ID
    pid = c_ulong(0)
    user32.GetWindowThreadProcessId()
    
