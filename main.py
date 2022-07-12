import sys
from flask import Flask
from flask_jsonrpc import JSONRPC
import cv2
import time
import subprocess
import os
import psutil
from shlex import split
import datetime
import multiprocessing
import client_record2db

numberCanal = 1
date_start = datetime.datetime.now()
date_end = datetime.datetime.now()
filePath = "C:/Praktika/abc/"
fileName = "Video_"
number = 1
flag = True
rtspUrl = "rtsp://root:12345678@192.168.35.202/axis-media/media.amp?videocodec=H264&resolution=1024x768&compression=30&fps=30&videokeyframeinterval=30&event=on"
frame = cv2.VideoCapture(rtspUrl)

app = Flask('record')
# Flask-JSONRPC
jsonrpc = JSONRPC(app, '/api_record', enable_web_browsable_api=True)
#file = "c:/Praktika/abc/out6.mp4"

@jsonrpc.method('launch_start')
def launch_start() -> int:
    #multiprocessing.context.Process
    pr1 = multiprocessing.Process(target=launch)
    pr1.start()
    return pr1.pid

@jsonrpc.method('echo')
def echo(message: str) -> str:
    return message

@jsonrpc.method('launch_end')
def launch_end(pr1: int):
    p = psutil.Process(pr1)
    p.terminate()


def launch():
    global frame
    v=1
    while (v != 2):
        status, image = frame.read()
        pr = start_recording()
        save_frame(image)
        stop_recording(pr)
        size_record()
        v += 1

def start_recording():
    global date_start
    global filePath
    global fileName
    global number
    global proc

    date_start = datetime.datetime.now()
    date_start = str(date_start).partition('.')[0]
    date_start = date_start.replace(':', '_')
    date_start = date_start.replace(' ', '_time_')
    date_start1 = str(filePath + date_start + ".mp4")
   # date_start1 = str(datetime.datetime.strptime(date_start,'%Y-%m-%d-%H-%M-%S'))
    #date_start1 = str(date_start.strftime('%Y-%m-%d_%H-%M'))
    #date_start2 = date3.replace(':', '_')
    #print(date_start1)
    #date_
    cmd = f"ffmpeg -y -i '{'rtsp://root:12345678@192.168.35.202/axis-media/media.amp?videocodec=H264&resolution=1024x768&compression=30&fps=30&videokeyframeinterval=30&event=on'}' -movflags +frag_keyframe+separate_moof+omit_tfhd_offset+empty_moov -acodec copy -vcodec copy {date_start1}"
    #cmd = f"ffmpeg -y -i '{'rtsp://root:12345678@192.168.35.202/axis-media/media.amp?videocodec=H264&resolution=1024x768&compression=30&fps=30&videokeyframeinterval=30&event=on'}' -acodec copy -vcodec copy c:/Praktika/abc/out6.mp4"
    proc = subprocess.Popen(split(cmd))
    time.sleep(20)
    return proc

def stop_recording(pr):
    global date_end
    global number
    pr.terminate()
   # os.kill(pr, signal.CTRL_C_EVENT)
    date_end = datetime.datetime.now()
    client_record2db.insert_into_db(15,'sgd',12,'/sgaf','2022-07-06 14:07:14.300513','2022-07-06 14:07:14.300513',12,'avi','/ssfh')
    # f = open("name.txt", 'w')
    # number += 1
    # number1 = str(number)
    # f.write(number1)
    # f.close()


def size_record():
    global filePath
    global fileName
    size_video = str(filePath + date_start + '.mp4')
    s = round((os.path.getsize(size_video) / (1024*2)), 2)
    print('File size:', s, 'bytes')
    return s


def save_frame(img):
    global number
    cv2.imwrite(filePath + "frame_" + date_start + ".jpg", img)
    #return str(filePath + "frame%d.jpg" % (number-1))


def kill(proc_pid):
    process = psutil.Process(proc_pid)
    for proc in process.children(recursive=True):
        proc.kill()
    process.kill()

if __name__ == "__main__":
    launch_start()
    launch_end()
   # app.run(port=1235, host='0.0.0.0')
