
import json
import rospy
from std_msgs.msg import String
import time


class ManagerNode():

    tablets = {}    #in the form of {tablet_id_1:{"subject_id":subject_id, "tablet_ip";tablet_ip}
                                    #,tablet_id_2:{"subject_id":subject_id, "tablet_ip";tablet_ip}

    tablets_ips = {}
    tablet_ids = {}
    tablets_subjects_ids = {}

    tablet_audience_data = {}
    tablet_audience_agree = {}


    def __init__(self):
        self.robot_publisher = rospy.Publisher('to_nao', String, queue_size=10)
        self.tablet_publisher = rospy.Publisher('to_tablet', String, queue_size=10)
        rospy.init_node('manager_node') #init a listener:
        rospy.Subscriber('nao_state', String, self.callback_nao_state)
        rospy.Subscriber('tablet_to_manager', String, self.callback_to_manager)
        rospy.Subscriber('log', String, self.callback_log)
        rospy.spin() #spin() simply keeps python from exiting until this node is stopped

        self.waiting = False


    def run_study(self):
        with open("robotator_study.json") as data_file:
            logics_json = json.load(data_file)
            #self.poses_conditions = logics_json['conditions']
            self.study_sequence = logics_json['sequence']
            for action in self.study_sequence[:7]:
                print ("action",action["action"])
                if (action["action"] == "run_behavior" or action["action"]=="rest"):
                    print("if", action)
                    nao_message = action
                    self.robot_publisher.publish(json.dumps(nao_message))
                    self.waiting = True
                    while self.waiting:
                        pass
                if (action['action'] == 'show_screen'):
                    if "tablets" in action:
                        for tablet_id in action['tablets']:
                            try:
                                client_ip = self.tablets_ips[str(tablet_id)]
                                message = {'action': 'show_screen', 'client_ip': client_ip, 'screen_name': action['screen_name']}
                                self.tablet_publisher.publish(json.dumps(message))
                            except:
                                print('not enough tablets')

                if action['action'] == 'sleep':
                    # send to all tablets, start_timer
                    for tablet_ip in self.tablets_ips:
                        message = {'action': 'start_timer', 'client_ip': client_ip, 'seconds': action['seconds']}
                        self.tablet_publisher.publish(json.dumps(message))
                    nao_message = {'action': 'sound_tracker'}
                    self.robot_publisher.publish(json.dumps(nao_message))

                    time.sleep(float(action['seconds']))

                if action['action'] == 'sound_tracker':
                    self.robot_publisher.publish(json.dumps(action))

                # TODO check this
                if action['action'] == "run_behavior_special":
                    if action['parameters'][0] == 'r10':
                        # find min, look at
                        min_text = (0, 100000)
                        for tablet_id, size_text in self.tablet_audience_data.items():
                            if size_text < min_text[1]:
                                min_text = (tablet_id, size_text)
                        nao_message = {'action': 'run_behavior',
                                       'parameters': ['robot_facilitator-ad2c5c/head_tablet_' + str(min_text[0])]}
                        self.robot_publisher.publish(json.dumps(nao_message))
                        nao_message = {'action': 'run_behavior', 'parameters': ['robot_facilitator-ad2c5c/r10']}
                        self.robot_publisher.publish(json.dumps(nao_message))

                if action['parameters'][0] == 'r12':
                    # find min, look at
                    max_text = (0, 0)
                    for tablet_id, size_text in self.tablet_audience_data.items():
                        if size_text > max_text[1]:
                            max_text = (tablet_id, size_text)
                    nao_message = {'action': 'run_behavior',
                                   'parameters': ['robot_facilitator-ad2c5c/head_tablet_' + str(max_text[0])]}
                    self.robot_publisher.publish(json.dumps(nao_message))
                    nao_message = {'action': 'run_behavior', 'parameters': ['robot_facilitator-ad2c5c/r12']}
                    self.robot_publisher.publish(json.dumps(nao_message))

                if action['parameters'][0] == 'r17':
                    for tablet_id, agree in self.tablet_audience_agree.items():
                        if not agree:
                            nao_message = {'action': 'run_behavior',
                                           'parameters': ['robot_facilitator-ad2c5c/head_tablet_' + str(tablet_id)]}
                            self.robot_publisher.publish(json.dumps(nao_message))
                            nao_message = {'action': 'run_behavior', 'parameters': ['robot_facilitator-ad2c5c/r17']}
                            self.robot_publisher.publish(json.dumps(nao_message))
                            break







                # nao_message = {'action': 'say_text_to_speech', 'parameters': ['hello']}
        # self.robot_publisher.publish(json.dumps(nao_message))


    def callback_nao_state(self, data):
        print("manager callback_nao_state", data.data)
        self.waiting = False
        # message = data.data
        # rospy.loginfo(message)
        # self.tablet_publisher.publish(message)
        # self.nao.parse_message(message)

    def callback_to_manager(self, data):
        print("manager callback_to_manager", data.data)
        data_json = json.loads(data.data)
        action = data_json['action']
        if (action=='register_tablet'):
            self.register_tablet(data_json['parameters']['tablet_id'],data_json['parameters']['subject_id'],data_json['client_ip'])
        else:
            self.robot_publisher.publish(data.data)

    def register_tablet(self, tablet_id, subject_id, client_ip):
        print("register_tablet", type(client_ip),client_ip)
        print(self.tablets)
        self.tablets[tablet_id] = {'subject_id':subject_id, 'tablet_ip':client_ip}
        self.tablets_subjects_ids[tablet_id] = subject_id
        self.tablets_ips[tablet_id] = client_ip
        self.tablets_ips[client_ip] = tablet_id

        nao_message = {'action': 'say_text_to_speech', 'client_ip':client_ip,'parameters': ['register tablet', 'tablet_id',str(tablet_id), 'subject id',str(subject_id)]}
        self.robot_publisher.publish(json.dumps(nao_message))
        if (len(self.tablets)>0):
            print("two tablets are registered")

            for key,value in self.tablets_ips.viewitems():
                client_ip = value
                message = {'action':'registration_complete','client_ip':client_ip}
                self.tablet_publisher.publish(json.dumps(message))

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

        if 'audience_list' in log['obj']:
            if 'text' in log['action']:
                if log['client_ip'] not in self.tablet_audience_data:
                    self.tablet_audience_data[log['client_ip']] = 0
                self.tablet_audience_data[self.tablets_ips[log['client_ip']]] += 1
                print(self.tablet_audience_data)

        if 'agree_audience_list' in log['obj']:
            if log['client_ip'] not in self.tablet_audience_agree:
                self.tablet_audience_agree[log['client_ip']] = False
            if log['obj'] == 'agree_audience_list':
                self.tablet_audience_agree[self.tablets_ips[log['client_ip']]] = True
            else:
                self.tablet_audience_agree[self.tablets_ips[log['client_ip']]] = False


if __name__ == '__main__':
    try:
        manager = ManagerNode()
        # manager.run_study()
    except rospy.ROSInterruptException:
        pass
