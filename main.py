from kivy.config import Config
Config.set('graphics', 'width', '480')
Config.set('graphics', 'height', '700')
Config.set('graphics', 'resizable', False)  # Jeśli nie chcesz, żeby okno było skalowalne

import multiprocessing
import os
import atexit
import subprocess
import time
import base64
import sys
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle  # Import do rysowania tła
from kivy.graphics import Color, Ellipse  # Import do rysowania kółka
from kivy.core.audio import SoundLoader
from functools import partial
import win32gui
# TO DO:
# ZROBIC BACKUP 
# bo rozwalimy ludziom systemy jak cos sie ... xD 

sites_to_block = ["facebook.com", "instagram.com", "linkedin.com",  "youtube.com", "pornhub.com", "tiktok.com"] 
hosts_path = r"C:\Windows\System32\drivers\etc\hosts"  # Windows
# hosts_path = "/etc/hosts"  # MacOS/Linux
redirect_ip = "127.0.0.1"

def resource_path(relative_path):
    """Zwraca ścieżkę do zasobu dla pliku .exe"""
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def get_active_window_title(sites):
    while True:
        window = win32gui.GetForegroundWindow()
        active_window = win32gui.GetWindowText(window)
        active_window = active_window.lower()

        for site in sites:
            if strip_site(site) in active_window:
                os.system("start https://matela7.github.io/")
            time.sleep(0.1)  
        #time.sleep(1)  

def strip_site(site):
    return site.replace("http://", "").replace("https://", "").replace("www.", "").replace(".com", "").split("/")[0].lower()
# Funkcja wyświetlająca popup z błędem
def error_popup(number):
    if number == 0:
        popup1 = Popup(title='ERROR CORGI IS ANGRY',
            content=Label(text='You have to run this program as an administrator \n to block websites!'),
            size_hint=(None, None), size=(400, 400))
        popup1.open()
    elif number == 1:
        popup2 = Popup(title='ERROR CORGI IS ANGRY',
            content=Label(text='You have to run this program as an administrator \n to unblock websites!'),
            size_hint=(None, None), size=(400, 400))
        popup2.open()
    else:
        popup3 = Popup(title='ERROR CORGI IS ANGRY',
            content=Label(text='Something went wrong!'),
            size_hint=(None, None), size=(400, 400))
        popup3.open()

def block_sites(hosts_path, sites_to_block, redirect_ip):
    if main_iterator.main_iterator == False:
        try:
            with open(hosts_path, 'r+') as file:
                hosts = file.read()
                for site in sites_to_block:
                    if site not in hosts:
                        file.write(redirect_ip + " " + site + "\n")
            print("Strony zablokowane.")
        except PermissionError:
            print(f"Brak uprawnień do zapisu w pliku hosts. Uruchom program jako administrator. {PermissionError}")
            error_popup(0)
    else:
        global get_active_window_title_process
        get_active_window_title_process = multiprocessing.Process(target=run_get_active_window_title, args=(sites_to_block,), daemon=True)
        get_active_window_title_process.start()

def unblock_sites(hosts_path, sites_to_block, redirect_ip):
    if main_iterator.main_iterator == True:
        try:
            get_active_window_title_process.terminate()
            get_active_window_title_process.join()
            if get_active_window_title_process.is_alive():
                get_active_window_title_process.kill()
        except Exception as e:
            print(e)
            pass
    else:   
        try:
            with open(hosts_path, 'r+') as file:
                lines = file.readlines()
                file.seek(0)
                for line in lines:
                    if not any(site in line for site in sites_to_block):
                        file.write(line)
                file.truncate()
            print("Strony odblokowane.")
        except PermissionError:
            print(f"Brak uprawnień do zapisu w pliku hosts. Uruchom program jako administrator. {PermissionError}")
            error_popup(1)

class MainIterator:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(MainIterator, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self._main_iterator = True
    
    @property
    def main_iterator(self):
        return self._main_iterator
    
    @main_iterator.setter
    def main_iterator(self, value):
        self._main_iterator = value


# Główna strona
class FirstScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=50, spacing=5)

        # Dodawanie koloru tła
        with layout.canvas.before:
            Color(0.647, 0.216, 0.992, 1)  # Kolor RGB
            self.rect = Rectangle(size=self.size, pos=self.pos)
            layout.bind(size=self._update_rect, pos=self._update_rect)

        text = Label(text="CORGI FOCUS", font_size='33sp', size_hint=(1, 0.2))
        layout.add_widget(text)  # Główny napis

        horizontal_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.5))
        image = Image(source=resource_path('korki.gif'), size_hint=(0.5, 1))
        horizontal_layout.add_widget(image)  # Obrazek animowany

        layout.add_widget(horizontal_layout)

        # Circle directly below the Corgi image
        with layout.canvas.after:
            self.circle_color = Color(0, 1, 0, 1)  # Initial color red (blocked)
            self.circle = Ellipse(size=(50, 50), pos=(self.width / 2 - 25, 150))  # Adjust pos as needed

        layout.bind(size=self._update_circle, pos=self._update_circle)

        # Tworzenie głównego layoutu dla przycisków
        buttons_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.2))

        # Tworzenie przycisku "BLOCK"
        button_block = Button(text="BLOCK", font_size='15sp', size_hint=(0.15, 0.25))
        button_block.bind(on_press=partial(self.on_block_button_press))
        buttons_layout.add_widget(button_block)  # Dodanie przycisku do layoutu

        # Dodanie pierwszego odstępu
        spacer1 = Widget(size_hint=(0.1, 1))
        buttons_layout.add_widget(spacer1)

        # Tworzenie przycisku "Change mode"
        self.button_change = Button(
            text="Block mode" if not main_iterator.main_iterator else "Popup mode",
            font_size='15sp', size_hint=(0.15, 0.25)
        )
        self.button_change.bind(on_press=self.on_change_button_press)
        buttons_layout.add_widget(self.button_change)

        # Dodanie drugiego odstępu
        spacer2 = Widget(size_hint=(0.1, 1))
        buttons_layout.add_widget(spacer2)

        # Tworzenie przycisku "Next"
        button_next = Button(text="Next", font_size='15sp', size_hint=(0.15, 0.25))
        button_next.bind(on_press=self.on_next_button_press)
        buttons_layout.add_widget(button_next)  # Dodanie przycisku do layoutu

        # Dodanie layoutu przycisków do głównego layoutu
        layout.add_widget(buttons_layout)

        # Drugi zestaw przycisków
        buttons_layout2 = BoxLayout(orientation='horizontal', size_hint=(1, 0.2))
        button_block2 = Button(text="BLOCK", font_size='20sp', size_hint=(0.3, 0.5))
        button_block2.bind(on_press=partial(self.on_block_button_press))
        buttons_layout2.add_widget(button_block2)  # Przyciski blokujące

        spacer3 = Widget(size_hint=(0.1, 1))
        buttons_layout2.add_widget(spacer3)

        button_unblock = Button(text="UNBLOCK", font_size='20sp', size_hint=(0.3, 0.5))
        button_unblock.bind(on_press=partial(self.on_unblock_button_press))
        buttons_layout2.add_widget(button_unblock)  # Przyciski odblokowujące

        spacer4 = Widget(size_hint=(0.1, 1))
        buttons_layout2.add_widget(spacer4)

        button_next2 = Button(text="Next", font_size='20sp', size_hint=(0.3, 0.5))
        button_next2.bind(on_press=self.on_next_button_press)
        buttons_layout2.add_widget(button_next2)  # Przycisk przechodzący do drugiej strony
        layout.add_widget(buttons_layout2)

        self.add_widget(layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def _update_circle(self, instance, value):
        self.circle.pos = (self.width / 2 - 25, self.height * 0.30)  # Update circle position based on layout size

    def on_block_button_press(self, instance):
        block_sites(hosts_path, sites_to_block, redirect_ip)
        self.circle_color.rgba = (1, 0, 0, 1)  # Change circle color to green when blocked

    def on_unblock_button_press(self, instance):
        unblock_sites(hosts_path, sites_to_block, redirect_ip)
        self.circle_color.rgba = (0, 1, 0, 1)  # Change circle color to red when unblocked(0, 1, 0, 1) 

    def on_change_button_press(self, instance):
        # Zmiana stanu trybu
        if main_iterator.main_iterator:
            main_iterator.main_iterator = False
            self.button_change.text = "Block mode"
        else:
            main_iterator.main_iterator = True
            self.button_change.text = "Popup mode"
        print(main_iterator.main_iterator)

    def on_next_button_press(self, instance):
        self.manager.current = 'second'


# Druga strona
class SecondScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        text = Label(text="Manage Websites", font_size='30sp', size_hint=(1, 0.1))
        layout.add_widget(text)

        scrollview = ScrollView(size_hint=(1, 0.8))
        grid = GridLayout(cols=1, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))

        for site in sites_to_block:
            lbl = Label(text=site, font_size='20sp', size_hint_y=None, height=40)
            grid.add_widget(lbl)

        scrollview.add_widget(grid)
        layout.add_widget(scrollview)

        button_prev = Button(text="Previous", font_size='20sp', size_hint=(1, 0.1))
        button_prev.bind(on_press=self.on_prev_button_press)
        layout.add_widget(button_prev)

        self.add_widget(layout)
        
    def on_prev_button_press(self, instance):
        self.manager.current = 'first'

# Klasa główna, aplikacja
class MyApp(App):
    icon = "icon.png" #or icon.ico
    title = "CORGI FOCUS"
    def build(self):
        self.play_sound_on_startup()
        global main_iterator
        main_iterator = MainIterator()  # Singleton instancja klasy MainIterator
        screen_manager = ScreenManager()
        screen_manager.add_widget(FirstScreen(name='first'))
        screen_manager.add_widget(SecondScreen(name='second'))
        return screen_manager
    
    def play_sound_on_startup(self):
        sound = SoundLoader.load(resource_path('corgi_bark.mp3'))
        if sound:
            sound.play()   

    def on_request_close(self, *args):
        unblock_sites(hosts_path, sites_to_block, redirect_ip)
        os.system("taskkill /F /IM python3.11.exe") 
    
    def on_stop(self):
        unblock_sites(hosts_path, sites_to_block, redirect_ip)
        os.system("taskkill /F /IM python3.11.exe")

def run_streamlit():
    subprocess.run(["streamlit", "run", "app.py"])

def run_get_active_window_title(sites=sites_to_block):
    get_active_window_title(sites)

'''
def close_processes():
    for process in [flask_process, streamlit_process]:
        if process.is_alive():
            process.terminate()
            process.join()  
            if process.is_alive():
                process.kill()  # Wymuś zakończenie, jeśli proces nadal działa
'''
#atexit.register(close_processes)

if __name__ == '__main__':
    multiprocessing.freeze_support()

    MyApp().run()