
import json
import rospy
from std_msgs.msg import String


class ManagerNode():
    def __init__(self):
        self.robot_publisher = rospy.Publisher('nao_commands', String, queue_size=10)
        self.tablet_publisher = rospy.Publisher('to_twisted', String, queue_size=10)
        rospy.init_node('nao_listener_node') #init a listener:
        rospy.Subscriber('nao_state', String, self.callback_nao)
        rospy.Subscriber('to_manager', String, self.callback_tablet)
        rospy.spin() #spin() simply keeps python from exiting until this node is stopped


    def callback_tablet (self, data):


    def callback_nao (self, data):
        print("callback_robotator", data.data)
        message = data.data
        rospy.loginfo(message)
        self.nao.parse_message(message)

    #def publish_angeles(self):
    #    rospy.init_node('nao_angeles')

if __name__ == '__main__':
    try:
        nao = NaoListenerNode()
    except rospy.ROSInterruptException:
        pass
