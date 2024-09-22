from kivy.config import Config
Config.set('graphics', 'width', '1920')
Config.set('graphics', 'height', '1080')
Config.set('graphics', 'resizable', True)  # Nie pozwala na zmianę rozmiaru

# Włącz tryb pełnoekranowy
Config.set('graphics', 'fullscreen', 'auto')  # Umożliwia automatyczne dopasowanie

# Możesz ustawić maksymalne rozmiary
Config.set('graphics', 'max_width', '1920')
Config.set('graphics', 'max_height', '1080')
import threading
import os
import atexit
import subprocess
import time
import base64
import sys
import time
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle
from kivy.graphics import Color, Ellipse
from kivy.core.audio import SoundLoader
from functools import partial
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.widget import MDWidget
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDFlatButton
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineAvatarIconListItem, IconRightWidget
from kivymd.uix.button import MDIconButton
from kivy.utils import get_color_from_hex
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.utils import get_color_from_hex
from kivy.core.audio import SoundLoader
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.gridlayout import MDGridLayout
from kivy.core.window import Window
from kivy.uix.video import Video

import win32gui

# TO DO:
# ZROBIC BACKUP 
# bo rozwalimy ludziom systemy jak cos sie ... xD 

sites_to_block = ["facebook.com", "instagram.com", "linkedin.com", "youtube.com", "pornhub.com", "tiktok.com"]

hosts_path = r"C:\Windows\System32\drivers\etc\hosts"  # Windows
# hosts_path = "/etc/hosts"  # MacOS/Linux
redirect_ip = "127.0.0.1"

def resource_path(relative_path):
    """Zwraca ścieżkę do zasobu dla pliku .exe"""
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def get_active_window_title(sites):
    while window_title_iterator.active_window_iterator == True:
        window = win32gui.GetForegroundWindow()
        active_window = win32gui.GetWindowText(window)
        active_window = active_window.lower()

        for site in sites:
            if strip_site(site) in active_window:
                os.system("start https://matela7.github.io/")
            time.sleep(0.1)

def strip_site(site):
    return site.replace("http://", "").replace("https://", "").replace("www.", "").replace(".com", "").split("/")[0].lower()

def error_popup(number):
    if number == 0:
        dialog = MDDialog(
            title='ERROR CORGI IS ANGRY',
            text='You have to run this program as an administrator to block websites!',
            size_hint=(None, None), size=(400, 400))
        dialog.open()
    elif number == 1:
        dialog = MDDialog(
            title='ERROR CORGI IS ANGRY',
            text='You have to run this program as an administrator to unblock websites!',
            size_hint=(None, None), size=(400, 400))
        dialog.open()
    else:
        dialog = MDDialog(
            title='ERROR CORGI IS ANGRY',
            text='Something went wrong!',
            size_hint=(None, None), size=(400, 400))
        dialog.open()

def block_sites(hosts_path, sites_to_block, redirect_ip):
    if main_iterator.main_iterator == False:
        try:
            with open(hosts_path, 'r+') as file:
                hosts = file.read()
                for site in sites_to_block:
                    if site not in hosts:
                        file.write(redirect_ip + " " + site + "\n")
        except PermissionError:
            error_popup(0)
    else:
        window_title_iterator.active_window_iterator = True
        global get_active_window_title_thread
        get_active_window_title_thread = threading.Thread(target=run_get_active_window_title, args=(sites_to_block,), daemon=True)
        get_active_window_title_thread.start()

def unblock_sites(hosts_path, sites_to_block, redirect_ip):
    if main_iterator.main_iterator == True:
        try:
            if get_active_window_title_thread.is_alive():
                window_title_iterator.active_window_iterator = False
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
        except PermissionError:
            error_popup(1)


def run_get_active_window_title(sites=sites_to_block):
    get_active_window_title(sites)

def stop_get_active_window_title():
    if get_active_window_title_thread.is_alive():
        get_active_window_title_thread.join()  

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
    
class WindowTitleIterator:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(WindowTitleIterator, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self._active_window_iterator = True
    
    @property
    def active_window_iterator(self):
        return self._active_window_iterator
    
    @active_window_iterator.setter
    def active_window_iterator(self, value):
        self._active_window_iterator = value

class PomodoroIterator:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(PomodoroIterator, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self._pomodoro_iterator = True
    
    @property
    def pomodoro_iterator(self):
        return self._pomodoro_iterator
    
    @pomodoro_iterator.setter
    def pomodoro_iterator(self, value):
        self._pomodoro_iterator = value


class FirstScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


        self.bg_video = Video(source=resource_path('video.mp4'), state='play', options={'eos': 'loop'})
        self.bg_video.volume = 0.0
        self.add_widget(self.bg_video)

        self.blocked = False  # Flaga do sprawdzania, czy strony są zablokowane
        layout = MDBoxLayout(orientation='vertical', padding=50, spacing=5)

        text = MDLabel(text="Corgi Focus", font_style='H3', halign="center", size_hint=(1, 0.2), theme_text_color="Custom", text_color=(1, 1, 1, 1))
        layout.add_widget(text)  # Główny napis

        image = Image(source=resource_path('korki.gif'), size_hint=(0.75, 1), pos_hint={'center_x': 0.5})
        layout.add_widget(image)

        buttons_layout = MDBoxLayout(orientation='horizontal', size_hint=(1, 0.2))
        
        # Przyciski
        self.button_block = MDRaisedButton(text="BLOCK", font_size='15sp', size_hint=(0.15, 0.25), md_bg_color=(get_color_from_hex("#2D2D2D")))
        self.button_block.bind(on_press=self.on_block_button_press)
        buttons_layout.add_widget(self.button_block)

        button_change = MDRaisedButton(
            text="Block mode" if not main_iterator.main_iterator else "Popup mode",
            font_size='15sp', size_hint=(0.15, 0.25), md_bg_color=(get_color_from_hex("#2D2D2D"))
        )
        button_change.bind(on_press=self.on_change_button_press)
        buttons_layout.add_widget(button_change)

        button_next = MDRaisedButton(text="Next", font_size='15sp', size_hint=(0.15, 0.25), md_bg_color=(get_color_from_hex("#2D2D2D")))
        button_next.bind(on_press=self.on_next_button_press)
        buttons_layout.add_widget(button_next)
        
        layout.add_widget(buttons_layout)
        self.add_widget(layout)

    def on_block_button_press(self, instance):
        if not self.blocked:
            block_sites(hosts_path, sites_to_block, redirect_ip)
            self.blocked = True
            self.button_block.text = "UNBLOCK"  # Zmieniamy tekst przycisku na UNBLOCK
        else:
            unblock_sites(hosts_path, sites_to_block, redirect_ip)
            self.blocked = False
            self.button_block.text = "BLOCK"  # Zmieniamy tekst przycisku z powrotem na BLOCK

    def on_change_button_press(self, instance):
        if main_iterator.main_iterator:
            main_iterator.main_iterator = False
            instance.text = "Block mode"
        else:
            main_iterator.main_iterator = True
            instance.text = "Popup mode"

    def on_next_button_press(self, instance):
        self.manager.transition = SlideTransition(direction="up", duration=0.5)
        self.manager.current = 'second'

class SecondScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bg_video = Video(source=resource_path('video3.mp4'), state='play', options={'eos': 'loop'})
        self.bg_video.volume = 0.0
        self.add_widget(self.bg_video)
        self.layout = MDBoxLayout(orientation='vertical')

        self.text = MDLabel(
            text="Corgi Focus", 
            font_style='H5', 
            halign="center", 
            size_hint=(1, 0.1), 
            theme_text_color="Custom", 
            text_color=(1, 1, 1, 1)
        )
        self.layout.add_widget(self.text)

        # Zwiększenie size_hint dla listy, aby była większa
        self.scrollview = MDScrollView(size_hint=(1, 0.65))  # Zwiększenie wysokości listy
        self.list_view = MDList()

        # Wyświetlanie istniejących stron
        for site in sites_to_block:
            self.add_site_to_list(site)

        self.scrollview.add_widget(self.list_view)
        self.layout.add_widget(self.scrollview)

        # Pole tekstowe do dodawania nowych stron
        self.text_field = MDTextField(
            hint_text="Enter a website to block",
            size_hint=(1, 0.1),
            multiline=False
        )
        self.layout.add_widget(self.text_field)

        # Zmniejszenie rozmiaru GIF-a
        image = Image(
            source=resource_path('korki4.gif'), 
            size_hint=(0.5, 0.2),  # Zmniejszenie size_hint
            pos_hint={'center_x': 0.5}
            
        )
        self.layout.add_widget(image)

        button_layout = MDGridLayout(
            cols=2, 
            spacing=70, 
            size_hint=(None, 0.15),  # Zmniejszenie wysokości button_layout
            pos_hint={'center_x': 0.5}
        )
        button_layout.bind(minimum_width=button_layout.setter('width'))

        # Przycisk do dodawania stron
        self.add_button = MDRaisedButton(
            text="Add Website",
            size_hint=(None, None),  # Brak automatycznego rozciągania
            size=(200, 50),  # Ustawienie stałego rozmiaru
            md_bg_color=(get_color_from_hex("#2D2D2D"))
        )
        self.add_button.bind(on_press=self.on_add_button_press)
        button_layout.add_widget(self.add_button)

        # Przycisk powrotu do poprzedniego ekranu
        self.button_prev = MDRaisedButton(
            text="Next", 
            size_hint=(None, None),  # Brak automatycznego rozciągania
            size=(200, 50),  # Ustawienie stałego rozmiaru
            md_bg_color=(get_color_from_hex("#2D2D2D"))
        )
        self.button_prev.bind(on_press=self.on_prev_button_press)
        button_layout.add_widget(self.button_prev)

        # Dodanie layoutu z przyciskami do głównego layoutu
        self.layout.add_widget(button_layout)
        self.add_widget(self.layout)

    def add_site_to_list(self, site):
        """Funkcja dodająca stronę do listy z możliwością usunięcia."""
        list_item = OneLineAvatarIconListItem(text=site, theme_text_color="Custom", text_color=(1, 1, 1, 1))

        # Dodaj ikonę kosza jako przycisk
        icon = IconRightWidget(icon="trash-can")
        icon.theme_text_color = "Custom"  # Pozwala na zastosowanie własnego koloru
        icon.text_color = get_color_from_hex("#6D214F")  # Zmiana koloru ikony na biały
        icon.bind(on_press=lambda x, site=site: self.remove_site(site, list_item))
        list_item.add_widget(icon)

        self.list_view.add_widget(list_item)

    def remove_site(self, site, list_item):
        """Funkcja usuwająca stronę z listy."""
        if site in sites_to_block:
            sites_to_block.remove(site)
            self.list_view.remove_widget(list_item)

    def on_add_button_press(self, instance):
        # Pobieranie tekstu z pola tekstowego
        new_site = self.text_field.text.strip()

        if new_site and new_site not in sites_to_block:
            # Dodajemy stronę do listy blokowanych
            sites_to_block.append(new_site)
            self.add_site_to_list(new_site)

            # Czyścimy pole tekstowe po dodaniu strony
            self.text_field.text = ""
        else:
            # Wyświetlamy błąd, jeśli pole tekstowe jest puste lub strona już istnieje
            error_dialog = MDDialog(
                title="Error",
                text="This site is already in the list or the field is empty.",
                buttons=[MDFlatButton(text="OK", on_release=lambda x: error_dialog.dismiss())]
            )
            error_dialog.open()

    def on_prev_button_press(self, instance):
        self.manager.current = 'third'

class ThirdScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


        self.bg_video = Video(source=resource_path('video2.mp4'), state='play', options={'eos': 'loop'})
        self.bg_video.volume = 0.0
        self.add_widget(self.bg_video)

        # Główny layout
        layout = MDBoxLayout(orientation='vertical', padding=50, spacing=5)
        
        # Nagłówek
        self.text = MDLabel(text="Pomodoro with Corgi", font_style='H5', halign="center", size_hint=(1, 0.1), theme_text_color="Custom", text_color=(1, 1, 1, 1))
        layout.add_widget(self.text)
        
        # Obrazek
        image = Image(source='korki2.gif', size_hint=(0.75, 1), pos_hint={'center_x': 0.5})
        layout.add_widget(image)

        # Layout dla timera i przycisków
        timer_layout = MDBoxLayout(orientation='vertical', spacing=20, size_hint=(1, 0.4))

        # Timer label (wyświetlanie czasu)
        self.timer_label = MDLabel(text="25:00", font_style='H3', halign="center", theme_text_color="Custom", text_color=(1, 1, 1, 1))
        timer_layout.add_widget(self.timer_label)
        # Layout na przyciski (start, pause, reset, next)
        button_layout = MDGridLayout(cols=4, spacing=20, size_hint=(None, 0.2), pos_hint={'center_x': 0.5})
        button_layout.bind(minimum_width=button_layout.setter('width'))  # Dostosowanie szerokości do liczby przycisków

                # Przycisk Start
        self.start_button = MDRaisedButton(text="Start", on_release=self.start_timer, md_bg_color=(get_color_from_hex("#2D2D2D")))
        button_layout.add_widget(self.start_button)
        
        # Przycisk Pause
        self.pause_button = MDRaisedButton(text="Pause", on_release=self.pause_timer, md_bg_color=(get_color_from_hex("#2D2D2D")))
        button_layout.add_widget(self.pause_button)
        
        # Przycisk Reset
        self.reset_button = MDRaisedButton(text="Reset/Break", on_release=self.reset_timer, md_bg_color=(get_color_from_hex("#2D2D2D")))
        button_layout.add_widget(self.reset_button)

        # Przycisk Next
        self.next_button = MDRaisedButton(text="Next", on_release=self.on_next_button_press, md_bg_color=(get_color_from_hex("#2D2D2D")))
        button_layout.add_widget(self.next_button)

        # Dodanie przycisków do layoutu
        timer_layout.add_widget(button_layout)
        
        # Dodanie layoutu timera do głównego layoutu
        layout.add_widget(timer_layout)

        # Dodanie layoutu do ekranu
        self.add_widget(layout)

        # Inicjalizacja zmiennych timerowych
        self.is_timer_running = False
        self.timer_seconds = 60 * 25 # 25 minut w sekundach
        pomodoro_iterator.pomodoro_iterator = True
        self.timer_event = None

    # Funkcja do aktualizowania timera
    def update_timer(self, dt):
        if self.timer_seconds > 0:
            self.timer_seconds -= 1
            minutes, seconds = divmod(self.timer_seconds, 60)
            self.timer_label.text = f"{minutes:02}:{seconds:02}"
        else:
            self.stop_timer()
            self.play_sound('ringtone.mp3')
            self.timer_label.text = "Time for coffe break!"
            # Możesz dodać dźwięk lub inne powiadomienie tutaj
            time.sleep(5)
            if pomodoro_iterator.pomodoro_iterator == True:
                self.timer_label.text = "5:00"
                self.timer_seconds = 5 * 60
                pomodoro_iterator.pomodoro_iterator = False
            else:
                self.timer_label.text = "25:00"
                self.timer_seconds = 25 * 60
                pomodoro_iterator.pomodoro_iterator = True

    # Funkcja startująca timer
    def start_timer(self, instance):
        if not self.is_timer_running:
            self.play_sound('click.mp3')
            self.timer_event = Clock.schedule_interval(self.update_timer, 1)
            self.is_timer_running = True

    # Funkcja zatrzymująca timer
    def pause_timer(self, instance):
        if self.is_timer_running:
            Clock.unschedule(self.timer_event)
            self.is_timer_running = False

    # Funkcja resetująca timer
    def reset_timer(self, instance):
        if self.is_timer_running:
            Clock.unschedule(self.timer_event)
        self.timer_seconds = 25 * 60  # Reset do 25 minut
        if self.timer_label.text == "25:00":
            self.timer_label.text = "5:00"
            self.timer_seconds = 5 * 60
            pomodoro_iterator.pomodoro_iterator = False
        elif self.timer_label.text == "5:00":
            self.timer_label.text = "25:00"
            pomodoro_iterator.pomodoro_iterator = True
        else:   
            self.timer_label.text = "25:00"
            pomodoro_iterator.pomodoro_iterator = True
        self.is_timer_running = False

    # Funkcja zatrzymująca timer po zakończeniu
    def stop_timer(self):
        if self.is_timer_running:
            Clock.unschedule(self.timer_event)
        self.is_timer_running = False


    def on_next_button_press(self, instance):
        self.manager.transition = SlideTransition(direction="down", duration=0.5)
        self.manager.current = 'first'

    def play_sound(self, sound):
        sound = SoundLoader.load(resource_path(sound))
        if sound:
            sound.play()

class MyApp(MDApp):
    icon = "icon.png"  # or icon.ico
    title = "CORGI FOCUS"

    def build(self):
        self.play_sound_on_startup()
        global main_iterator
        global window_title_iterator
        global pomodoro_iterator
        main_iterator = MainIterator()  # Singleton instancja klasy MainIterator
        window_title_iterator = WindowTitleIterator() # Singleton instancja klasy WindowTitleIterator
        pomodoro_iterator = PomodoroIterator()  # Singleton instancja klasy PomodoroIterator
        screen_manager = ScreenManager()
        screen_manager.add_widget(FirstScreen(name='first'))
        screen_manager.add_widget(SecondScreen(name='second'))
        screen_manager.add_widget(ThirdScreen(name='third'))
        return screen_manager

    def play_sound_on_startup(self):
        sound = SoundLoader.load(resource_path('corgi_bark.mp3'))
        if sound:
            sound.play()

    def on_stop(self):
        unblock_sites(hosts_path, sites_to_block, redirect_ip)

if __name__ == "__main__":
    MyApp().run()

