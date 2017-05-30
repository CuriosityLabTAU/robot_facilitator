#from fake_twisted_server import FakeTwistedServer
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
import json
import random
from kivy_communication import *
import sys


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
        self.the_app = self
        #return ScatterTextWidget ()
        #self.twisted_server = FakeTwistedServer()
        self.screen_manager = MyScreenManager()
        screen1 = Screen1(self)
        screen2 = Screen2(self)
        self.screen_manager.add_widget(screen1)
        self.screen_manager.add_widget(screen2)
        self.screen_manager.current = 'Screen2'
        self.init_communication()

        return self.screen_manager

    def init_communication(self):
        local_ip = '192.168.1.254'
        server_ip = '192.168.0.105'
        try:
            KC.start(the_parents=[self, self.the_app], the_ip=server_ip)  # 127.0.0.1
            KL.start(mode=[DataMode.file, DataMode.communication, DataMode.ros], pathname=self.user_data_dir, the_ip=server_ip)
        except:
            print ("unexpected error:", sys.exc_info())

    def on_connection(self):
        KL.log.insert(action=LogAction.data, obj='RobotatorApp', comment='start')

    def robot_say(self, text):
        print ("robot say", text)
        try:
            nao_message = {'nao': {'action':'say_text_to_speech', 'parameters': [text]}}
            nao_message_str = str(json.dumps(nao_message))
            print("json.loads=", json.loads(nao_message_str))
            #self.twisted_server.send_message(nao_message_str)
            KC.client.send_message(nao_message_str)
            print("robot say: end of try")
        except:
            print ("unexpected error:", sys.exc_info())

    def change_screen(self, screen_name):
        print(screen_name)
        self.screen_manager.current = screen_name

    def data_received(self, data):
        print ("robotator_app: data_received", data)
        self.screen_manager.get_screen('Screen2').ids['callabck_label'].text = data
if __name__ == "__main__":
    RobotatorApp().run()
