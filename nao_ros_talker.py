import json
import rospy
from std_msgs.msg import String
from nao import Nao


class NaoTalkerNode():
    def __init__(self):
        self.nao = Nao()
        self.publisher = rospy.Publisher('nao_talker', String, queue_size=10)
        rospy.init_node('nao_talker', anonymous=True)
        rate = rospy.Rate(10)  # 10hz

        while not rospy.is_shutdown():
            hello_str = "hello world %s" % rospy.get_time()
            angles_str = str(self.nao.get_angles())
            rospy.loginfo(angles_str)
            self.publisher.publish(angles_str)
            rate.sleep()

    def publish_angeles(self):
        rospy.init_node('nao_angeles')

if __name__ == '__main__':
    try:
        nao = NaoTalkerNode()
    except rospy.ROSInterruptException:
        pass