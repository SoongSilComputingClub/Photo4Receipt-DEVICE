from escpos import printer, image
import time
import numpy as np
from PIL import Image
import cv2

p = printer.Usb(0x1fc9, 0x2016, in_ep=0x81, out_ep=0x01)

# cv2 
src = cv2.imread("person.jpg", cv2.IMREAD_COLOR)
resized_src = cv2.resize(src, (500, 500))
dst = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

x = np.array(dst)
print(x.shape)

each_num = np.array([])
tmp = 0
for test in x:
    flat = test.flatten()
    print(flat.shape)
    each_num = np.append(each_num, flat)
    tmp+=1
    if tmp == 50:
        print(each_num.shape)
        print(each_num)
        resized = each_num.reshape(50,500)
        img_2 = Image.fromarray(resized) # NumPy array to PIL image
        p.line_spacing(spacing=None, divisor=0)
        p.set(font="a", height=2, align="center")
        p.image(img_2)
        each_num = np.array([])
        tmp = 0
        time.sleep(1)
p.cut()