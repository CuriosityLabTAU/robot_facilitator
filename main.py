import json
import rospy
from std_msgs.msg import String
import time
from twisted_server import TwistedServer


ts = TwistedServer()
time.sleep(0.5)


#nao_message = {'action':'say_text_to_speech', 'parameters': ["How are you Orpaz? Happy Birthday!"]}
#nao_message = {'action':'run_behavior', 'parameters': ["movements/introduction_all_0"]}
#nao_message = {'action' :'play_audio_file', 'parameters': ["/home/nao/wav/ask_again_0.wav"]}
nao_message = {'action':'face_tracker','parameters': ['none']}
nao_message_str = str(json.dumps(nao_message))
ts.send_message(nao_message_str)


