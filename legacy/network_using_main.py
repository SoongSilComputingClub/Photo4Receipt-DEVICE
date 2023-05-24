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

url = 'http://146.56.106.142/'


pygame.init()
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 1000
# surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.NOFRAME)
# surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.NOFRAME)
surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)


class BmoEmotion:
    def __init__(self, path):
        self.__image = pygame.image.load(path)

    def getImage(self):
        return self.__image

    def setSize(self, size):
        dx, dy = map(lambda x: int(size * x), self.__image.get_size())
        self.__image = pygame.transform.scale(self.__image, (dx, dy))



class CamImage:
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



emotion_animation = {
    "open" : BmoEmotion("./img/bmo_animation/emotion_0.png"),
    "close_1" : BmoEmotion("./img/bmo_animation/emotion_1.png"),
    "close_2" : BmoEmotion("./img/bmo_animation/emotion_2.png"),
    "close": BmoEmotion("./img/bmo_animation/emotion_3.png"),
}

EMOTION_INIT = {
    3: "close_1",
    2: "close_2",
    1: "close",
    -1: "open",
}

Camera = CamImage("")
Camera.setSize(2.1)

for key in emotion_animation.keys():
    emotion_animation[key].setSize(1.25)


webcam = cv2.VideoCapture(0)

timer = 0
EYE_COUNT_INIT = 100
eye_count = EYE_COUNT_INIT

running = True



img_saved = []

font1 = pygame.font.SysFont(None, 500)


while running:
    status, frame = webcam.read()
    Camera.setFrame(frame)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                timer = 5 * 10
                # print("스페이스바")
            elif event.key == pygame.K_ESCAPE:
                running = False
                break
    pygame.time.delay(10)
    eye_count -= 1

    surface.blit(emotion_animation["open"].getImage(), (0, 0))

    if eye_count < 0:
        eye_count = EYE_COUNT_INIT
    # elif eye_count in EMOTION_INIT.keys():
    #     surface.blit(emotion_animation[EMOTION_INIT[eye_count]].getImage(), (0, 0))
    #
    elif eye_count == 3:
        surface.blit(emotion_animation["close_1"].getImage(), (0, 0))
    elif eye_count == 2:
        surface.blit(emotion_animation["close_2"].getImage(), (0, 0))
    elif eye_count == 1:
        surface.blit(emotion_animation["close"].getImage(), (0, 0))
    
    # print(eye_count)

    if timer > 0:
        timer -= 1
        surface.blit(Camera.getImage(), (0, 0))



        if timer == 0:
            # print(len(img_saved))
            if len(img_saved) <= 3:
                surface.fill((255, 255, 255))
                pygame.display.flip()
                main_frame = imageCombine(f'./img/frames/mario/mario_0{len(img_saved) + 1}.png', frame, len(img_saved) + 1)
                
                img_saved.append(main_frame)
                
                pygame.time.delay(50)
                timer = 5 * 10
                if len(img_saved) == 4:
                    timer = 1
                # continue
            else:
                
                # img_saved
                # HASH
                hash_object = hashlib.sha256(f"{time.time_ns()}".encode())
                filename = hash_object.hexdigest()[:20]
                file_directory = './img/capture/'+filename+'.png'

                with open(".last", "w") as f:
                    f.write(file_directory)
                # IMG SAVE
                # 



                # main_frame = imageCombine(f'./img/frames/mario/mario_0{i}.png', frame, i)
                # img_saved.append(main_frame)


                # img_saved.append(cv2.imread('./img/sscc.jpg'))

                main_frame = cv2.vconcat(img_saved)
                

                cv2.imwrite(file_directory, main_frame)
                print(file_directory)

                # IMG UPLOAD
                with open(file_directory, 'rb') as f:
                    res = requests.post(url+"uploadfile/", files = {'file': f})
                    if res.status_code == 200:
                        print(res.status_code, "Image Upload Success")
                    else:
                        print(res.status_code, "Error Occured")
                # PRINT
                p = Usb(0x1fc9, 0x2016, in_ep=0x81, out_ep=0x01)
                
                p.set(font="a", height=2, align="center")
                # p.text("SoongSil\n")
                # p.set(font="b", height=2, align="center")
                # p.text("Computing Club\n\n")


                for img_t in img_saved:
                    color_coverted = cv2.cvtColor(img_t, cv2.COLOR_BGR2RGB)
                    # convert from openCV2 to PIL
                    pil_image=Image.fromarray(color_coverted)
                    gd = ImageEnhance.Brightness(pil_image)
                    i = gd.enhance(1.5)
                    p.image(i, fragment_height=3)

                
                img_saved = []
                # QR
                # qrGenerate(url, filename)
                qrimg = cv2.imread('./img/sscc.jpg')




                qr = qrcode.QRCode(version=1, box_size=3, border=5)
                
                qr.add_data(url+"images/"+filename)
                qr.make(fit=True)
                qr_temp = qr.make_image(fill_color = "black", back_color="white")
                qr_temp.save('./img/qr.jpg')
                qr_img = cv2.imread('./img/qr.jpg')

                # qrimg[0:128, 0:128] = qr_img[0:128, 0:128]
                qrimg[0:128, 384:512] = qr_img[0:128, 0:128]
                # qrimg.save('./img/temp.png')

                # print(qr_img)
                cv2.imwrite("img/temp.jpg", qrimg)
                p.image("img/temp.jpg", fragment_height=3)
                # p.image("img/sscc.jpg", fragment_height=3)
                
                
                # p.image('./img/qr.png', fragment_height=3)
                p.cut()
                # p.text("\n" * 10)
                # p.cut()


        else:
            img1 = font1.render(f'{timer // 10}', True, (255, 255, 255))
            surface.blit(img1, (SCREEN_WIDTH // 2 - 125, SCREEN_HEIGHT // 2 - 125))


    # else:
    #     surface.blit(emotion_animation["open"].getImage(), (0, 0))




    pygame.display.flip()

pygame.quit()
