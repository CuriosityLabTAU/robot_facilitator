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
from kivy.clock import *
from kivy.uix.label import Label


class TimerLabel(Label):
    time = -1
    def start_timer(self, duration=5):
        self.stop_timer()
        print("start_timer?")
        if (self.time>-1): # in case the timer was already on, unschedule it
            Clock.unschedule(self.event)

        self.time = duration
        self.event = Clock.schedule_interval(self.advance, 1)
        min,sec = divmod(duration, 60)
        str_time = "%d:%02d" % (min, sec)
        self.text = str_time

    def stop_timer(self):
        try:
            Clock.unschedule(self.event)
            self.time = -1
            self.text = ""
        except:
            print ("stop timer failed")

    def advance(self, dt):
        min, sec = divmod(self.time, 60)
        str_time = "%d:%02d" % (min, sec)
        print("self.time", self.time, str_time)
        self.text = str_time
        if self.time <= 0:
            Clock.unschedule(self.event)
            self.text = 'רמגנ'
        else:
            self.time -= 1


class MyScreenManager (ScreenManager):
    the_app = None


class ScreenRegister (Screen):
    the_app = None

    def __init__(self, the_app):
        self.the_app = the_app
        super(Screen, self).__init__()

        self.ids["tablet_id"].bind(text=self.ids["tablet_id"].on_text_change)
        self.ids["subject_id"].bind(text=self.ids["subject_id"].on_text_change)

    def start_interaction(self):
        print(self.ids)

    def data_received(self, data):
        print ("ScreenRegister: data_received", data)
        # self.the_app.screen_manager.current = 'ScreenAudience'
        print("end")
        #self.ids['callback_label'].text = data


class ScreenHello (Screen):
    the_app = None

    def __init__(self, the_app):
        self.the_app = the_app
        super(Screen, self).__init__()


class ScreenAudience(Screen):
    the_app = None

    def __init__(self, the_app):
        self.the_app = the_app
        super(Screen, self).__init__()
        audience_text = "(תישיא הדובע) דעי להק"
        #audience_text = str(audience_text[::-1])
      #  print(audience_text, audience_text[::-1])
        self.ids["audience_title"].text = audience_text #HebrewManagement.multiline(, num_char=30, start_to_end=True)

        self.ids["audience_list_1"].bind(text=HebrewManagement.text_change)
        self.ids["audience_list_2"].bind(text=HebrewManagement.text_change)
        self.ids["audience_list_3"].bind(text=HebrewManagement.text_change)
        self.ids["audience_list_4"].bind(text=HebrewManagement.text_change)
        self.ids["audience_list_5"].bind(text=HebrewManagement.text_change)

        self.ids["audience_list_1"].bind(text=self.ids["audience_list_1"].on_text_change)
        self.ids["audience_list_2"].bind(text=self.ids["audience_list_2"].on_text_change)
        self.ids["audience_list_3"].bind(text=self.ids["audience_list_3"].on_text_change)
        self.ids["audience_list_4"].bind(text=self.ids["audience_list_4"].on_text_change)
        self.ids["audience_list_5"].bind(text=self.ids["audience_list_5"].on_text_change)

        self.ids["audience_list_1"].focus=True
        # self.ids['timer_time'].start_timer()




class ScreenAudienceGroup(Screen):
    the_app = None

    def __init__(self, the_app):
        self.the_app = the_app
        super(Screen, self).__init__()

        self.ids["audience_group_title"].text = "(תיתצובק הדובע) דעי להק" #HebrewManagement.multiline(, num_char=30, start_to_end=True)
        self.ids["audience_list_group_1"].bind(text=HebrewManagement.text_change)
        self.ids["audience_list_group_2"].bind(text=HebrewManagement.text_change)
        self.ids["audience_list_group_3"].bind(text=HebrewManagement.text_change)
        self.ids["audience_list_group_4"].bind(text=HebrewManagement.text_change)
        self.ids["audience_list_group_5"].bind(text=HebrewManagement.text_change)

        self.ids["audience_list_group_1"].bind(text=self.ids["audience_list_group_1"].on_text_change)
        self.ids["audience_list_group_2"].bind(text=self.ids["audience_list_group_2"].on_text_change)
        self.ids["audience_list_group_3"].bind(text=self.ids["audience_list_group_3"].on_text_change)
        self.ids["audience_list_group_4"].bind(text=self.ids["audience_list_group_4"].on_text_change)
        self.ids["audience_list_group_5"].bind(text=self.ids["audience_list_group_5"].on_text_change)

        self.ids["audience_list_group_1"].focus=True


class ScreenAudienceAgreeLeader(Screen):
    the_app = None

    def __init__(self, the_app):
        self.the_app = the_app
        super(Screen, self).__init__()
        audience_text = "?תאזה המישרה םע ה/םיכסמ ה/תא םאה"
        self.ids["audience_title"].text = audience_text
        #self.ids["audience_list_group_1"].bind(text=self.the_app.screen_manager.get_screen('ScreenAudienceGroup').ids['audience_list_group_1'].text)
        #self.ids["audience_list_group_1"].bind(text=self.screen_manager.get_screen('ScreenRegister').ids['subject_id'].text

        self.ids["audience_list_group_1"].bind(text=HebrewManagement.text_change)
        self.ids["audience_list_group_2"].bind(text=HebrewManagement.text_change)
        self.ids["audience_list_group_3"].bind(text=HebrewManagement.text_change)
        self.ids["audience_list_group_4"].bind(text=HebrewManagement.text_change)
        self.ids["audience_list_group_5"].bind(text=HebrewManagement.text_change)

    def on_enter(self, *args):
        self.ids["audience_list_group_1"].text = self.the_app.screen_manager.get_screen('ScreenAudienceGroup').ids['audience_list_group_1'].text
        self.ids["audience_list_group_2"].text = self.the_app.screen_manager.get_screen('ScreenAudienceGroup').ids['audience_list_group_2'].text
        self.ids["audience_list_group_3"].text = self.the_app.screen_manager.get_screen('ScreenAudienceGroup').ids['audience_list_group_3'].text
        self.ids["audience_list_group_4"].text = self.the_app.screen_manager.get_screen('ScreenAudienceGroup').ids['audience_list_group_4'].text
        self.ids["audience_list_group_5"].text = self.the_app.screen_manager.get_screen('ScreenAudienceGroup').ids['audience_list_group_5'].text

class ScreenAudienceAgree(Screen):
    the_app = None

    def __init__(self, the_app):
        self.the_app = the_app
        super(Screen, self).__init__()
        audience_text = "?תאזה המישרה םע ה/םיכסמ ה/תא םאה"
        self.ids["audience_title"].text = audience_text


class ScreenAudienceQuestions(Screen):
    the_app = None

    def __init__(self, the_app):
        self.the_app = the_app
        super(Screen, self).__init__()
        audience_text = "(תישיא הדובע) םישמתשמ רקחמ"
        #audience_text = str(audience_text[::-1])
      #  print(audience_text, audience_text[::-1])
        self.ids["audience_questions_title"].text = audience_text #HebrewManagement.multiline(, num_char=30, start_to_end=True)

        self.ids["audience_questions_list_1"].bind(text=HebrewManagement.text_change)
        self.ids["audience_questions_list_2"].bind(text=HebrewManagement.text_change)
        self.ids["audience_questions_list_3"].bind(text=HebrewManagement.text_change)

        self.ids["audience_questions_list_1"].bind(text=self.ids["audience_questions_list_1"].on_text_change)
        self.ids["audience_questions_list_2"].bind(text=self.ids["audience_questions_list_2"].on_text_change)
        self.ids["audience_questions_list_3"].bind(text=self.ids["audience_questions_list_3"].on_text_change)

        self.ids["audience_questions_list_1"].focus=True


class ScreenAudienceQuestionsGroup(Screen):
    the_app = None
    def __init__(self, the_app):
        self.the_app = the_app
        super(Screen, self).__init__()
        audience_group_title = "(תיתצובק הדובע) םישמתשמ רקחמ"
        #audience_text = str(audience_text[::-1])
      #  print(audience_text, audience_text[::-1])
        self.ids["audience_questions_group_title"].text = audience_group_title #HebrewManagement.multiline(, num_char=30, start_to_end=True)

        self.ids["audience_questions_group_list_1"].bind(text=HebrewManagement.text_change)
        self.ids["audience_questions_group_list_2"].bind(text=HebrewManagement.text_change)
        self.ids["audience_questions_group_list_3"].bind(text=HebrewManagement.text_change)
        self.ids["audience_questions_group_list_4"].bind(text=HebrewManagement.text_change)
        self.ids["audience_questions_group_list_5"].bind(text=HebrewManagement.text_change)


        self.ids["audience_questions_group_list_1"].bind(text=self.ids["audience_questions_group_list_1"].on_text_change)
        self.ids["audience_questions_group_list_2"].bind(text=self.ids["audience_questions_group_list_2"].on_text_change)
        self.ids["audience_questions_group_list_3"].bind(text=self.ids["audience_questions_group_list_3"].on_text_change)
        self.ids["audience_questions_group_list_4"].bind(text=self.ids["audience_questions_group_list_4"].on_text_change)
        self.ids["audience_questions_group_list_5"].bind(text=self.ids["audience_questions_group_list_5"].on_text_change)

        self.ids["audience_questions_group_list_1"].focus=True


class ScreenStartSimulation(Screen):
    the_app = None
    roles = {
        'proctor': 'ןייסנ',
        'subject': 'קדבנ'
    }
    bias = {
        'proctor': ('תומידקה תייטה','רושיאה תייטה','תרוקיב לבקל ישוקה לש הייטה'),
        'subject': ('הרק תמאב המ חוכשל הייטה','הייצרה תייטה')
    }


    def __init__(self, the_app):
        self.the_app = the_app
        super(Screen, self).__init__()
        self.role_title = "תויהל תרחבנ"
        self.ids['start_simulation_role'].text = self.role_title
        self.bias_title = "ךלש הייטהה"
        self.ids['start_simulation_bias'].text = self.bias_title

    def update_role_bias(self, role, bias):
        self.role_title += ' '  + self.roles[role]
        self.ids['start_simulation_role'].text = self.role_title
        self.bias_title += ' ' + self.bias[role][bias]
        self.ids['start_simulation_bias'].text = self.bias_title


class ScreenSimulation(Screen):
    the_app = None
    def __init__(self, the_app):
        self.the_app = the_app
        super(Screen, self).__init__()
        title = "םירחאה לש תויטהה ויה המ"
        #audience_text = str(audience_text[::-1])
      #  print(audience_text, audience_text[::-1])
        self.ids['simulation_title'].text = title #HebrewManagement.multiline(, num_char=30, start_to_end=True)

        self.ids['simulation_spinner_1'].option_cls = MySpinnerOption
        self.ids['simulation_spinner_2'].option_cls = MySpinnerOption
        self.ids['simulation_spinner_3'].option_cls = MySpinnerOption
        self.ids['simulation_spinner_4'].option_cls = MySpinnerOption
        self.ids['simulation_spinner_5'].option_cls = MySpinnerOption


        self.ids["simulation_spinner_1"].bind(text=self.ids["simulation_spinner_1"].on_text_change)
        self.ids["simulation_spinner_2"].bind(text=self.ids["simulation_spinner_2"].on_text_change)
        self.ids["simulation_spinner_3"].bind(text=self.ids["simulation_spinner_3"].on_text_change)
        self.ids["simulation_spinner_4"].bind(text=self.ids["simulation_spinner_4"].on_text_change)
        self.ids["simulation_spinner_5"].bind(text=self.ids["simulation_spinner_5"].on_text_change)


class ScreenBye (Screen):
    the_app = None

    def __init__(self, the_app):
        self.the_app = the_app
        super(Screen, self).__init__()


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
        # self.basic_server_ip = '127.0.0.1'
        self.server_ip_end = 0

        #return ScatterTextWidget ()
        #self.twisted_server = FakeTwistedServer()
        self.screen_manager = MyScreenManager()
        screen1 = Screen1(self)
        screen2 = Screen2(self)

        screen_register = ScreenRegister(self)
        screen_hello = ScreenHello(self)
        screen_audience = ScreenAudience(self)
        screen_audience_group = ScreenAudienceGroup(self)
        screen_audience_questions = ScreenAudienceQuestions(self)
        screen_audience_questions_group = ScreenAudienceQuestionsGroup(self)
        screen_audience_agree = ScreenAudienceAgree(self)
        screen_audience_agree_leader = ScreenAudienceAgreeLeader(self)
        screen_start_simulation = ScreenStartSimulation(self)
        screen_simulation = ScreenSimulation(self)
        screen_bye = ScreenBye(self)

        self.screen_manager.add_widget(screen1)
        self.screen_manager.add_widget(screen2)
        self.screen_manager.add_widget(screen_register)
        self.screen_manager.add_widget(screen_hello)
        self.screen_manager.add_widget(screen_audience)
        self.screen_manager.add_widget(screen_audience_group)
        self.screen_manager.add_widget(screen_audience_agree)
        self.screen_manager.add_widget(screen_audience_agree_leader)
        self.screen_manager.add_widget(screen_audience_questions)
        self.screen_manager.add_widget(screen_audience_questions_group)
        self.screen_manager.add_widget(screen_start_simulation)
        self.screen_manager.add_widget(screen_simulation)
        self.screen_manager.add_widget(screen_bye)

        self.screen_manager.current = 'ScreenRegister'
        # self.screen_manager.current = 'ScreenHello'
        # self.screen_manager.current = 'ScreenAudience'
        # self.screen_manager.current = 'ScreenAudienceGroup'
        # self.screen_manager.current = 'ScreenAudienceAgree'
        # self.screen_manager.current = 'ScreenAudienceQuestions'
        # self.screen_manager.current = 'ScreenAudienceQuestionsGroup'
        # self.screen_manager.current = 'ScreenStartSimulation'
        # self.screen_manager.current = 'ScreenSimulation'
        # self.screen_manager.current = 'ScreenBye'

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

    def audience_done(self):
        print("audience_done")
        self.screen_manager.current_screen.ids['timer_time'].stop_timer()
        tablet_id = self.screen_manager.get_screen('ScreenRegister').ids['tablet_id'].text
        subject_id = self.screen_manager.get_screen('ScreenRegister').ids['subject_id'].text
        print("audience_done", tablet_id, subject_id)
        message = {'tablet_to_manager': {'action': 'audience_done', 'parameters': {'subject_id':subject_id, 'tablet_id':tablet_id}}}
        message_str = str(json.dumps(message))
        print("audience_done", message_str)
        KC.client.send_message(message_str)

    def audience_group_done(self):
        print("audience_done")
        self.screen_manager.current_screen.ids['timer_time'].stop_timer()
        tablet_id = self.screen_manager.get_screen('ScreenRegister').ids['tablet_id'].text
        subject_id = self.screen_manager.get_screen('ScreenRegister').ids['subject_id'].text
        print("audience_done", tablet_id, subject_id)
        message = {'tablet_to_manager': {'action': 'audience_group_done', 'parameters': {'subject_id':subject_id, 'tablet_id':tablet_id}}}
        message_str = str(json.dumps(message))
        print("audience_done", message_str)
        KC.client.send_message(message_str)

    #'{"tablet_to_manager": {"action": "register_tablet", "parameters": {"tablet_id": "1", "subject_id": "0"}}}'
    #'{"tablet_to_manager": {"action": "audience_done", "parameters": {"tablet_id": "1", "subject_id": "0"}}}'
    def agree_audience_list(self, agree):

        if agree:
            self.screen_manager.current_screen.ids['agree_audience_list'].background_color = (0, 1, 0, 1)
            self.screen_manager.current_screen.ids['dont_agree_audience_list'].background_color = (0, 0.5, 0.5, 1)
            print("agree")
        else:
            self.screen_manager.current_screen.ids['dont_agree_audience_list'].background_color = (1, 0, 0, 1)
            self.screen_manager.current_screen.ids['agree_audience_list'].background_color = (0, 0.5, 0.5, 1)
            print("disagree")

    def simulation_spinners_submit (self):
        self.proctor1 = self.screen_manager.get_screen('screen_simulation').ids['spinner1'].text
        self.proctor2 = self.screen_manager.get_screen('screen_simulation').ids['spinner2'].text
        self.subject1 = self.screen_manager.get_screen('screen_simulation').ids['spinner1'].text
        self.subject2 = self.screen_manager.get_screen('screen_simulation').ids['spinner2'].text
        self.subject3 = self.screen_manager.get_screen('screen_simulation').ids['spinner3'].text

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
            json_data = [json.loads(data)]
        except:
            json_data = []
            spl = data.split('}{')
            print(spl)
            for k in range(0, len(spl)):
                the_msg = spl[k]
                if k > 0:
                    the_msg = '{' + the_msg
                if k < (len(spl) - 1):
                    the_msg = the_msg + '}'
                json_msg = json.loads(the_msg)
                json_data.append(json_msg)
            # print("data_received err", sys.exc_info())


        for data in json_data:
            print("data['action']", data['action'])
            if (data['action']=='registration_complete'):
                self.screen_manager.get_screen('ScreenRegister').data_received(data)
                print("registration_complete")

            if (data['action'] == 'show_screen'):
                print(data)
                self.screen_manager.current = data['screen_name']

                if 'role' in data:
                    self.screen_manager.current_screen.update_role_bias(role=data['role'], bias=int(data['bias']))

            if (data['action'] == 'start_timer'):
                self.screen_manager.current_screen.ids['timer_time'].start_timer(int(data['seconds']))

            if data['action'] == 'set_widget_text':
                self.screen_manager.current_screen.ids[data['widget_id']].text = data['text']

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
