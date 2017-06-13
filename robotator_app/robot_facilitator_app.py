#!/usr/bin/python
# -*- coding: utf-8 -*-

#from fake_twisted_server import FakeTwistedServer
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
import json
import random
from kivy_communication import *
import sys
import time
import os
import subprocess
from hebrew_management import *

class MyScreenManager (ScreenManager):
    the_app = None



class ScreenRegister (Screen):
    the_app = None
    def __init__(self, the_app):
        self.the_app = the_app
        super(Screen, self).__init__()

    def start_interaction(self):
        print(self.ids)

    def data_received(self, data):
        print ("ScreenRegister: data_received", data)
        self.the_app.screen_manager.current = 'ScreenAudience'
        print("end")
        #self.ids['callback_label'].text = data


class ScreenAudience(Screen):
    the_app = None
    def __init__(self, the_app):
        self.the_app = the_app
        super(Screen, self).__init__()
        audience_text = "ישיא דעי להק"
        #audience_text = str(audience_text[::-1])
      #  print(audience_text, audience_text[::-1])
        self.ids["audience_title"].text = audience_text #HebrewManagement.multiline(, num_char=30, start_to_end=True)


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
        self.basic_server_ip = '192.168.0.10'
        self.server_ip_end = 0

        #return ScatterTextWidget ()
        #self.twisted_server = FakeTwistedServer()
        self.screen_manager = MyScreenManager()
        screen1 = Screen1(self)
        screen2 = Screen2(self)
        screen_audience = ScreenAudience(self)
        screen_register = ScreenRegister(self)
        self.screen_manager.add_widget(screen1)
        self.screen_manager.add_widget(screen2)
        self.screen_manager.add_widget(screen_register)
        self.screen_manager.add_widget(screen_audience)
        self.screen_manager.current = 'ScreenRegister'
        self.screen_manager.current = 'ScreenAudience'
        self.try_connection()
        return self.screen_manager

    def on_connection(self):
        KL.log.insert(action=LogAction.data, obj='RobotatorApp', comment='start')
        print("the client status on_connection ", KC.client.status)


    def register_tablet(self):
        tablet_id = self.screen_manager.current_screen.ids['tablet_id'].text
        subject_id = self.screen_manager.current_screen.ids['subject_id'].text
        message = {'tablet_to_manager': {'action': 'register_tablet', 'parameters': {'subject_id':subject_id,'tablet_id':tablet_id}}}
        message_str = str(json.dumps(message))
        print("register_tablet", message_str)
        KC.client.send_message(message_str)

    def robot_say(self, text):
        print ("robot say", text)
        try:
            nao_message = {'tablet_to_manager': {'action':'say_text_to_speech', 'parameters': [text]}}
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
        self.screen_manager.get_screen('ScreenRegister').ids['callback_label'].text = data
        try:
            json_data = json.loads(data)
            print("data['action']", json_data['action'])
            if (json_data['action']=='registration_complete'):
                self.screen_manager.get_screen('ScreenRegister').data_received(json_data)
                print("registration_complete")
        except:
            print("data_received err", sys.exc_info())
    # ==== communicatoin to twisted server  KC: KivyClient KL: KivyLogger=====
    def try_connection(self):
        server_ip = self.basic_server_ip + str(self.server_ip_end)
        KC.start(the_parents=[self], the_ip=server_ip)  # 127.0.0.1
        KL.start(mode=[DataMode.file, DataMode.communication, DataMode.ros], pathname=self.user_data_dir,
             the_ip=server_ip)

    def failed_connection(self):
        self.server_ip_end += 1
        if self.server_ip_end < 9:
            self.try_connection()

    def success_connection(self):
        self.server_ip_end = 99
       # self.screen_manager.current = 'Screen2'

if __name__ == "__main__":
    RobotatorApp().run()
