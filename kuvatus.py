import os
import re
import shutil
import sys
import threading
import time

import FreeSimpleGUI as gui
from configparser import ConfigParser

name = "Kuvatus"
THEME = 'LightBlue'
bg = 'pink'


def create_config_file():
    path = 'config.ini'
    flags = os.O_RDWR | os.O_CREAT
    fd = os.open(path, flags)
    default_path = 'config/config.ini'
    f = open(default_path, 'r')
    txt = f.read()
    f.close()
    os.write(fd, str.encode(txt))


def read_config_file():
    if not os.path.exists("config.ini"):
        create_config_file()

    config = ConfigParser()

    config.read("config.ini", encoding="UTF-8")

    src = config['FILEPATHS']['source']

    usr = os.environ['USERPROFILE']
    folder = config['FILEPATHS']['destination']

    if int(config['FILEPATHS']['store_under_user']):
        dst = os.path.join(usr, folder)
    else:
        dst = folder

    rmv = int(config['PREFERENCES']['remove'])

    use_months = int(config['PREFERENCES']['month_names'])

    months = config['PREFERENCES']['months'].split('\n')
    print(months)

    return src, dst, rmv, use_months, months


def main_dialog(init_src, init_dst, init_rmv, init_mths):
    gui.theme(THEME)

    src_str = 'Muuta'

    if not os.path.exists(init_src):
        init_src = "etsi kansio"
        src_str = 'Etsi'
    src_btn = gui.FolderBrowse(src_str, initial_folder=init_src, key='src')

    dst_str = 'Muuta'
    if not os.path.exists(init_dst):
        init_dst = "etsi kansio"
        dst_str = 'Etsi'

    dst_btn = gui.FolderBrowse(dst_str, initial_folder=init_dst, key='dst')

    rmv_txt = [gui.Checkbox("Poista siirretyt kuvat lähdekansiosta?", default=init_rmv)]

    # TODO add ability to save preferences
    layout = [[gui.Text('Lähdekansion polku: '), gui.Text(init_src), src_btn],
              [gui.Text('Kohdekansion polku: '), gui.Text(init_dst), dst_btn],
              rmv_txt,
              [gui.Button('Ok'), gui.Button('Sulje')]]

    # WINDOW MADE HERE
    window = gui.Window(name, layout, return_keyboard_events=True, icon='kuvatus.ico', scaling=2.5)

    old_element, old_bg = None, None

    base_btn = gui.Button('')
    base_chk = gui.Checkbox('')

    while True:
        event, values = window.read()
        new_element = window.find_element_with_focus()

        if new_element != old_element:

            if isinstance(old_element, gui.Button):
                old_element.update(button_color=base_btn.ButtonColor)

            if isinstance(old_element, gui.Checkbox):
                old_element.update(background_color=base_chk.BackgroundColor)

            if isinstance(new_element, gui.Button):
                old_element = new_element
                old_element.update(button_color=bg)

            if isinstance(new_element, gui.Checkbox):
                old_element = new_element
                old_element.update(background_color=bg)

        if event == gui.WIN_CLOSED or event == 'Sulje':
            break

        if event == 'Ok':
            src = layout[0][1].get()
            dst = layout[1][1].get()
            rmv = layout[2][0].get()

            if os.path.exists(src) and os.path.exists(dst):
                return src, dst, rmv, months
            else:
                validation_error_dialog(src, dst)
    window.close()


def months_config_error_dialog(mths):
    gui.theme(THEME)

    warning_title = gui.Text('Virhe ohjelma-asetuksissa!', font='bold')
    warning = gui.Text('\nOdotettu kuukausien lukumäärä 12.\n\n'
                       + 'Kuvatuksen asetuksiin on määritelty ' + str(mths) + ' kuukautta.\n\n'
                       + 'Tarkista asetukset ja käynnistä Kuvatus uudelleen.\n')

    ok_btn = gui.Button('Ok, sulje ohjelma')

    layout = [[warning_title], [warning], [ok_btn]]

    window = gui.Window(name, layout, finalize=True, icon='kuvatus.ico', scaling=1.5)

    while True:
        event, values = window.read()
        if event == gui.WIN_CLOSED or event == 'Ok, sulje ohjelma':
            break

    window.close()


def done_dialog():
    gui.theme(THEME)

    ok_btn = gui.Button('Ok', button_color=bg)

    layout = [[gui.Text('Valmis!')], [], [],
              [ok_btn], [], []]

    window = gui.Window(name, layout, finalize=True, icon='kuvatus.ico')
    ok_btn.set_focus()

    while True:
        event, values = window.read()
        if event == 'Ok':
            break

    window.close()


def validation_error_dialog(src, dst):
    gui.theme(THEME)

    layout = [[gui.Text('Virhe!')], [], [],
              [gui.Text('Tarkista seuraavat tiedot:')], [], [],
              ]

    if not os.path.exists(src):
        src_gui = [[gui.Text("- lähdekansion polku")], [], []]
        layout += src_gui

    if not os.path.exists(dst):
        dst_gui = [[gui.Text("- kohdekansion polku")], [], []]
        layout += dst_gui

    ok_btn = gui.Button('Ok', button_color=bg)
    layout += [[ok_btn], [], []]

    window = gui.Window(name, layout, finalize=True, icon='kuvatus.ico')
    ok_btn.set_focus()

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
def move_files(src, dst, rmv, months):
    files = [f for f in os.listdir(src) if os.path.isfile(os.path.join(src, f))]

    for file in files:
        year, month = file[:4], file[4:6]

        create_dir_if_none([dst, year])

        # add suffix to month if mths is not None
        month = month + ' ' + months[int(month) - 1] if months else month

        # TOD) don't create duplicates! either 01 or 01 tammi existing is ok!
        create_dir_if_none([dst, year, month])

        file_source = path_join([src, file])
        file_destination = path_join([dst, year, month, file])

        if not os.path.exists(file_destination):
            if rmv:
                os.rename(file_source, file_destination)
            else:
                shutil.copy(file_source, file_destination)

        elif rmv:
            os.remove(file_source)


if __name__ == '__main__':
    init_src, init_dst, init_rmv, init_use_mths, months = read_config_file()

    # must have correct months even if months are not used
    if len(init_mths) != 12:
        months_config_error_dialog(len(init_mths))
        sys.exit()

    # get parameters from UI
    params = main_dialog(init_src, init_dst, init_rmv, init_use_mths)

    if params is None:
        sys.exit()

    (source, destination, remove, use_months) = (params[0], params[1], params[2], init_use_mths)

    months = months if use_months else None

    thread = threading.Thread(move_files(source, destination, remove, months))
    thread.start()

    done_dialog()
