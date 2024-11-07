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
# returns tuple with parameters
def dialog():
    gui.theme('DarkAmber')

    # on laptops try D because usually no extra discs
    init_mem = os.path.join('D:\\', '')
    mem = gui.FolderBrowse('Muuta', initial_folder=init_mem, key='mem')
    mem_t = "etsi kansio"

    init_pic = os.path.join(os.environ['USERPROFILE'], 'pictures')
    pic = gui.FolderBrowse('Muuta', initial_folder=init_pic, key='pic')
    pic_t = "etsi kansio"

    ok = gui.Button('Ok', disabled=False)

    layout = [[gui.Text('Lähdekansion polku: '), gui.Text(mem_t), mem],
              [gui.Text('Kohdekansion polku: '), gui.Text(init_pic), pic],
              [gui.Checkbox("Poista siirretyt kuvat lähdekansiosta?")],
              [ok, gui.Button('Peruuta')]]

    # WINDOW MADE HERE
    window = gui.Window(name + " " + version.__str__(), layout)

    while True:
        event, values = window.read()

        if event == gui.WIN_CLOSED or event == 'Peruuta':
            break

        if event == 'Ok':
            # TODO disable ok unless mem and pic are not default value?
            if layout[0][1].get() == mem_t:
                continue
            # mem, pic, delete
            return layout[0][1].get(), layout[1][1].get(), layout[2][0].get()
    window.close()


def done_dialog():
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
def find_dates(src, files, make_set):
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

        if make_set:
            if date not in dates:
                dates.append(date)
        else:
            dates.append(date)

    return dates


# if rmv False, copy files from src to dst, else move
def move_files(src, dst, rmv):
    # look up folders that already exist
    existing_folders = next(os.walk(dst))[1]

    # print("existingFolders ", existingFolders)

    # look up folder dates in the existing folders
    old_dates = find_dates(dst, existing_folders, True)

    new_dates = []

    # print('pre-existing folders ', oldDates)

    # look up files from source
    files = [f for f in os.listdir(src) if os.path.isfile(os.path.join(src, f))]

    # keep a list of all creation dates
    file_dates = find_dates(src, files, False)

    # filter
    for date in file_dates:
        if date not in old_dates and date not in new_dates:
            new_dates.append(date)

    # print("oldDates ", oldDates)
    # print("newDates ", newDates)

    # make new folders
    for n in new_dates:
        # print(os.path.join(dst, n))
        os.makedirs(os.path.join(dst, n))

    # copy or move files
    for f in files:
        source_file = os.path.join(src, f)
        dst_file = os.path.join(dst, file_dates[files.index(f)], f)

        # remove
        if rmv:
            os.rename(source_file, dst_file)
            # print("file 'removed'")
        else:
            # TODO make folder if it doesn't exist
            shutil.copy2(source_file, dst_file)
            # print("file 'copied'")


if __name__ == '__main__':
    # get parameters from UI
    params = dialog()

    if params is None:
        sys.exit()

    (src, dst, rmv) = (params[0], params[1], params[2])
    thread = threading.Thread(move_files(src, dst, rmv))
    thread.start()

    done_dialog()


