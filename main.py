import os
import re
import shutil
import sys
import threading
import time
import PySimpleGUI as gui

name = "Kuvake"
version = 1.0


# TODO make UI bigger
def dialog():
    gui.theme('DarkAmber')

    # on laptops try D because usually no extra stuff
    initMem = os.path.join('D:\\', '')
    mem = gui.FolderBrowse('Muuta', initial_folder=initMem, key='mem')
    memT = "etsi kansio"

    initPic = os.path.join(os.environ['USERPROFILE'], 'pictures')
    pic = gui.FolderBrowse('Muuta', initial_folder=initPic, key='pic')
    picT = "etsi kansio"

    ok = gui.Button('Ok', disabled=False)

    layout = [[gui.Text('Lähdekansion polku: '), gui.Text(memT), mem],
              [gui.Text('Kohdekansion polku: '), gui.Text(initPic), pic],
              [gui.Checkbox("Poista siirretyt kuvat alkuperäisestä kansiosta?")],
              [ok, gui.Button('Peruuta')]]

    # WINDOW MADE HERE
    window = gui.Window(name + " " + version.__str__(), layout)

    while True:
        event, values = window.read()

        if event == gui.WIN_CLOSED or event == 'Peruuta':
            break

        if event == 'Ok':
            # TODO disable ok unless mem and pic are not default value?
            if layout[0][1].get() == memT:
                continue
            # mem, pic, delete
            return layout[0][1].get(), layout[1][1].get(), layout[2][0].get()
    window.close()


def doneDialog():
    gui.theme('DarkAmber')

    layout = [[gui.Text('Valmis!')], [], [],
              [gui.Button('Ok')], [], []]

    window = gui.Window(name, layout)

    while True:
        event, values = window.read()
        if event == 'Ok':
            break

    window.close()


# returns a set or array of file creation dates in the format yyyy-mm
# if file or folder has a name fitting with the format or "yyyy mm", add that to set instead
def findDates(src, files, makeset):
    dates = []
    for filename in files:
        # if name is in format yyyy-mm or yyyy mm, add to set if possible
        # format check
        x = re.findall("[1-2][0-9]{3}[-, " "][0-1][0-9]", filename)

        date = ""

        if len(x) == 1:
            # trim to first 6 characters (in case of folder names like "2000-01 birthday")
            date = filename[:len('yyyy-mm'):]
        else:
            f = os.path.join(src, filename)

            ctime = os.path.getctime(f)
            t_obj = time.strptime(time.ctime(ctime))

            # Transforming the time object to a timestamp
            # of ISO 8601 format
            T_stamp = time.strftime("%Y-%m-%d %H:%M:%S", t_obj)
            space = T_stamp.split(" ")[0].split("-")
            date = space[0] + "-" + space[1]

        if makeset:
            if date not in dates:
                dates.append(date)
        else:
            dates.append(date)

    return dates


# if rmv False, copies files from src to dst, else replaces
def moveFiles(src, dst, rmv):
    # look up folders that already exist
    existingFolders = next(os.walk(dst))[1]

    # print("existingFolders ", existingFolders)

    # look up folder dates in the existing folders
    oldDates = findDates(dst, existingFolders, True)

    newDates = []

    # print('pre-existing folders ', oldDates)

    # look up files from source
    files = [f for f in os.listdir(src) if os.path.isfile(os.path.join(src, f))]

    # keep a list of all creation dates
    fileDates = findDates(src, files, False)

    # filter
    for date in fileDates:
        if date not in oldDates and date not in newDates:
            newDates.append(date)

    # print("oldDates ", oldDates)
    # print("newDates ", newDates)

    # make new folders
    for n in newDates:
        # print(os.path.join(dst, n))
        os.makedirs(os.path.join(dst, n))

    # copy or move files
    for f in files:
        sourceFile = os.path.join(src, f)
        dstFile = os.path.join(dst, fileDates[files.index(f)], f)

        # remove
        if rmv:
            os.rename(sourceFile, dstFile)
            # print("file 'removed'")
        else:
            # TODO make folder if it doesn't exist
            shutil.copy2(sourceFile, dstFile)
            # print("file 'copied'")


if __name__ == '__main__':
    # get parameters from UI
    paths = dialog()

    if paths is None:
        sys.exit()

    thread = threading.Thread(moveFiles(paths[0], paths[1], paths[2]))
    thread.start()

    doneDialog()


