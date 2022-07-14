import shlex
import sys
from multiprocessing import Queue
import threading

from flask import Flask
from flask_jsonrpc import JSONRPC
import cv2
import time
import subprocess
import os
import signal
import psutil
from shlex import split
import datetime
import multiprocessing
import client_record2db
import uuid

numberCanal = 1
date_start0 = datetime.datetime.now()
date_start = datetime.datetime.now()
date_end = datetime.datetime.now()
filePath = "C:/Users/praktika/PycharmProjects/video_record_permyakova/web/video/"
filePath2 = "http://192.168.35.96:1235/"
number = 0
flag = True

perem = 0
q = multiprocessing.Value('i',0)
current_pid = 0
flashok = 1

app = Flask('record', static_url_path='', static_folder='web/video')
# Flask-JSONRPC
jsonrpc = JSONRPC(app, '/api_record', enable_web_browsable_api=True)


@jsonrpc.method('launch_start')
def launch_start():
    global number, flag
    number = 0
    flag = True
    pr1 = threading.Thread(target = launch)
    pr1.start()


@jsonrpc.method('echo')
def echo(message: str) -> str:
    return message

@jsonrpc.method('launch_end')
def launch_end():
    global perem, flag, current_pid

    flag = False
    #print("stop flag = ", flag)
    try:
       # print(current_pid)
        os.kill(current_pid, signal.SIGINT)
    except Exception:
        pass
    stop_recording()


def launch():
    global frame
    global proces
    global flag
    while (flag):
       # print("while flag = ", flag)
        start_recording()
        stop_recording()


def handler(signum, frame):
    print("CTRL+C")

def start_recording():
    global date_start
    global date_start0
    global filePath
    global number
    global perem
    global date_end
    global current_pid

    number += 1
    date_start0 = datetime.datetime.now()
    date_start = datetime.datetime.now()
    date_start = str(date_start).partition('.')[0]
    date_start = date_start.replace(':', '_')
    date_start = date_start.replace(' ', '_time_')
    date_start1 = str(filePath + date_start + ".mkv")
    date_start11 = str(filePath + date_start + ".mp4")
    scrin = str(filePath + "frame_" + date_start + ".jpg")
    cmd = f"ffmpeg -y -i '{'rtsp://root:12345678@192.168.35.202/axis-media/media.amp?videocodec=H264&resolution=1024x768&compression=30&fps=30&videokeyframeinterval=30&event=on'}' -acodec copy -vcodec copy {date_start1}"
    proc = subprocess.Popen(split(cmd))
    current_pid = proc.pid
    #print(current_pid)
    try:
        time.sleep(5)
        rtspUrl = "rtsp://root:12345678@192.168.35.202/axis-media/media.amp?videocodec=H264&resolution=1024x768&compression=30&fps=30&videokeyframeinterval=30&event=on"
        frame = cv2.VideoCapture(rtspUrl)
        status, image = frame.read()
        save_frame(image)
        proc.communicate(timeout=25)

    except BaseException as e:
        try:
            proc.kill()
            cmd2 = f"ffmpeg -i {date_start1} -vcodec copy -acodec copy {date_start11}"
          #  print("cmd2: ", cmd2)
            proc2 = subprocess.Popen(shlex.split(cmd2))
            proc2.communicate()
            os.remove(date_start1)
        except BaseException as e:
            pass

def stop_recording():
    global date_start
    global date_start0
    global date_end
    global number
    global flag
    global filePath2

    date_end = datetime.datetime.now()
    id = str(uuid.uuid4())
    client_record2db.insert_into_db(1, 'auth', id, str(filePath2+date_start+".mp4"), date_start0, date_end, size_record(), 'mp4', str(filePath2+"frame_"+date_start+ ".jpg"))



def size_record():
    global filePath
    global date_start
    size_video = str(filePath + date_start + '.mp4')
    if (os.path.exists(size_video)):
        s = round((os.path.getsize(size_video) / (1024*2)), 2)
    else:
        s = 0
   # print('File size:', s, 'bytes')
    return s


def save_frame(img):
    global number
    global date_start
    cv2.imwrite(filePath + "frame_" + date_start + ".jpg", img)


def kill(proc_pid):
    process = psutil.Process(proc_pid)
    for proc in process.children(recursive=True):
        proc.kill()
    process.kill()

if __name__ == "__main__":
    try:
        #signal.signal(signal.CTRL_C_EVENT, handler)
        signal.signal(signal.SIGINT, handler)
        app.run(port=1235, host='0.0.0.0')
    except BaseException as e:
        t = True