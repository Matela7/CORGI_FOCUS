from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from functools import partial  # Importujemy funkcję partial z modułu functools

sites_to_block = ["facebook.com", "www.facebook.com", "instagram.com", "www.instagram.com"]
hosts_path = r"C:\Windows\System32\drivers\etc\hosts"  # Windows
# hosts_path = "/etc/hosts"  # MacOS/Linux
redirect_ip = "127.0.0.1"

def block_sites(hosts_path, sites_to_block, redirect_ip):
    with open(hosts_path, 'r+') as file:
        hosts = file.read()
        for site in sites_to_block:
            if site not in hosts:
                file.write(redirect_ip + " " + site + "\n")
    print("Strony zablokowane.")

def unblock_sites(hosts_path, sites_to_block, redirect_ip):
    with open(hosts_path, 'r+') as file:
        lines = file.readlines()
        file.seek(0)
        for line in lines:
            if not any(site in line for site in sites_to_block):
                file.write(line)
        file.truncate()
    print("Strony odblokowane.")

class FirstScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        text = Label(text="CORGI FOCUS", font_size='30sp', size_hint=(1, 0.3))
        layout.add_widget(text)

        text2 = Label(text="Stop procastination with CORGI!\nTurn on focus mode to BLOCK addicting websites\nto add websites or delete them, turn second page,\nin case to stop blocking websites, just click again", font_size='20sp', size_hint=(1, 0.3))
        layout.add_widget(text2)

        image = Image(source='korki.gif', size_hint=(1, 0.4))
        layout.add_widget(image)

        button_block = Button(text="BLOCK", font_size='20sp', size_hint=(1, 0.1))
        button_block.bind(on_press=partial(self.on_block_button_press))
        layout.add_widget(button_block)

        button_unblock = Button(text="UNBLOCK", font_size='20sp', size_hint=(1, 0.1))
        button_unblock.bind(on_press=partial(self.on_unblock_button_press))
        layout.add_widget(button_unblock)

        self.add_widget(layout)
        
    def on_block_button_press(self, instance):
        block_sites(hosts_path, sites_to_block, redirect_ip)

    def on_unblock_button_press(self, instance):
        unblock_sites(hosts_path, sites_to_block, redirect_ip)

class MyApp(App):
    def build(self):
        screen_manager = ScreenManager()
        screen_manager.add_widget(FirstScreen(name='first'))
        return screen_manager

if __name__ == '__main__':
    MyApp().run()
