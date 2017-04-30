import rospy
from std_msgs.msg import String
from nao import Nao


class NaoNode():
    def __init__(self):
       self.nao = Nao()
       self.publisher = rospy.Publisher('nao_state', String, queue_size=10)

    def start(self):
        print("start")
        #init a listener:
        rospy.init_node('nao_listener')
        rospy.Subscriber('nao_commands', String, self.callback_robotator)
        rospy.spin() #spin() simply keeps python from exiting until this node is stopped

    def callback_robotator (self, data):
        print("callback_robotator", data.data)
        message = data.data
        rospy.loginfo(message)
        self.nao.say_text_to_speech(message)

nao = NaoNode()
nao.start()