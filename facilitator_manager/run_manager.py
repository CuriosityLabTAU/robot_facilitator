
import json
import rospy
from std_msgs.msg import String
import time
from threading import Timer

class ManagerNode():

    number_of_tablets = 3
    tablets = {}    #in the form of {tablet_id_1:{"subject_id":subject_id, "tablet_ip";tablet_ip}
                                    #,tablet_id_2:{"subject_id":subject_id, "tablet_ip";tablet_ip}

    tablets_ips = {}
    tablets_ids = {}
    tablets_subjects_ids = {}

    tablet_audience_data = {}
    tablets_audience_agree = {}
    tablets_audience_done = {}  # by id
    count_audience_done = 0

    attention_tablet = {}
    listen_to_text = None
    text_audience_group = {}
    sleep_timer = None
    is_audience_done  = False

    waiting = False
    waiting_timer = False
    waiting_robot = False

    def __init__(self):
        self.robot_publisher = rospy.Publisher('to_nao', String, queue_size=10)
        self.tablet_publisher = rospy.Publisher('to_tablet', String, queue_size=10)
        rospy.init_node('manager_node') #init a listener:
        rospy.Subscriber('nao_state', String, self.callback_nao_state)
        rospy.Subscriber('tablet_to_manager', String, self.callback_to_manager)
        rospy.Subscriber('log', String, self.callback_log)
        self.waiting = False
        self.waiting_timer = False
        self.waiting_robot = False
        i=1
        while i <= self.number_of_tablets:
            self.tablets_audience_agree[i]= None
            i=+1

        rospy.spin() #spin() simply keeps python from exiting until this node is stopped


    def timer_out (self):
        print ("timer_out")
        self.sleep_timer.cancel()
        print ("self.sleep_timer.cancel()")
        self.waiting = False
        self.waiting_timer = False

    def run_robot_behavior(self,nao_message):
        self.robot_publisher.publish(json.dumps(nao_message))
        self.waiting = True
        self.waiting_robot = True
        while self.waiting_robot:
            pass
        print('done waiting_robot', nao_message["action"])

    def run_study(self):
        data_file = open("robotator_study.json")
        logics_json = json.load(data_file)
        #self.poses_conditions = logics_json['conditions']
        self.study_sequence = logics_json['sequence']
        for action in self.study_sequence:
            print ("action",action["action"])


            if action["action"]=="rest" or action["action"]=="wake_up":
                print("if", action)
                nao_message = action
                self.run_robot_behavior(nao_message)

            if action["action"] == "run_behavior":
                print("one_min_left",action["parameters"][0], self.is_audience_done)
                if ("one_min_left" in action["parameters"][0]) and (self.is_audience_done == True):
                    print("one_min_left and audience_done")
                elif ("TU10" in action["parameters"][0]):
                    if (self.is_audience_done == True):
                        nao_message = {"action":"run_behavior", "parameters":["robot_facilitator-ad2c5c/robotator_behaviors/TU10a", "wait"]}
                    else:
                        nao_message = {"action": "run_behavior", "parameters": ["robot_facilitator-ad2c5c/robotator_behaviors/TU10b", "wait"]}
                    self.is_audience_done = False
                    self.run_robot_behavior(nao_message)

                elif ("TU12" in action["parameters"][0]):
                    if (self.is_audience_done == True):
                        nao_message = {"action": "run_behavior",
                                       "parameters": ["robot_facilitator-ad2c5c/robotator_behaviors/TU12a", "wait"]}
                    else:
                        nao_message = {"action": "run_behavior",
                                       "parameters": ["robot_facilitator-ad2c5c/robotator_behaviors/TU12b", "wait"]}
                    self.is_audience_done = False
                    self.run_robot_behavior(nao_message)


                elif ("TU13" in action["parameters"][0]):
                    all_agree = True
                    for item in self.tablets_audience_agree.items():
                        all_agree = all_agree and item

                    if not all_agree:
                        nao_message = {"action": "run_behavior",
                                       "parameters": ["robot_facilitator-ad2c5c/robotator_behaviors/TU13a", "wait"]}
                        self.run_robot_behavior(nao_message)
                        self.attention_tablet[tablet_id] = True
                    else:
                        nao_message = {'action': 'run_behavior',
                                       'parameters': ['robot_facilitator-ad2c5c/robotator_behaviors/TU13b', 'wait']}
                        self.run_robot_behavior(nao_message)



                else:
                    print("if", action)
                    nao_message = action
                    self.run_robot_behavior(nao_message)

            if action["action"] == "sleep":
                print("the action is sleep", action["seconds"], self.is_audience_done)
                if (self.is_audience_done == False):
                    self.sleep_timer = Timer(float(action["seconds"]), self.timer_out)
                    print("self.sleep_timer.start()")
                    self.sleep_timer.start()
                    self.waiting = True
                    self.waiting_timer = True
                    while self.waiting_timer:
                        pass
                    print('done waiting_timer', action)
                    #nao_message = {'action': 'sound_tracker'}
                    #self.robot_publisher.publish(json.dumps(nao_message))
                    #time.sleep(float(action['seconds']))

            if action['action'] == 'start_timer':
                print("the action is start timer")
                for tablet_id in action['tablets']:
                    try:
                        client_ip = self.tablets_ips[str(tablet_id)]
                        message = {'action': 'start_timer', 'client_ip': client_ip,
                                   'seconds': action['seconds']}
                        self.tablet_publisher.publish(json.dumps(message))
                    except:
                        print('not enough tablets')

            if action['action'] == 'sound_tracker':
                self.robot_publisher.publish(json.dumps(action))

            if action['action'] == 'say_text_to_speech':
                self.robot_publisher.publish(json.dumps(action))

            if (action['action'] == 'show_screen'):
                self.init_audience_done()
                if "tablets" in action:
                    for tablet_id in action['tablets']:
                        try:
                            client_ip = self.tablets_ips[str(tablet_id)]
                            message = {'action': 'show_screen', 'client_ip': client_ip, 'screen_name': action['screen_name']}
                            self.tablet_publisher.publish(json.dumps(message))
                        except:
                            print('not enough tablets')
                else:
                    if "parameters" in action:
                        if "r13" in action['parameters']:
                            for tablet_id, tablet_ip in self.tablets_ips.items():
                                if tablet_id not in self.attention_tablet:
                                    message = {'action': 'show_screen', 'client_ip': tablet_ip,
                                               'screen_name': action['screen_name']}
                                    self.tablet_publisher.publish(json.dumps(message))
                                    self.attention_tablet[tablet_id] = False
                                    self.listen_to_text = tablet_ip
                                    break

                        if "r16" in action['parameters']:
                            for widget_id, text in self.text_audience_group.items():
                                message = {'action': 'set_widget_text', 'client_ip': tablet_ip,
                                           'widget_id': widget_id, 'text': text}
                                self.tablet_publisher.publish(json.dumps(message))
                                self.listen_to_text = None

                        if "r32" in action['parameters']:
                            for tablet_id, tablet_ip in self.tablets_ips.items():
                                if tablet_id not in self.attention_tablet:
                                    message = {'action': 'show_screen', 'client_ip': tablet_ip,
                                               'screen_name': action['screen_name']}
                                    self.tablet_publisher.publish(json.dumps(message))
                                    self.attention_tablet[tablet_id] = False
                                    break
                        if "r39" in action['parameters']:
                            tablet_ip = self.tablets_ips.values()[0]
                            message = {'action': 'show_screen', 'client_ip': tablet_ip,
                                       'screen_name': action['screen_name'], 'role': 'proctor', 'bias': '0'}
                            self.tablet_publisher.publish(json.dumps(message))
                            tablet_ip = self.tablets_ips.values()[1]
                            message = {'action': 'show_screen', 'client_ip': tablet_ip,
                                       'screen_name': action['screen_name'], 'role': 'proctor', 'bias': '1'}
                            self.tablet_publisher.publish(json.dumps(message))
                            tablet_ip = self.tablets_ips.values()[2]
                            message = {'action': 'show_screen', 'client_ip': tablet_ip,
                                       'screen_name': action['screen_name'], 'role': 'proctor', 'bias': '2'}
                            self.tablet_publisher.publish(json.dumps(message))
                            tablet_ip = self.tablets_ips.values()[3]
                            message = {'action': 'show_screen', 'client_ip': tablet_ip,
                                       'screen_name': action['screen_name'], 'role': 'subject', 'bias': '0'}
                            self.tablet_publisher.publish(json.dumps(message))
                            tablet_ip = self.tablets_ips.values()[4]
                            message = {'action': 'show_screen', 'client_ip': tablet_ip,
                                       'screen_name': action['screen_name'], 'role': 'subject', 'bias': '1'}
                            self.tablet_publisher.publish(json.dumps(message))

            # TODO check this
            if action['action'] == "run_behavior_special":
                if action['parameters'][0] == 'r10':
                    # find min, look at
                    min_text = (0, 100000)
                    for tablet_id, size_text in self.tablet_audience_data.items():
                        if size_text < min_text[1]:
                            min_text = (tablet_id, size_text)
                    nao_message = {'action': 'run_behavior',
                                   'parameters': ['robot_facilitator-ad2c5c/point_to_' + str(min_text[0])]}
                    self.robot_publisher.publish(json.dumps(nao_message))
                    nao_message = {'action': 'run_behavior', 'parameters': ['robot_facilitator-ad2c5c/r10', 'wait']}
                    self.robot_publisher.publish(json.dumps(nao_message))
                    self.attention_tablet[min_text[0]] = True

                if action['parameters'][0] == 'r12':
                    # find min, look at
                    max_text = (0, 0)
                    for tablet_id, size_text in self.tablet_audience_data.items():
                        if size_text > max_text[1]:
                            max_text = (tablet_id, size_text)
                    nao_message = {'action': 'run_behavior',
                                   'parameters': ['robot_facilitator-ad2c5c/point_to_' + str(max_text[0])]}
                    self.robot_publisher.publish(json.dumps(nao_message))
                    nao_message = {'action': 'run_behavior', 'parameters': ['robot_facilitator-ad2c5c/r12', 'wait']}
                    self.robot_publisher.publish(json.dumps(nao_message))
                    self.attention_tablet[max_text[0]] = True

                if action['parameters'][0] == 'r17':
                    for tablet_id, agree in self.tablets_audience_agree.items():
                        if not agree:
                            nao_message = {'action': 'run_behavior',
                                           'parameters': ['robot_facilitator-ad2c5c/point_to_' + str(tablet_id)]}
                            self.robot_publisher.publish(json.dumps(nao_message))
                            nao_message = {'action': 'run_behavior', 'parameters': ['robot_facilitator-ad2c5c/r17', 'wait']}
                            self.robot_publisher.publish(json.dumps(nao_message))
                            self.attention_tablet[tablet_id] = True
                            break

                if action['parameters'][0] == 'r34':
                    for tablet_id, status in self.attention_tablet.items():
                        if status == False:
                            nao_message = {'action': 'run_behavior',
                                           'parameters': ['robot_facilitator-ad2c5c/point_to_' + str(tablet_id)]}
                            self.robot_publisher.publish(json.dumps(nao_message))
                            nao_message = {'action': 'run_behavior', 'parameters': ['robot_facilitator-ad2c5c/r34', 'wait']}
                            self.robot_publisher.publish(json.dumps(nao_message))
                            status = True
                            break

                if action['parameters'][0] == 'r41':
                    nao_message = {'action': 'run_behavior', 'parameters': ['robot_facilitator-ad2c5c/r41', 'wait']}
                    self.robot_publisher.publish(json.dumps(nao_message))
                    tablet_id = self.tablets_ids.values()[3]
                    nao_message = {'action': 'run_behavior',
                                   'parameters': ['robot_facilitator-ad2c5c/point_to_' + str(tablet_id)]}
                    self.robot_publisher.publish(json.dumps(nao_message))
                    tablet_id = self.tablets_ids.values()[4]
                    nao_message = {'action': 'run_behavior',
                                   'parameters': ['robot_facilitator-ad2c5c/point_to_' + str(tablet_id)]}
                    self.robot_publisher.publish(json.dumps(nao_message))

                if action['parameters'][0] == 'r42':
                    nao_message = {'action': 'run_behavior', 'parameters': ['robot_facilitator-ad2c5c/r42', 'wait']}
                    self.robot_publisher.publish(json.dumps(nao_message))
                    tablet_id = self.tablets_ids.values()[0]
                    nao_message = {'action': 'run_behavior',
                                   'parameters': ['robot_facilitator-ad2c5c/point_to_' + str(tablet_id)]}
                    self.robot_publisher.publish(json.dumps(nao_message))
                    tablet_id = self.tablets_ids.values()[1]
                    nao_message = {'action': 'run_behavior',
                                   'parameters': ['robot_facilitator-ad2c5c/point_to_' + str(tablet_id)]}
                    self.robot_publisher.publish(json.dumps(nao_message))
                    tablet_id = self.tablets_ids.values()[2]
                    nao_message = {'action': 'run_behavior',
                                   'parameters': ['robot_facilitator-ad2c5c/point_to_' + str(tablet_id)]}
                    self.robot_publisher.publish(json.dumps(nao_message))

                if action['parameters'][0] == 'r47':
                    nao_message = {'action': 'run_behavior', 'parameters': ['robot_facilitator-ad2c5c/r47', 'wait']}
                    self.robot_publisher.publish(json.dumps(nao_message))
                    tablet_id = self.tablets_ids.values()[0]
                    nao_message = {'action': 'run_behavior',
                                   'parameters': ['robot_facilitator-ad2c5c/point_to_' + str(tablet_id)]}

                if action['parameters'][0] == 'r49':
                    nao_message = {'action': 'run_behavior', 'parameters': ['robot_facilitator-ad2c5c/r49', 'wait']}
                    self.robot_publisher.publish(json.dumps(nao_message))
                    tablet_id = self.tablets_ids.values()[1]
                    nao_message = {'action': 'run_behavior',
                                   'parameters': ['robot_facilitator-ad2c5c/point_to_' + str(tablet_id)]}

                if action['parameters'][0] == 'r51':
                    nao_message = {'action': 'run_behavior', 'parameters': ['robot_facilitator-ad2c5c/r51', 'wait']}
                    self.robot_publisher.publish(json.dumps(nao_message))
                    tablet_id = self.tablets_ids.values()[2]
                    nao_message = {'action': 'run_behavior',
                                   'parameters': ['robot_facilitator-ad2c5c/point_to_' + str(tablet_id)]}

                if action['parameters'][0] == 'r54':
                    nao_message = {'action': 'run_behavior', 'parameters': ['robot_facilitator-ad2c5c/r47', 'wait']}
                    self.robot_publisher.publish(json.dumps(nao_message))
                    tablet_id = self.tablets_ids.values()[3]
                    nao_message = {'action': 'run_behavior',
                                   'parameters': ['robot_facilitator-ad2c5c/point_to_' + str(tablet_id)]}

                if action['parameters'][0] == 'r56':
                    nao_message = {'action': 'run_behavior', 'parameters': ['robot_facilitator-ad2c5c/r51', 'wait']}
                    self.robot_publisher.publish(json.dumps(nao_message))
                    tablet_id = self.tablets_ids.values()[4]
                    nao_message = {'action': 'run_behavior',
                                   'parameters': ['robot_facilitator-ad2c5c/point_to_' + str(tablet_id),
                                                  'wait']}
                # nao_message = {'action': 'say_text_to_speech', 'parameters': ['hello']}
    # self.robot_publisher.publish(json.dumps(nao_message))


    def callback_nao_state(self, data):
        print("manager callback_nao_state", data.data, self.waiting_robot)
        if 'register tablet' not in data.data and 'sound_tracker' not in data.data:
            self.waiting = False
            self.waiting_robot = False
        # message = data.data
        # rospy.loginfo(message)
        # self.tablet_publisher.publish(message)
        # self.nao.parse_message(message)

    def callback_to_manager(self, data):
        print("manager callback_to_manager", data.data)
        data_json = json.loads(data.data)
        action = data_json['action']
        if (action == 'register_tablet'):
            self.register_tablet(data_json['parameters']['tablet_id'],data_json['parameters']['subject_id'],data_json['client_ip'])
        elif (action == 'audience_done'):
            self.audience_done(data_json['parameters']['tablet_id'],data_json['parameters']['subject_id'],data_json['client_ip'])
        else:
            self.robot_publisher.publish(data.data)

    def audience_done (self, tablet_id, subject_id, client_ip):
        print("audience_done!!! tablet_id=", tablet_id)
        self.count_audience_done = 0
        print ("values before", self.tablets_audience_done.values())
        self.tablets_audience_done[tablet_id] =  True
        print ("values after",self.tablets_audience_done.values())
        for value in self.tablets_audience_done.values():
            if value ==True:
                self.count_audience_done += 1
                print("self.count_audience_done",self.count_audience_done)

        if (self.count_audience_done == self.number_of_tablets):
            print("self.count_audience_done == self.number_of_tablets",self.count_audience_done,self.number_of_tablets)
            try:
                self.sleep_timer.cancel()
                print("self.sleep_timer.cancel()")
            except:
                print("failed self.sleep_timer_cancel")
            self.waiting_timer = False
            self.is_audience_done = True
            #restart the values for future screens
            self.count_audience_done = 0
            #for key in self.tablets_audience_done.keys():
            #    self.tablets_audience_done[key]=False

    def init_audience_done(self):
        self.is_audience_done = False
        # restart the values for future screens
        self.count_audience_done = 0
        for key in self.tablets_audience_done.keys():
            self.tablets_audience_done[key] = False

    def audience_group_done(self, tablet_id, subject_id, client_ip):
        print("audience_group_done!!!")
        self.sleep_timer.cancel()
        print("self.sleep_timer.cancel()")
        self.waiting = False
        self.waiting_timer = False
        self.is_audience_done = True


    def register_tablet(self, tablet_id, subject_id, client_ip):
        print("register_tablet", type(client_ip),client_ip)
        print(self.tablets)
        self.tablets[tablet_id] = {'subject_id':subject_id, 'tablet_ip':client_ip}
        self.tablets_subjects_ids[tablet_id] = subject_id
        self.tablets_ips[tablet_id] = client_ip
        self.tablets_ids[client_ip] = tablet_id
        self.tablets_audience_done[tablet_id] = False

        nao_message = {'action': 'say_text_to_speech', 'client_ip':client_ip,'parameters': ['register tablet', 'tablet_id',str(tablet_id), 'subject id',str(subject_id)]}
        self.robot_publisher.publish(json.dumps(nao_message))
        if (len(self.tablets) == self.number_of_tablets):
            print("two tablets are registered")
            for key,value in self.tablets_ips.viewitems():
                client_ip = value
                message = {'action':'registration_complete','client_ip':client_ip}
                self.tablet_publisher.publish(json.dumps(message))
            time.sleep(2)
            self.run_study()

    def scene1(self):
        print("start")
        str_wav = '/home/nao/wav_facilitator/r1.wav'
        self.robot_play_audio_file(str_wav)

    def robot_play_audio_file (self, wav_path):
        nao_message = {'action': 'play_audio_file', 'parameters': [wav_path]}
        self.robot_publisher.publish(json.dumps(nao_message))
        print("end start")


    # def callback_to_manager_draft (self, data):
    #     direction = {1:"\"HeadPitch;0.0;0.1\"",2:"\"HeadPitch;29.0;0.1\""}
    #     #direction = {1: 'HeadPitch;80.0;0.1', 2: 'HeadPitch;29.0;0.9'}
    #     print("manager callback_to_manager", data.data)
    #     #send the command to the robot
    #     data_json = json.loads(data.data)
    #
    #     #tablet_id = int(data_json['parameters'][0])
    #
    #     #nao_message = {'action': 'change_pose', 'parameters': direction[tablet_id]}
    #
    #     text_input = data_json['parameters']
    #     print("text_input", text_input)
    #     # nao_message = {'action': 'say_text_to_speech', 'parameters': text_input}  #client_ip = str(data_json["client_ip"])
    #     #nao_message = {'action': 'change_pose', 'parameters': direction[tablet_id]}
    #     #self.robot_publisher.publish (json.dumps(nao_message))
    #     self.robot_publisher.publish(data.data)



    #def publish_angeles(self):
    #    rospy.init_node('nao_angeles')

    def callback_log(self, data):
        print('----- log -----', data)
        log = json.loads(data.data)
        print(log)

        if 'audience_done' in log['obj'] and log['action'] == 'press':
            client_ip = log['client_ip']
            tablet_id = self.tablets_ids[client_ip]
            subject_id = self.tablets_subjects_ids[tablet_id]
            self.audience_done(tablet_id,subject_id,client_ip)

        if 'audience_group_done' in log['obj'] and log['action'] == 'press':
            client_ip = log['client_ip']
            tablet_id = self.tablets_ids[client_ip]
            subject_id = self.tablets_subjects_ids[tablet_id]
            self.audience_group_done(tablet_id,subject_id,client_ip)

        if 'audience_list' in log['obj']:
            if 'text' in log['action']:
                if self.tablets_ids[log['client_ip']] not in self.tablet_audience_data:
                    self.tablet_audience_data[self.tablets_ids[log['client_ip']]] = 0
                self.tablet_audience_data[self.tablets_ids[log['client_ip']]] += 1
                print("self.tablet_audience_data", self.tablet_audience_data)

        if 'agree_audience_list' in log['obj']:
            print("agree_audience_list")
            if self.tablets_ids[log['client_ip']] not in self.tablets_audience_agree.values():
                self.tablets_audience_agree[self.tablets_ids[log['client_ip']]] = False
            if log['obj'] == 'agree_audience_list' and log['action'] == 'press':
                print("agree_audience_list True")
                self.tablets_audience_agree[self.tablets_ids[log['client_ip']]] = True
            elif (log['action'] == 'press'):
                print("agree_audience_list False")
                self.tablets_audience_agree[self.tablets_ids[log['client_ip']]] = False

            allVoted = True
            i=1
            while i <= self.number_of_tablets:
                if (self.tablets_audience_agree[i] == None):
                    allVoted = False
                i =+ 1
            if (allVoted == True):
                self.waiting_timer = False
                self.sleep_timer.cancel()
                print("self.sleep_timer.cancel()")
                self.waiting = False
                self.waiting_timer = False


        if self.listen_to_text:
            self.text_audience_group[log['obj']] = log['comment']


if __name__ == '__main__':
    try:
        manager = ManagerNode()
        # manager.run_study()
    except rospy.ROSInterruptException:
        pass
