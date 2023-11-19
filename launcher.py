import ctypes
import os
import sys

def run_as_admin():
    if ctypes.windll.shell32.IsUserAnAdmin():
        return True
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        return False

if __name__ == "__main__":
    if run_as_admin():
        from sscert import *
