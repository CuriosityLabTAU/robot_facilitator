import os
import threading
from naoqi import ALProxy
import time

def init_experiment(session_id):
    start_working(session_id)

    time.sleep(60)


def start_working(session_id):

    session_id = session_id

    def rosbag_record():
        os.system('rosbag record -a -o data/robot_facilitator_chi_' + session_id + '.bag')

    def init_nao_ros_listener():
        os.system('python nao_ros_listener.py')
        return

    def init_nao_ros_talker():
        os.system('python nao_ros_talker.py')
        return

    def init_robot_facilitator_app():
        os.system('python robotator_app/robot_facilitator_app.py')

    def skeleton_launch():
        os.system('roslaunch skeleton_markers markers.launch')
        return

    def camera_affdex_launch():
        os.system('roslaunch multi_camera_affdex multi_camera_affdex.launch')


    t1 = threading.Thread(target=rosbag_record)
    t1.start()
    threading._sleep(0.2)

    t2 = threading.Thread(target=init_nao_ros_listener)
    t2.start()
    threading._sleep(0.2)

    #t3 = threading.Thread(target=init_nao_ros_talker)
    #t3.start()
    #threading._sleep(0.2)

    t4 = threading.Thread(target=init_robot_facilitator_app)
    t4.start()
    threading._sleep(0.2)


init_experiment("2")