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


def path_exists(path_parts: [str]):
    path = path_join(path_parts)
    return os.path.exists(path)


def path_join(path_parts: [str]):
    return '/'.join(path_parts)


def create_dir_if_none(path_parts: [str]):
    path = path_join(path_parts)
    if not os.path.exists(path):
        os.mkdir(path)


# Copy files from src to dst if rmv True, else move
def move_files(src, dst, rmv):
    files = [f for f in os.listdir(src) if os.path.isfile(os.path.join(src, f))]

    for file in files:
        year, month = file[:4], file[4:6]

        create_dir_if_none([dst, year])

        create_dir_if_none([dst, year, month])

        file_source = path_join([src, file])
        file_destination = path_join([dst, year, month, file])

        if not os.path.exists(file_destination):  # either move or copy
            if rmv:
                os.rename(file_source, file_destination)
            else:
                shutil.copy(file_source, file_destination)

        elif rmv:  # remove or do nothing
            os.remove(file_source)


if __name__ == '__main__':
    # get parameters from UI
    params = dialog()

    if params is None:
        sys.exit()

    (source, destination, remove) = (params[0], params[1], params[2])
    thread = threading.Thread(move_files(source, destination, remove))
    thread.start()

    done_dialog()


