import os
import threading
import time


def run_periphery():
    start_working()
    time.sleep(60)


def start_working():

    def find_cameras():
        result = os.popen("ls /dev").read().split('\n')

        video_list = [x for x in result if 'video' in x]
        media_list = [x for x in result if 'media' in x]

        result = os.popen("arecord -l").read().split('\n')
        webcam_card_list = [x[5] for x in result if 'Webcam' in x]
        return video_list, media_list, webcam_card_list

    video_list, media_list, webcam_card_list = find_cameras()
    def run_camera(camera_id):
        run_command = 'roslaunch usb_cam usb_cam.launch device:="' + camera_id + '" camera_frame_id:="usb_cam_' + camera_id[-1] + '"'
        print(run_command)
        os.system(run_command)


    threads = []
    for v in video_list[:1]:
        threads.append(threading.Thread(target=run_camera, args=(v,)))
        threads[-1].start()
        threading._sleep(0.2)

run_periphery()

