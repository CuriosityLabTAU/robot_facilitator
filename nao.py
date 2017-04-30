
from naoqi import ALProxy
import sys
import almath


class Nao():

    def __init__(self):
        # Init the connection to nao

        self.robotIP = '192.168.0.100'
        self.port = 9559
        try:
            self.motionProxy = ALProxy("ALMotion", self.robotIP, self.port)
            self.audioProxy = ALProxy("ALAudioPlayer", self.robotIP, self.port)
            self.managerProxy = ALProxy("ALBehaviorManager", self.robotIP, self.port)
            self.postureProxy = ALProxy("ALRobotPosture", self.robotIP, self.port)
            tracker = ALProxy("ALTracker", self.robotIP, self.port)
            self.tts = ALProxy("ALTextToSpeech", self.robotIP, self.port)

        except Exception,e:
            print "Could not create proxy to ALMotion"
            print "Error was: ",e
            sys.exit(1)

        # Get the Robot Configuration
        self.robotConfig = self.motionProxy.getRobotConfig()
        self.motionProxy.rest()
        self.motionProxy.setStiffnesses("Body", 1.0)

    def parse_message(self, message):
        print (message)

    def run_behavior(self, behavior):
        # run a behavior installed on nao
        # for example: "movements/introduction_all_0"

        self.managerProxy.post.runBehavior(behavior)

    def print_installed_behaviors(self):
        # print all the behaviors installed on nao

        names = self.managerProxy.getInstalledBehaviors()
        print "Behaviors on the robot:"
        print names

    def say_text_to_speech (self, text):
        # make nao say the string text
        self.tts.say (text)

    def play_audio_file (self, file):
        # Play audio file on nao.
        # For example: file = '/home/nao/wav/ask_again_0.wav'

        self.audioProxy.playFile(file, 1.0, 0.0)

    def print_installed_sound_sets_list(self):
        #print all the sounds installed on nao
        ssl = self.audioProxy.getInstalledSoundSetsList()
        print ssl

    def change_pose(self, data_str):
        # data_str = 'name1, name2;target1, target2;pMaxSpeedFraction'

        info = data_str.split(';')

        pNames = info[0].split(',')

        pTargetAngles = [float(x) for x in info[1].split(',')]
        pTargetAngles = [x * almath.TO_RAD for x in pTargetAngles]  # Convert to radians

        pMaxSpeedFraction = float(info[2])

        print(pNames, pTargetAngles, pMaxSpeedFraction)
        self.motionProxy.post.angleInterpolationWithSpeed(pNames, pTargetAngles, pMaxSpeedFraction)

    def do_animation(self, action):
        # This function is from tangram. I'm leaving it here just as an example for changing poses

        if action == 'LOOKAT_TABLET':
            self.change_pose('HeadPitch;29.0;0.1')
        elif action == 'LOOKAT_CHILD':
            self.change_pose('HeadPitch;0.0;0.1')
        elif action == 'POSE_FORWARD':
            self.change_pose('HeadPitch;0.0;0.1')
        elif action == 'EXCITED':
            #self.change_pose('HeadPitch,RShoulderPitch;-10.0,-50.0;0.5')
            #self.change_pose('HeadPitch,RShoulderPitch;0.0,70.0;0.5')
            self.managerProxy.post.runBehavior("movements/raise_the_roof/raise_the_roof")
        elif action == 'LEFTRIGHTLOOKING':
            self.change_pose('HeadYaw;-50.0;0.2')
            self.change_pose('HeadYaw;50.0;0.2')
            self.change_pose('HeadYaw;0.0;0.1')
        elif action == 'HAPPY_UP':
            #self.change_pose('HeadPitch,HeadYaw,RShoulderPitch,LShoulderPitch;-10.0,-10.0,-50.0,-50.0;0.5')
            #self.change_pose('HeadPitch,HeadYaw,RShoulderPitch,LShoulderPitch;0.0,0.0,70.0,70.0;0.5')
            self.managerProxy.post.runBehavior("movements/raise_the_roof/raise_the_roof")
        elif action == 'PROUD':
            self.change_pose('RShoulderPitch,RElbowYaw;-50.0,-50.0;0.2')
            self.change_pose('RShoulderPitch,RElbowYaw;50.0,-10.0;0.2')
        elif action == 'SAD':
            self.change_pose('HeadPitch,HeadYaw;10.0,10.0;0.05')
            self.change_pose('HeadPitch,HeadYaw;0.0,0.0;0.1')

