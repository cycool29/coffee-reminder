from queue import Queue  # nopep8
import configparser  # nopep8
import threading  # nopep8
import multiprocessing  # nopep8
import os  # nopep8

os.environ['PYSTRAY_BACKEND'] = 'gtk'  # nopep8
import gi  # nopep8

gi.require_version('Gtk', '3.0')  # nopep8
from gi.repository import Gtk  # nopep8
from PIL import ImageTk, Image  # nopep8
from tkinter import tix  # nopep8
import tkinter as tk  # nopep8
import datetime  # nopep8
import time  # nopep8
import webbrowser  # nopep8
import PySimpleGUIQt as sg  # nopep8
import plyer

if "DIRECTORY" not in os.environ:
    DIRECTORY = os.path.dirname(os.path.abspath(__file__))
else:
    DIRECTORY = os.getenv("DIRECTORY")
stop_timer_thread = False
quit_everything = False
show_notification = True
font = Gtk.Settings.get_default().get_property("gtk-font-name")
default_font_name = font.split(',')[0].replace(' ', '')
default_font_size = font[-2:]
default_font = default_font_name + ' ' + default_font_size

config = configparser.ConfigParser()
config.read(DIRECTORY + '/configurations.ini')
coffee_break_interval = config['CoffeeTime']['coffee_break_interval']
coffee_break_message = config['CoffeeTime']['coffee_break_message']
coffee_break_sound = config['CoffeeTime']['coffee_break_sound']
coffee_or_water = config['CoffeeTime']['coffee_or_water']
ramdom_daily_quotes = config['CoffeeTime']['ramdom_daily_quotes']
theme = config['CoffeeTime']['theme']


def open_subwindow(window):
    x = window()
    cycool29_is_very_cool = x.launch_window()
    del cycool29_is_very_cool


timer_event = threading.Event()


class CoffeeTimeTimer:
    def __init__(self):
        self.current_countdown_time_seconds = int(
            main_window.time_spinbox.get()) * 60
        self.total_countdown_time_seconds = self.current_countdown_time_seconds
        self.refresh_curent_time()

    def refresh_curent_time(self):
        self.current_time_seconds = int(datetime.datetime.now().strftime(
            "%H")) * 3600 + int(datetime.datetime.now().strftime(
                "%M")) * 60
        return self.current_time_seconds

    def calc_time(self, type):
        self.refresh_countdown_time()
        if type == 'next_break_time_seconds':
            return self.current_countdown_time_seconds + self.refresh_curent_time()

    def refresh_break_time(self):
        self.next_break_time_seconds = self.current_time_seconds + \
            self.current_countdown_time_seconds
        self.next_break_time_interval_seconds = self.next_break_time_seconds - \
            self.current_time_seconds
        self.next_break_time_interval_user = self.next_break_time_interval_seconds / 60

    def refresh_lefttime_label(self):
        try:
            if self.next_break_time_interval_user == 1:  # 1 minute later
                main_window.lefttime_label['text'] = "\nYour next coffee break is at a minute later."
                main_window.lefttime_label.pack()
            elif self.next_break_time_interval_user > 1:  # More than 1 minute later
                main_window.lefttime_label['text'] = "\nYour next coffee break is at " + str(
                    self.next_break_time_interval_user).split(
                    '.')[0] + " minutes later."
                main_window.lefttime_label.pack()
            elif self.next_break_time_interval_user < 1:  # Less than 1 minute later
                main_window.lefttime_label['text'] = "\nYour next coffee break is at less than a minute later."
                main_window.lefttime_label.pack()
            else:
                pass
        except:
            pass

    def reset_current_countdown_time(self):
        self.current_countdown_time_seconds = self.total_countdown_time_seconds

    def coffee_break_countdown(self):
        self.refresh_break_time()
        self.refresh_lefttime_label()

        while True:
            while current_countdown_time_seconds > 0:
                try:
                    print(current_countdown_time_seconds)
                    self.refresh_curent_time()
                    self.refresh_break_time()
                    self.refresh_lefttime_label()

                    current_countdown_time_seconds -= 1
                    time.sleep(1)

                except:
                    stop_timer_thread = True
                    break
                if stop_timer_thread == True:
                    break

            if show_notification == True:
                open_subwindow(NotificationWindow)
                self.reset_current_countdown_time()
            else:
                stop_timer_thread = True

    def start_coffee_break_countdown(self):
        main_window.window.withdraw()
        print('wow')

        if timer_thread.is_alive() == False:
            timer_thread.start()
            
        print('wow')


class MainWindow:
    def update_current_time_seconds(self):
        current_time = datetime.datetime.now().strftime("%H:%M")
        if quit_everything != True:
            self.time_label['text'] = "It's " + current_time + ' now.\n'
        self.window.after(1, self.update_current_time_seconds)

    def launch_window(self):
        self.window.protocol('WM_DELETE_WINDOW', withdraw_window)
        if theme.lower() == 'light':
            self.window.tk_setPalette(background='#d3d3d3')
        elif theme.lower() == 'dark':
            self.window.tk_setPalette(background='#1b1c1e')
        self.window.title("Coffee Time")
        self.window.geometry("450x600+" + str(int(screen_width / 2 - 225)) +
                             "+" + str(int(screen_height / 2 - 300)))
        self.window.iconphoto(
            True, ImageTk.PhotoImage(Image.open(f"{DIRECTORY}/icon.png")))
        self.window.deiconify()
        self.time_spinbox.pack()
        self.start_button.pack()

        # Logo frame
        tk.Label(master=self.logo_frame, image=self.logo_image).pack()
        self.logo_frame.pack()

        # Text frame
        self.time_label.pack()
        self.quote_label.pack()
        self.time_frame.pack()

        # Spinbox frame
        self.spinbox_separator.pack()
        self.time_spinbox.pack(side=tk.LEFT)
        self.time_unit.pack(side=tk.RIGHT)
        self.spinbox_frame.pack()

        # Start from spinbox
        self.start_button.pack(side=tk.BOTTOM, pady=10)
        self.start_frame.pack()

        # Left time
        main_window.lefttime_label.pack()
        self.lefttime_frame.pack()

        # Info frame
        self.github_button.bind(
            "<Button-1>",
            lambda e: open_url("https://github.com/cycool29/coffeetime"))
        self.sponsor_button.bind(
            "<Button-1>",
            lambda e: open_url("https://buymeacoffee.com/cycool29"))
        self.quit_button.bind("<Button-1>", quit_coffeetime)
        self.info_frame.pack(side="bottom", )
        self.github_button.pack(side="left", padx=5, pady=5)
        self.quit_button.pack(side="right", padx=5, pady=5)
        self.settings_button.pack(side="right", padx=5, pady=5)
        self.sponsor_button.pack(side="right", padx=5, pady=5)
        tix.Balloon(self.window).bind_widget(
            self.github_button, balloonmsg="View CoffeeTime GitHub page.")
        tix.Balloon(self.window).bind_widget(
            self.sponsor_button, balloonmsg="Buy cycool29 a coffee.")
        tix.Balloon(self.window).bind_widget(self.quit_button,
                                             balloonmsg="Quit CoffeeTime.")
        tix.Balloon(self.window).bind_widget(
            self.settings_button, balloonmsg="Change CoffeeTime settings.")

        self.update_current_time_seconds()

        self.window.mainloop()

    def show_window(self):
        self.window.wm_deiconify()
        # self.window.attributes('-topmost', 1)
        # self.window.attributes('-topmost', 0)

    def __init__(self) -> None:
        self.window = tix.Tk()
        self.time_spinbox = tk.Spinbox(self.window,
                                       from_=1,
                                       to=60,
                                       increment=1,
                                       width=3)
        self.logo_frame = tk.Frame(master=self.window)
        if theme.lower() == 'light':
            self.logo_image = ImageTk.PhotoImage(
                Image.open(f"{DIRECTORY}/proglogo-in-light-theme.png"))
        elif theme.lower() == 'dark':
            self.logo_image = ImageTk.PhotoImage(
                Image.open(f"{DIRECTORY}/proglogo-in-dark-theme.png"))
        self.time_frame = tk.Frame(master=self.window)
        self.time_label = tk.Label(master=self.time_frame,
                                   text="",
                                   font=default_font_name + ' 20')
        self.quote_label = tk.Label(
            master=self.time_frame,
            text="Focus, do what you do best.\nI will remind you when you need a rest. ;)",
            font=default_font)
        self.spinbox_value = 30
        self.spinbox_frame = tk.Frame(master=self.window, )
        self.spinbox_separator = tk.Label(master=self.window,
                                          text='\n\nCoffee break interval:',
                                          font=default_font)
        self.time_spinbox = tk.Spinbox(master=self.spinbox_frame,
                                       from_=0,
                                       to=10000,
                                       font=default_font,
                                       width=12,
                                       textvariable=self.spinbox_value)
        self.time_unit = tk.Label(master=self.spinbox_frame,
                                  text=' minutes',
                                  font=default_font)
        self.spinbox_value = 0
        self.start_frame = tk.Frame(master=self.window)
        self.start_button = tk.Button(master=self.start_frame,
                                      text='Start',
                                      command=start_coffee_break_countdown,
                                      font=default_font)
        self.lefttime_frame = tk.Label(master=self.window)
        self.lefttime_label = tk.Label(master=self.lefttime_frame,
                                       text='',
                                       font=default_font_name + ' 11')
        self.info_frame = tk.Frame(master=self.window)
        self.github_button = tk.Button(master=self.info_frame,
                                       text="GitHub",
                                       font=default_font_name + ' 11')
        self.sponsor_button = tk.Button(master=self.info_frame,
                                        text="Support",
                                        font=default_font_name + ' 11')
        self.quit_button = tk.Button(master=self.info_frame,
                                     text="Quit",
                                     font=default_font_name + ' 11')
        self.settings_button = tk.Button(
            master=self.info_frame,
            text="Settings",
            font=default_font_name + ' 11',
            command=lambda: open_subwindow(SettingsWindow))


# default coffee break interval
# default notification message
# default notification sound
# notiification sound?
# water or coffee
# random daily quote
# theme


class SettingsWindow:

    def launch_window(self):
        self.settings_window.geometry("450x650+" +
                                      str(int(screen_width / 2 - 225)) + "+" +
                                      str(int(screen_height / 2 - 325)))
        self.settings_window.title('CoffeeTime Settings')
        self.settings_title_label.pack()
        self.settings_title_frame.pack()
        self.coffee_break_interval_label.pack()
        self.coffee_break_interval_spinbox.pack()
        self.coffee_break_interval_frame.pack()
        self.coffee_break_message_label.pack()
        self.coffee_break_message_entry.pack()
        self.coffee_break_message_frame.pack()
        self.coffee_break_sound_label.pack()
        self.coffee_break_sound_button.pack()
        self.coffee_break_sound_frame.pack()
        self.theme_label.pack()
        self.theme_spinbox.pack()
        self.theme_frame.pack()
        self.settings_window.mainloop()

    def change_theme(self):
        self.update_config()
        main_window.window.tk_setPalette(background='#1b1c1e')
        main_window.window.update()

    def update_config(self):
        config['CoffeeTime'][
            'coffee_break_interval'] = self.coffee_break_interval_spinbox.get(
        )
        config['CoffeeTime'][
            'coffee_break_message'] = self.coffee_break_message_entry.get()
        config['CoffeeTime']['coffee_break_sound'] = self.coffee_break_sound
        config['CoffeeTime']['theme'] = self.theme_spinbox.get().lower()

        with open('configurations.ini', 'w') as configfile:
            config.write(configfile)

    def choose_sound_file(self):
        self.coffee_break_sound = \
            plyer.filechooser.open_file(filters=["*mp3", "*ogg", "*aac"], title='Choose a sound file',
                                        icon=f'{DIRECTORY}/icon.png')[0]
        if os.path.isfile(self.coffee_break_sound):
            self.update_config()

    def __init__(self) -> None:
        self.settings_window = tk.Toplevel()
        self.coffee_break_interval_stringvar = tk.StringVar(
            value=coffee_break_interval)
        self.coffee_break_message_stringvar = tk.StringVar(
            value=coffee_break_message)
        self.theme_stringvar = tk.StringVar(value=theme)
        if theme.lower() == 'dark':
            self.theme_values = ['Dark', 'Light']
        else:
            self.theme_values = ['Light', 'Dark']
        self.coffee_break_sound = ''

        self.settings_title_frame = tk.Frame(master=self.settings_window)
        self.settings_title_label = tk.Label(master=self.settings_title_frame,
                                             text='Settings\n',
                                             font=default_font_name + ' 25')

        self.coffee_break_interval_frame = tk.Frame(
            master=self.settings_window)
        self.coffee_break_interval_label = tk.Label(
            master=self.coffee_break_interval_frame,
            text='Coffee break interval:',
            font=default_font)
        self.coffee_break_interval_spinbox = tk.Spinbox(
            master=self.coffee_break_interval_frame,
            from_=1,
            to=10000,
            textvariable=self.coffee_break_interval_stringvar,
            font=default_font,
            command=self.update_config)

        self.coffee_break_message_frame = tk.Frame(master=self.settings_window)
        self.coffee_break_message_label = tk.Label(
            master=self.coffee_break_message_frame,
            text='\nCoffee break message:',
            font=default_font)
        self.coffee_break_message_entry = tk.Entry(
            master=self.coffee_break_message_frame,
            textvariable=self.coffee_break_message_stringvar,
            font=default_font,
            validatecommand=self.update_config)

        self.coffee_break_sound_frame = tk.Frame(master=self.settings_window)
        self.coffee_break_sound_label = tk.Label(
            master=self.coffee_break_sound_frame,
            text='\nSelect a coffee break sound effect:',
            font=default_font)
        self.coffee_break_sound_button = tk.Button(
            master=self.coffee_break_sound_frame,
            text='Select file',
            font=default_font,
            command=self.choose_sound_file)

        self.theme_frame = tk.Frame(master=self.settings_window)
        self.theme_label = tk.Label(master=self.theme_frame,
                                    text='\nSelect a theme:',
                                    font=default_font)
        self.theme_spinbox = tk.Spinbox(master=self.theme_frame,
                                        textvariable=self.theme_stringvar,
                                        font=default_font,
                                        command=self.change_theme,
                                        values=self.theme_values,
                                        wrap=True)


class NotificationWindow:

    def __init__(self) -> None:
        self.notification_window = tk.Toplevel()
        self.notification_label = tk.Label(self.notification_window,
                                           text="\nTake a coffee break!",
                                           font=default_font_name + " 20")
        self.logo_image = ImageTk.PhotoImage(
            Image.open(f"{DIRECTORY}/icon.png"))

    def launch_window(self):
        self.notification_window.attributes('-topmost', 'true')
        self.notification_window.iconphoto(False, self.logo_image)
        self.notification_window.title("Coffee Break!")
        self.notification_window.geometry("300x100+" +
                                          str(int(screen_width / 2 - 150)) +
                                          "+" +
                                          str(int(screen_height / 2 - 50)))
        self.notification_window.resizable(False, False)
        self.notification_label.pack()
        while tk.Toplevel.winfo_exists(self.notification_window):
            self.notification_window.geometry("300x100+" +
                                              str(int(screen_width / 2 -
                                                      150)) + "+" +
                                              str(int(screen_height / 2 - 50)))
            self.notification_window.update()
            time.sleep(1)
            print('waiting')


def system_tray_icon():
    global show_main_window
    global tray
    menu_def = ['File', ['Show', 'Exit']]
    tray = sg.SystemTray(menu=menu_def,
                         filename='/home/pi/coffeetime/src/icon.png')
    while True:
        menu_item = tray.Read(timeout=0)
        if menu_item != None and menu_item != '__TIMEOUT__':
            print(menu_item)

        if menu_item == 'Show' or menu_item == '__ACTIVATED__':
            if show_main_window_task_queue.full() == False:
                print('wow')
                show_main_window_task_queue.put('show_main_window')

        elif menu_item == 'Exit':
            quit_coffeetime()

        time.sleep(0.1)


def start_coffee_break_countdown():
    print(timer)
    timer.start_coffee_break_countdown()


timer_thread = threading.Thread(target=start_coffee_break_countdown,
                                name='CoffeeTime Timer')

main_window = MainWindow()
timer = CoffeeTimeTimer()


show_main_window_task_queue = Queue(maxsize=1)


def withdraw_window(window=main_window.window):
    window.withdraw()
    show_main_window_task_queue.empty()
    if window == main_window.window:
        # wait for user to select show on tray
        while show_main_window_task_queue.get() != 'show_main_window':
            print('hey')
            pass

        window.wm_deiconify()
        # show_main_window_task_queue.empty()


def open_url(url):
    webbrowser.open(url)


def quit_coffeetime(window=None):
    global stop_timer_thread
    global quit_everything
    stop_timer_thread = True
    quit_everything = True
    os._exit(0)


screen_width = main_window.window.winfo_screenwidth()
screen_height = main_window.window.winfo_screenheight()
threading.Thread(target=system_tray_icon, name='CoffeeTime SysTray').start()

if __name__ == '__main__':
    main_window.launch_window()
