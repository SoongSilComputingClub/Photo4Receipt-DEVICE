from escpos.printer import Usb
import cv2
import numpy as np
from PIL import Image

p = Usb(0x1fc9, 0x2016, in_ep=0x81, out_ep=0x01)

#src = cv2.imread("person.jpg", cv2.IMREAD_COLOR)
#dst = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

src = cv2.imread('person.jpg', cv2.IMREAD_GRAYSCALE)
dst = cv2.normalize(src, None, 0, 255, cv2.NORM_MINMAX)
#x = np.array(dst)
img_2 = Image.fromarray(dst) 

p.set(font="a", height=2, align="center")
p.text("SoongSil\n")
p.set(font="b", height=2, align="center")
p.text("Computing Club\n")
p.image(img_2, fragment_height=3)
p.cut()
p.text("\n"*10)
p.cut()