from escpos import printer
import cv2
import numpy as np
from PIL import Image


src = cv2.imread("Lenna.jpg", cv2.IMREAD_COLOR)
dst = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
x = np.array(dst)
img_2 = Image.fromarray(x) 
# We use Dummy printer to pre-process commands
dummy = printer.Dummy('POS-5890')  # Automatic selection of the charcode thanks to the profile, if fails then set the charcode CP860 manually
dummy.hw('init')
dummy.set(height=2, width=2)
dummy.text("SoongSil Computing Club\n")
dummy.image(img_2)
dummy.cut()

# Then we send the raw output to the real printer
#p = printer.File(devfile='/bus/usb/003/032')
p = printer.File(devfile='/dev/printer')
#p = printer.Usb(0x1fc9, 0x2016, timeout=10, in_ep=0x81, out_ep=0x01)
p._raw(dummy.output)