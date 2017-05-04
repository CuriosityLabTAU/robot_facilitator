import json
import rospy
from std_msgs.msg import String
from nao import Nao


class NaoTalkerNode():
    def __init__(self):
        self.nao = Nao()
        self.publisher = rospy.Publisher('nao_talker_topic', String, queue_size=10)
        rospy.init_node('nao_talker_node', anonymous=True)
        rate = rospy.Rate(10)  # 10hz

        while not rospy.is_shutdown():
            hello_str = "hello world %s" % rospy.get_time()
            print (hello_str)
            angles_str = str(self.nao.get_angles())
            rospy.loginfo(angles_str)
            self.publisher.publish(angles_str)
            rate.sleep()


if __name__ == '__main__':
    try:
        nao = NaoTalkerNode()
    except rospy.ROSInterruptException:
        pass