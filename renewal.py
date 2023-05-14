import pygame
import cv2
import time

import hashlib
import requests

from escpos.printer import Usb
import qrcode

url = 'http://146.56.106.142/'


pygame.init()
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 1000
surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.NOFRAME)
#
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
        # return self.__image
        image = pygame.image.frombuffer(self.__frame.tobytes(), self.__frame.shape[1::-1], "BGR")
        dx, dy = map(lambda x: int(self.__size * x), image.get_size())
        # image =
        return pygame.transform.scale(image, (dx, dy))

    def setSize(self, size: float):
        self.__size = size



emotion_animation = {
    "open" : BmoEmotion("./img/bmo_animation/emotion_0.png"),
    "close_1" : BmoEmotion("./img/bmo_animation/emotion_1.png"),
    "close_2" : BmoEmotion("./img/bmo_animation/emotion_2.png"),
    "close": BmoEmotion("./img/bmo_animation/emotion_3.png"),
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





font1 = pygame.font.SysFont(None, 500)


while running:
    status, frame = webcam.read()
    Camera.setFrame(frame)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                timer = 5 * 10
                print("스페이스바")
            elif event.key == pygame.K_ESCAPE:
                running = False
                break
    pygame.time.delay(10)
    eye_count -= 1


    if eye_count < 0:
        eye_count = EYE_COUNT_INIT
    elif eye_count == 3:
        surface.blit(emotion_animation["close_1"].getImage(), (0, 0))
    elif eye_count == 2:
        surface.blit(emotion_animation["close_2"].getImage(), (0, 0))
    elif eye_count == 1:
        surface.blit(emotion_animation["close"].getImage(), (0, 0))


    if timer > 0:
        timer -= 1
        surface.blit(Camera.getImage(), (0, 0))



        if timer == 0:
            # HASH
            hash_object = hashlib.sha256(time.time_ns.encode())
            filename = hash_object.hexdigest()[:20]
            # IMG SAVE
            cv2.imwrite(f'./img/capture/{filename}.png', frame)

            # IMG UPLOAD
            with open(filename, 'rb') as f:
                res = requests.post(url+"uploadfile/", files = {'file': f})
                if res.status_code == 200:
                    print(res.status_code, "Image Upload Success")
                else:
                    print(res.status_code, "Error Occured")
            # PRINT
            p = Usb(0x1fc9, 0x2016, in_ep=0x81, out_ep=0x01)

            p.set(font="a", height=2, align="center")
            p.text("SoongSil\n")
            p.set(font="b", height=2, align="center")
            p.text("Computing Club\n\n")
            p.image(filename, fragment_height=3)
            p.image("sscc.jpg", fragment_height=3)
            p.qr(url+"images/"+filename)
            p.cut()
            p.text("\n" * 10)
            p.cut()



        else:
            img1 = font1.render(f'{timer // 10}', True, (255, 255, 255))
            surface.blit(img1, (SCREEN_WIDTH // 2 - 125, SCREEN_HEIGHT // 2 - 125))


    else:
        surface.blit(emotion_animation["open"].getImage(), (0, 0))




    pygame.display.flip()

pygame.quit()
