
import rospy
from std_msgs.msg import String
import time

from naoqi import ALProxy
import sys
import almath


class TwistedServer():

    def __init__(self):
        rospy.init_node('rinat')
        self.pub = rospy.Publisher('nao_commands', String, queue_size=10)

    def send_message (self, message):
        rospy.loginfo(message)
        #pub = rospy.Publisher('nao_commands', String, queue_size=10)

        self.pub.publish(message)



ts = TwistedServer()
time.sleep(0.5)
ts.send_message(str('How are you?'))

#send_message(str('How are you?'))