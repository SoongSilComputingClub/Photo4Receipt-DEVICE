import pygame
import cv2
import time

import hashlib
import requests
from escpos.printer import Usb
import qrcode

import numpy as np
from PIL import Image, ImageEnhance

from util import imageCombine, qrGenerate, saturate_contrast2
from qr import QR
# import Qr

HOST_URL = 'http://146.56.106.142/'


pygame.init()
SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 1000
# surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.NOFRAME)
# surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.NOFRAME)
# surface = pygame.display.set_mode((480*2, 320*2))
surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

class ImgObject:
    def __init__(self, path, size):
        self.__img = pygame.image.load(path)
        self.__size = size
        self.__x, self.__y = self.__img.get_size()

    def get_image(self):
        return pygame.transform.scale(self.__img, (self.__x * self.__size, self.__y * self.__size))


BMO_TIMER_INIT = 15 * 10
TAKE_TIMER_INIT = 10 * 10

class BMO_generator:
    def __init__(self):
        self.timer = BMO_TIMER_INIT
        self.__emotion = {
            "open": ImgObject("./img/bmo_animation/emotion_0.png", 1.25),
            "close_1": ImgObject("./img/bmo_animation/emotion_1.png", 1.25),
            "close_2": ImgObject("./img/bmo_animation/emotion_2.png", 1.25),
            "close": ImgObject("./img/bmo_animation/emotion_3.png", 1.25),
        }

    def next(self):
        self.timer -= 1
        if self.timer <= 0: self.timer = BMO_TIMER_INIT
        if self.timer == 4: return self.__emotion["close_1"].get_image()
        elif self.timer == 3: return self.__emotion["close_2"].get_image()
        elif self.timer == 2: return self.__emotion["close"].get_image()
        elif self.timer == 1: return self.__emotion["close_1"].get_image()
        return self.__emotion["open"].get_image()



class Cam_Object:
    def __init__(self, frame):
        self.__frame = frame
        self.__size = 1

    def setFrame(self, frame):
        self.__frame = frame

    def getImage(self):
        image = pygame.image.frombuffer(self.__frame.tobytes(), self.__frame.shape[1::-1], "BGR")
        dx, dy = map(lambda x: int(self.__size * x), image.get_size())
        image = pygame.transform.scale(image, (dx, dy))
        image = pygame.transform.flip(image, True, False)
        return image

    def setSize(self, size: float):
        self.__size = size

####################
#       Init       #
####################


# qr code init
qr = QR(HOST_URL)

# camera init
Camera = Cam_Object(None)
Camera.setSize(2.1)
webcam = cv2.VideoCapture(0)
timer = 0






img_saved = []


# time timer init
font1 = pygame.font.SysFont(None, 500)

# BMO animation setting
BMO = BMO_generator()

p = Usb(0x1fc9, 0x2016, in_ep=0x81, out_ep=0x01)



running = True

while running:

    status, frame = webcam.read()
    Camera.setFrame(frame)

    # Key pressed
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE: # SPACE : 사진 찍기
                timer = 5 * 10
            elif event.key == pygame.K_ESCAPE: # ESC : BMO 닫기
                running = False
                break

    # 다음 screen까지 딜레이
    pygame.time.delay(10)
    surface.blit(BMO.next(), (0, 0))


    # 타이머 0 이상일 시 ( 타이머 돌고 있을 경우 )
    if timer > 0:
        timer -= 1

        surface.blit(Camera.getImage(), (0, 0))

        if timer == 0: # 사진 찍혔을 때
            if len(img_saved) <= 3:
                surface.fill((255, 255, 255))
                pygame.display.flip()
		
                main_frame = imageCombine(f'./img/frames/mario/mario_0{len(img_saved) + 1}.png', frame, len(img_saved) + 1)
                img_saved.append(main_frame)

                pygame.time.delay(50)

                timer = 5 * 10

                if len(img_saved) == 4:
                    timer = 1

            else: # img_saved

                # hashing
                hash_object = hashlib.sha256(f"{time.time_ns()}".encode())
                filename = hash_object.hexdigest()[:20]
                
                # directory name define
                FILE_DIRECTORY = './img/capture/' + filename + '.png'

                with open(".last", "w") as f:
                    f.write(FILE_DIRECTORY)

                # # IMG SAVE
                # main_frame = imageCombine(f'./img/frames/mario/mario_0{i}.png', frame, i)
                # img_saved.append(main_frame)
                # img_saved.append(cv2.imread('./img/sscc.jpg'))

                main_frame = cv2.vconcat(img_saved)


                cv2.imwrite(FILE_DIRECTORY, main_frame)
                print(FILE_DIRECTORY)

                # # IMG UPLOAD
                # with open(FILE_DIRECTORY, 'rb') as f:
                #    res = requests.post(HOST_URL+"uploadfile/", files = {'file': f})
                #    if res.status_code == 200:
                #        print(res.status_code, "Image Upload Success")
                #    else:
                #        print(res.status_code, "Error Occured")


                # print
                p.set(font="a", height=2, align="center")

                for img_t in img_saved:
                    color_coverted = cv2.cvtColor(img_t, cv2.COLOR_BGR2RGB)
                    # i = Image.fromarray(color_coverted)
                    # gd = ImageEnhance.Brightness(pil_image)
                    # i = gd.enhance(0.5)
                    p.image(Image.fromarray(color_coverted), fragment_height=3)

                img_saved = []

                # QR
                footer = qr.get_with_logo(HOST_URL+"images/"+filename)
                p.image(footer, fragment_height=3)

                # finish
                p.cut()


        else:
            img1 = font1.render(f'{timer // 10}', True, (255, 255, 255))
            surface.blit(img1, (SCREEN_WIDTH // 2 - 125, SCREEN_HEIGHT // 2 - 125))

    pygame.display.flip()



pygame.quit()
