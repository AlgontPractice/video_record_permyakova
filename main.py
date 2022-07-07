import glob
import shutil

import ffmpeg
import cv2
import os
from PIL import Image, ImageEnhance
import numpy as np
import datetime
import db_record
#import glob
#import shutil
#import moviepy.editor as mpy

isRecord = False
out = None
number = 0
numberCanal=1
#VideoDir = 'video' #директория для записи кадров
record_icon_img = cv2.imread('icon.png', cv2.IMREAD_UNCHANGED)
record_icon = Image.fromarray(record_icon_img)
date_start=datetime.datetime.now()
date_end=datetime.datetime.now()

rtspUrl = "rtsp://root:12345678@192.168.35.202/axis-media/media.amp?videocodec=H264&resolution=1024x768&compression=30&fps=30&videokeyframeinterval=30&event=on"
filePath= "C:/Users/praktika/PycharmProjects/video/"
frame = cv2.VideoCapture(rtspUrl)
if (frame.isOpened ()):
	print("Open camera!")
else:
     print("Fail to open camera!")


def start_recording():
    global out
    global number
    global date_start
    #Получаем размеры видео, которое идет с камеры
    frame_width = int(frame.get(3))
    frame_height = int(frame.get(4))
    print("start")
    f=open("name.txt")
    file_name  = f.read()
    number  = int(file_name)
    out = cv2.VideoWriter(filePath + 'Video_' + file_name + '.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 20, (frame_width, frame_height), True)
    f.close()
    date_start = datetime.datetime.now()


def stop_recording():
   global out
   global number
   global date_end
   global date_start
   out.release()
   print(number)
   f=open("name.txt", 'w')
   number +=1
   number1 =str(number)
   f.write(number1)
   f.close()
   date_end = datetime.datetime.now()


def save_frame(img):
    global number
    cv2.imwrite(filePath+ "frame%d.jpg" % number, img)
    return str(filePath+ "frame%d.jpg" % number)


def size_record():
    global number
    size_video = str(filePath+'/Video_'+str(number-1)+'.avi')
    s=os.path.getsize(size_video)
    print('File size:', s, 'bytes')
    return s


def add_record(img):
    #Переводим массив изображения в объект Pillow и преобразуем в тип RGBA с маской прозрачности
    img_out=Image.fromarray(img)
    img_out.paste(record_icon, (0, 50))
    return np.asarray(img_out, dtype='uint8')

########################################################################

while (True):
    status, image = frame.read()

    if isRecord:
       # save_frame(image)
        out.write(image)
        image = add_record(image)

    cv2.imshow("Hidden camera", image)
    k = cv2.waitKey(30)
    #r
    if k == 114:
        if not isRecord:
            start_recording()
            save_frame(image)
            isRecord = True
        else:
            stop_recording()
            size_record()
            db_record.insert_record(numberCanal, "user", number - 1, str(filePath + '/Video_' + str(number - 1) + '.avi'), date_start, date_end, size_record(), 'avi', save_frame())
            isRecord = False

    if k == 27:
        break

frame.release()
cv2.destroyAllWindows()