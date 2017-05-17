from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
import random

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
import random


class MyScreenManager (ScreenManager):
    the_tablet = None

class ScatterTextWidget (BoxLayout):
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
class RobotatorApp(App):  #The name of the class will make it search for learning2.kv
    def build(self):
        #return ScatterTextWidget ()
        self.screen_manager = MyScreenManager()


if __name__ == "__main__":
    RobotatorApp().run()