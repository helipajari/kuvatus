import os
import shutil
import sys
import threading
from configparser import ConfigParser

import FreeSimpleGUI as gui

name = "Kuvatus"
THEME = 'LightBlue'
bg = 'pink'
IMG_PATH = 'src/img/'


def create_config_file():
    """
    Creates config.ini from template in /config if one doesn't exist.
    Throws config_not_found error if /config doesn't exist.
    """
    default_path = 'src/config/config_template.ini'

    try:
        f = open(default_path, 'r', encoding="utf-8")
        txt = f.read()
        f.close()

        path = 'config.ini'
        flags = os.O_RDWR | os.O_CREAT
        fd = os.open(path, flags)

        os.write(fd, str.encode(txt))
    except FileNotFoundError:
        config_not_found_error_dialog()
        sys.exit()


def get_config():
    """
    Returns ConfigParser() read from config.ini
    """
    if not os.path.exists("config.ini"):
        create_config_file()

    config = ConfigParser()

    config.read("config.ini", encoding="utf-8")
    return config


def read_config_file():
    """
    Reads program settings, returns src, dst, rmv, month_use, month_names
    """
    config = get_config()

    src = config['FILEPATHS']['source']

    usr = os.environ['USERPROFILE']
    folder = config['FILEPATHS']['destination']

    if int(config['FILEPATHS']['store_under_user']):
        dst = os.path.join(usr, folder)
    else:
        dst = folder

    rmv = int(config['PREFERENCES']['remove'])

    month_use = int(config['PREFERENCES']['month_names'])

    month_names = config['PREFERENCES']['months'].split('\n')

    return src, dst, rmv, month_use, month_names


def update_config_file(src, dst, rmv, month_use):
    config = get_config()
    config['FILEPATHS']['source'] = str(src)
    config['FILEPATHS']['destination'] = str(dst)
    config['FILEPATHS']['store_under_user'] = '0'       # user has provided a path, default setting not needed anymore
    config.set('PREFERENCES', 'remove', '1' if rmv else '0')
    config.set('PREFERENCES', 'month_names', '1' if month_use else '0')

    with open('config.ini', 'w', encoding='utf-8') as configfile:
        config.write(configfile)


def main_dialog(init_src, init_dst, init_rmv, init_mths):
    """
    Returns: source, dst, rmv, use
    """
    gui.theme(THEME)

    src_txt = init_src if os.path.exists(init_src) else "etsi kansio"
    src_str = 'Muuta' if src_txt is init_src else 'Etsi'
    src_browse = gui.FolderBrowse(src_str, initial_folder=src_txt)

    dst_txt = init_dst if os.path.exists(init_dst) else "etsi kansio"
    dst_str = 'Muuta' if dst_txt is init_dst else 'Etsi'
    dst_browse = gui.FolderBrowse(dst_str, initial_folder=dst_txt)

    rmv_txt = [gui.Checkbox("Poista siirretyt kuvat lähdekansiosta?", default=init_rmv)]
    use_mth = [gui.Checkbox("Käytä kuukausien nimiä kansioissa?", default=init_mths)]

    layout = [[gui.Text('Lähdekansion polku: '), gui.Text(src_txt), src_browse],
              [gui.Text('Kohdekansion polku: '), gui.Text(dst_txt), dst_browse],
              rmv_txt,
              use_mth,
              [gui.Button('Ok'), gui.Button('Sulje')]]

    window = get_window(layout)

    old_element, old_bg = None, None

    # template items used for resetting the background color of unfocused elements
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
            use = layout[3][0].get()

            if os.path.exists(src) and os.path.exists(dst) and src != dst:
                return src, dst, rmv, use
            else:
                validation_warning_dialog(src, dst)
    window.close()


def config_not_found_error_dialog():
    gui.theme(THEME)

    warning_title = gui.Text('Virhe asennuksessa!', font='bold')
    img = get_error_img()

    warning = gui.Text('\nKuvatus ei löytänyt config-kansiota eikä voinut käynnistyä.\n\n'
                       + 'Varmista seuraavat kohdat:'
                         '\n - kuvatus.exe (sovellus, ei pikakuvake) ja'
                       + '\n   src-kansio ovat samassa alakansiossa'
                       + '\n - config-kansio on src-kansiossa\n\n'
                       + 'Tarkista tiedot ja käynnistä Kuvatus uudelleen.\n')

    ok_btn = gui.Button('Ok, sulje ohjelma')

    layout = [[warning_title, img], [warning], [ok_btn]]

    window = get_window(layout)

    while True:
        event, values = window.read()
        if event == gui.WIN_CLOSED or event == 'Ok, sulje ohjelma':
            break

    window.close()


def months_config_error_dialog(mths):
    gui.theme(THEME)

    warning_title = gui.Text('Virhe ohjelma-asetuksissa!', font='bold')
    img = get_error_img()

    warning = gui.Text('\nOdotettu kuukausien lukumäärä 12.\n\n'
                       + 'Kuvatuksen asetuksiin on määritelty ' + str(mths) + ' kuukautta.\n\n'
                       + 'Tarkista asetukset config.ini-tiedostossa ja käynnistä Kuvatus uudelleen.\n')

    ok_btn = gui.Button('Ok, sulje ohjelma')
    layout = [[warning_title, img], [warning], [ok_btn]]

    window = get_window(layout)

    while True:
        event, values = window.read()
        if event == gui.WIN_CLOSED or event == 'Ok, sulje ohjelma':
            break

    window.close()


def done_dialog():
    gui.theme(THEME)

    ok_btn = gui.Button('Ok, sulje ohjelma', button_color=bg)
    img = get_succ_img()

    layout = [[gui.Text('Valmis!'), img],
              [ok_btn]]

    window = get_window(layout)
    ok_btn.set_focus()

    while True:
        event, values = window.read()
        if event == 'Ok, sulje ohjelma':
            break


def validation_warning_dialog(src, dst):
    gui.theme(THEME)

    title = gui.Text('Varoitus!')
    img = get_warn_img()
    layout = [[title, img]]

    layout += [[gui.Text('Kuvatus ei voi siirtää tiedostoja koska:')]]

    if not os.path.exists(src):
        src_gui = [[gui.Text(" - lähdekansion polku ei ole olemassa")]]
        layout += src_gui

    if not os.path.exists(dst):
        dst_gui = [[gui.Text(" - kohdekansion polku ei ole olemassa")]]
        layout += dst_gui

    if src == dst:
        layout += [[gui.Text(" - lähdekansio on sama kuin kohdekansio")]]

    layout += [[gui.Text("Tarkista tiedot ja yritä uudelleen.")]]

    ok_btn = gui.Button('Ok', button_color=bg)
    layout += [[ok_btn]]

    window = get_window(layout)
    ok_btn.set_focus()

    while True:
        event, values = window.read()
        if event == 'Ok' or event == gui.WIN_CLOSED:
            break

    window.close()


def get_window(layout: []):
    icon = get_img_path('kuvatus logo.ico')
    return gui.Window(title=name, layout=layout, icon=icon, finalize=True, return_keyboard_events=True, scaling=2.5)


def get_img(img: str):
    """
    Returns an image object with specified image.
    """
    path = get_img_path(img)
    return gui.Image(source=path, expand_x=True, subsample=6)


def get_img_path(img: str):
    """Helper function for getting images, returns path to specified image"""
    return os.path.join(IMG_PATH, img)


def get_succ_img():
    return get_img('kuvatus success.png')


def get_warn_img():
    return get_img('kuvatus warning.png')


def get_error_img():
    return get_img('kuvatus error.png')


def path_exists(path_parts: [str]):
    """
    Checks if the path formed by given array of strings exists.
    """
    path = path_join(path_parts)
    return os.path.exists(path)


def path_join(path_parts: [str]):
    """
    Makes a path out of an array of strings.
    """
    return '/'.join(path_parts)


def create_dir_if_none(path_parts: [str]):
    path = path_join(path_parts)
    if not os.path.exists(path):
        os.mkdir(path)


def check_month_name(path_parts: [str], short_conv: str, long_conv: str, use_mth: bool):
    """
    Checks if a folder under different naming convention wrt user choice exists.
    Renames to new convention if yes, else creates a new folder if one doesn't exist yet.
    """
    short_path = path_join(path_parts + [short_conv])
    long_path = path_join(path_parts + [long_conv])

    if use_mth:
        if os.path.exists(short_path):
            os.rename(short_path, long_path)
        elif not os.path.exists(long_path):
            os.mkdir(long_path)

    if not use_mth:
        if os.path.exists(long_path):
            os.rename(long_path, short_path)
        elif not os.path.exists(short_path):
            os.mkdir(short_path)


def move_files(src, dst, rmv, use_months, months):
    """
        Copy files from src to dst if rmv True, else move
    """
    files = [f for f in os.listdir(src) if os.path.isfile(os.path.join(src, f))]

    for file in files:
        year, month = file[:4], file[4:6]

        create_dir_if_none([dst, year])

        long_month = month + ' ' + months[int(month) - 1]

        check_month_name([dst, year], month, long_month, bool(use_months))

        if use_months:
            month = long_month

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

    # must have correct number of months even if months are not used
    if len(months) != 12:
        months_config_error_dialog(len(months))
        sys.exit()

    params = main_dialog(init_src, init_dst, init_rmv, init_use_mths)

    if params is None:
        sys.exit()

    (source, destination, remove, use_months) = (params[0], params[1], params[2], params[3])

    thread = threading.Thread(move_files(source, destination, remove, use_months, months))
    thread.start()

    update_config_file(source, destination, remove, use_months)
    done_dialog()
