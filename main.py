
import rospy
from std_msgs.msg import String
from naoqi import ALProxy
import sys
import almath

rospy.init_node('rinat')
pub = rospy.Publisher ('nao_commands', String, queue_size=10)
message = 'say'
#rospy.loginfo (message)
pub.publish(message)
rospy.spin()