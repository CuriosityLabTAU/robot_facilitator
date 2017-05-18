from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
import random

from twisted_server import TwistedServer
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
import json
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
import random
import time

class MyScreenManager (ScreenManager):
    the_app = None


class Screen1 (Screen):
    the_app = None

    def __init__(self, the_app):
        self.the_app = the_app
        super(Screen, self).__init__()

    def change_label_color(self, *args):
        color = [random.random() for i in xrange(3)]+[1]
        print(color)
        label = self.ids['my_label']
        label1 = self.ids['label1']
        label2 = self.ids['label2']
        label.color = color
        label1.color = color
        label2.color = color
        print(label1.color)

    def on_checkbox_active(self, checkbox, value):
        if value:
            print('The checkbox', checkbox, 'is active')
        else:
            print('The checkbox', checkbox, 'is inactive')

class Screen2 (Screen):
    the_app = None

    def __init__(self, the_app):
        self.the_app = the_app
        super(Screen, self).__init__()


class RobotatorApp(App):  #The name of the class will make it search for learning2.kv
    def build(self):
        #return ScatterTextWidget ()
        self.twisted_server = TwistedServer()
        self.screen_manager = MyScreenManager()
        screen1 = Screen1(self)
        screen2 = Screen2(self)
        self.screen_manager.add_widget(screen1)
        self.screen_manager.add_widget(screen2)
        self.screen_manager.current = 'Screen2'
        return self.screen_manager

    def robot_say(self, text):
        nao_message = {'action':'say_text_to_speech', 'parameters': [text]}
        nao_message_str = str(json.dumps(nao_message))
        self.twisted_server.send_message(nao_message_str)

    def change_screen(self, screen_name):
        print(screen_name)
        self.screen_manager.current = screen_name


if __name__ == "__main__":
    RobotatorApp().run()
