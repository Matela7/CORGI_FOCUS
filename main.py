import multiprocessing
import os
import atexit
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
from functools import partial
from flask import Flask, redirect


# TO DO:
# ZROBIC BACKUP 
# bo rozwalimy ludziom systemy jak cos sie ... xD 

sites_to_block = ["facebook.com", "www.facebook.com", "instagram.com", "www.instagram.com", "linkedin.com", "www.linkedin.com", "youtube.com", "www.youtube.com"] 
hosts_path = r"C:\Windows\System32\drivers\etc\hosts"  # Windows
# hosts_path = "/etc/hosts"  # MacOS/Linux
redirect_ip = "127.0.0.1"

# Flask app 
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return redirect("http://localhost:8501")  # Port Streamlit

@flask_app.errorhandler(404)
def page_not_found(error):
    return redirect("http://localhost:8501")  # Przekierowanie na stronę główną Streamlit

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
def unblock_sites(hosts_path, sites_to_block, redirect_ip):
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
# Główna strona
class FirstScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding = 50, spacing = 5)

        text = Label(text="CORGI FOCUS", font_size='30sp', size_hint=(1, 0.2))
        layout.add_widget(text) # główny napis

        horizontal_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.5))

        text2 = Label(text="Stop procastination with CORGI!\nTurn on focus mode to BLOCK addicting websites\nto add websites or delete them, turn second page,\nin case to stop blocking websites, just click again", 
                      font_size='25sp', 
                      size_hint=(0.5, 1), 
                      halign='left', 
                      valign='middle', 
                      )
        text2.bind(size=text2.setter('text_size'))
        horizontal_layout.add_widget(text2) # tekst numer 1

        image = Image(source='korki.gif', size_hint=(0.5, 1))
        horizontal_layout.add_widget(image) # obrazek animowany
        layout.add_widget(horizontal_layout)

        buttons_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.2))
        button_block = Button(text="BLOCK", font_size='20sp', size_hint=(0.3, 0.5))
        button_block.bind(on_press=partial(self.on_block_button_press))
        buttons_layout.add_widget(button_block) # przycisk blokujacy

        spacer1 = Widget(size_hint=(0.1, 1))
        buttons_layout.add_widget(spacer1)

        button_unblock = Button(text="UNBLOCK", font_size='20sp', size_hint=(0.3, 0.5))
        button_unblock.bind(on_press=partial(self.on_unblock_button_press))
        buttons_layout.add_widget(button_unblock) # przycisk odblokowujacy

        spacer2 = Widget(size_hint=(0.1, 1))
        buttons_layout.add_widget(spacer2)

        button_next = Button(text="Next", font_size='20sp', size_hint=(0.3, 0.5))
        button_next.bind(on_press=self.on_next_button_press)
        buttons_layout.add_widget(button_next) # przycisk przechodzacy do drugiej strony
        layout.add_widget(buttons_layout)

        self.add_widget(layout)
        
    def on_block_button_press(self, instance): 
        block_sites(hosts_path, sites_to_block, redirect_ip)

    def on_unblock_button_press(self, instance):
        unblock_sites(hosts_path, sites_to_block, redirect_ip)
        
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
    def build(self):
        screen_manager = ScreenManager()
        screen_manager.add_widget(FirstScreen(name='first'))
        screen_manager.add_widget(SecondScreen(name='second'))
        return screen_manager
    
    def on_request_close(self, *args):
        unblock_sites(hosts_path, sites_to_block, redirect_ip)
        return False
    
    def on_stop(self):
        close_processes()
        unblock_sites(hosts_path, sites_to_block, redirect_ip)
        return False
def run_flask():
    flask_app.run(port=8501, debug=True)
    # debug=False, threaded=True) ?

def run_streamlit():
    os.system("streamlit run app.py")

def close_processes():
    for process in [flask_process, streamlit_process]:
        if process.is_alive():
            process.terminate()
            process.join()
    return False

atexit.register(close_processes)

if __name__ == '__main__':
    flask_process = multiprocessing.Process(target=run_flask)
    streamlit_process = multiprocessing.Process(target=run_streamlit)
    flask_process.start()
    streamlit_process.start()

    try:
        MyApp().run()
    finally:
        # w razie co zamykamy procesy, ale powinny byc zamkniete przez on_stop
        close_processes()


