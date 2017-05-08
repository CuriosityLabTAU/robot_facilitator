import json
import rospy
from std_msgs.msg import String
import time

from naoqi import ALProxy
import sys
import almath


class TwistedServer():

    def __init__(self):
        rospy.init_node('rinat')
        self.pub = rospy.Publisher('nao_commands_topic', String, queue_size=10)

    def send_message (self, message):
        rospy.loginfo(message)
        #pub = rospy.Publisher('nao_commands', String, queue_size=10)

        self.pub.publish(message)


ts = TwistedServer()
time.sleep(0.5)

# task_dic =  {'size': '5 5', 'pieces': [('square', '90', '1 1'), ('small triangle2', '180', '0 1')]}
# json_str = json.dumps(task_dic)

#nao_message = {'action':'say_text_to_speech', 'parameters': ["How are you Orpaz? Happy Birthday!"]}
#nao_message = {'action':'run_behavior', 'parameters': ["movements/introduction_all_0"]}
#nao_message = {'action' :'play_audio_file', 'parameters': ["/home/nao/wav/ask_again_0.wav"]}
nao_message = {'action':'face_tracker','parameters': ['none']}
nao_message_str = str(json.dumps(nao_message))
ts.send_message(nao_message_str)


