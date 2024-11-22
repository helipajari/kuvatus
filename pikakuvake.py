import os
import winshell

from win32com.client import Dispatch

if __name__ == '__main__':
    sc_name = 'Kuvatus.lnk'
    desktop_path = winshell.desktop()

    cwd = os.getcwd()
    target = os.path.join(cwd, 'kuvatus.exe')
    kuvatus_sc_path = os.path.join(cwd, sc_name)

    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(kuvatus_sc_path)
    shortcut.WorkingDirectory = cwd
    shortcut.TargetPath = target

    desktop_sc_path = os.path.join(desktop_path, sc_name)

    if not os.path.exists(desktop_sc_path):
        shortcut.save()
        os.rename(kuvatus_sc_path, desktop_sc_path)
