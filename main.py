<<<<<<< HEAD
# https://naemo-naemo.tistory.com/68
import threading
import time
import tkinter
import cv2
import PIL.Image, PIL.ImageTk

class App:
    global shot_timer
    def __init__(self, window, window_title, video_source=0):
        # Tkinter 기본 설정
        self.photo = None
        self.window = window
        self.window.title(window_title)  # 타이틀 설정
        self.window.attributes('-fullscreen', True)  # 전체 화면 설정
        self.video_source = video_source  # 웹캠 = 0
        self.scale = 2.5  # 이미지 배율

        self.vid = MyVideoCapture(self.video_source, self.scale)  # 웹캠 가져오기

        # 웹캠 화면 그리는 캔버스
        self.canvas = tkinter.Canvas(window, width=self.vid.width, height=self.vid.height)
        self.canvas.pack()
        # 플래쉬 타이밍 변수
        self.shot_cnt = 13


        # 영상 FPS 설정
        self.fps = self.vid.webcam.get(cv2.CAP_PROP_FPS)
        self.delay = round(1000.0 / self.fps)
        self.update()

        # 문제의 쓰레드...
        self.window.mainloop()

    def update(self):  # 웹캠 화면 업데이트
        global shot_timer
        ret, frame = self.vid.get_frame()
        if ret:

            if shot_timer == 0:
                print("0 감지\n" * 100)

                shot_timer=-1

            #     ret, frame = self.vid.get_frame()
            #     if ret:
                array = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    
                img = PIL.Image.fromarray(array)
                # img.show()      
            #         # img 변수에 저장되어 있는데 활용방법을...
                
                img = img.resize((500,375))

                p.set(font="a", height=2, align="center")
                p.text("SoongSil\n")
                p.set(font="b", height=2, align="center")
                p.text("Computing Club\n\n")
                p.image(img, fragment_height=3)
                p.image("sscc.jpg", fragment_height=3)
                p.cut()
                p.text("\n"*10)
                p.cut()
            #         return

            # elif shot_timer > 0:
            if shot_timer > 0:
                print("감지됨", shot_timer)
                

                # array = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                array = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                if shot_timer == 1:
                    self.shot_cnt -= 1
                    if 1 < self.shot_cnt < 5:
                        array.fill(255)

                img = PIL.Image.fromarray(array)
                img = img.resize((int(img.width * self.scale), int(img.height * self.scale)))


                self.photo = PIL.ImageTk.PhotoImage(image=img)
                self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)
            else:
                self.photo = tkinter.PhotoImage(file="img/bmo.png")
                self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)
        self.window.after(self.delay, self.update)



class MyVideoCapture:
    def __init__(self, video_source=0, scale=1.0):
        self.webcam = cv2.VideoCapture(video_source)  # 웹캠에서 영상을 가져오게 설정
        self.scale = scale  # 이미지 배율
        if not self.webcam.isOpened():  # 웹캠이 꺼져있으면 강제 종료 ( error )
            raise ValueError("Unable to open video source", video_source)
        self.width = self.webcam.get(cv2.CAP_PROP_FRAME_WIDTH) * self.scale
        self.height = self.webcam.get(cv2.CAP_PROP_FRAME_HEIGHT) * self.scale

    def get_frame(self):
        if self.webcam.isOpened():
            ret, frame = self.webcam.read()
            if ret:
                frame = cv2.flip(frame, 1)
                return (ret, frame)
            else:
                return (ret, None)
        else:
            return (False, None)

    def __del__(self):
        if self.webcam.isOpened():
            self.webcam.release()

from serial import Serial

ser = Serial("/dev/ttyUSB0", 9600)

def isPressButton():
    global shot_timer, reset_shot_timer
    tmp_bin = 1
    # cnt = 0
    while True:
        if ser.readable():
            res = ser.readline()
            # print(res.decode()[:len(res)-1])
            if "1" in res.decode()[:len(res)-1] and shot_timer < 0:
                shot_timer = 5
                print("굳")
        print("MAIN THREAD", shot_timer)
        # if GPIO.input(button_pin) == GPIO.HIGH and shot_timer == 0:
        if shot_timer == -1 or shot_timer == 0:
            continue
        # print(shot_timer)
        tmp_bin += 1
        if tmp_bin > 10:
            shot_timer -= 1
            tmp_bin = 1
        time.sleep(0.1)
        
        # print(shot_timer, tmp_bin)
        # if shot_timer == 0:
        #     tmp_bin += 1
        #     if tmp_bin == 10 * 10:
        #         print(tmp_bin)
        #         shot_timer = reset_shot_timer
        #         cnt = 0
        #         tmp_bin = 0

        # if shot_timer == 0:
        #     continue

        # cnt += 1
        # if cnt == 10:
        #     shot_timer -= 1
        #     cnt = 1
        # time.sleep(0.1)


# import RPi.GPIO as GPIO
import time
from escpos.printer import Usb
import cv2
import numpy as np
from PIL import Image

time.sleep(10)
print("GOING")
p = Usb(0x1fc9, 0x2016, in_ep=0x81, out_ep=0x01)

#src = cv2.imread("person.jpg", cv2.IMREAD_COLOR)
#dst = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)



# button_pin = 15
# GPIO.setwarnings(False)
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# while True:
#     if GPIO.input(button_pin)==GPIO.HIGH:
#         print("button pushed")
#         time.sleep(0.1)

reset_shot_timer = 5

shot_timer = -1

thread = threading.Thread(target=isPressButton, args=())
thread.daemon = True
thread.start()

gui = None
gui = App(tkinter.Tk(), "BMO SCREEN")
=======
from utils import getImage, getAA_01

def main():
    # RESIZE_RATE * 100 = PERSENT
    RESIZE_RATE = 0.2  # 원본의 20% (축소)

    img, HEI, WID = getImage('./img/lena.png', RESIZE_RATE)

    for h in range(HEI):
        for w in range(WID):
            print(getAA_01(img[h][w]), end="")
        print()

if __name__ == '__main__':
    main()
>>>>>>> 0ba43dc12f06184d5078c144a0e7484663649dd1
