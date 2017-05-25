import json
import rospy
from std_msgs.msg import String
import time

from naoqi import ALProxy
import sys
import almath


class FakeTwistedServer():
    publishers = {}

    def __init__(self):

        rospy.init_node('fake_server')
        self.pub = rospy.Publisher('nao_commands', String, queue_size=10)

    def send_message (self, topic, message):
        rospy.loginfo(message)

        self.pub.publish(message)





