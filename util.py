import cv2
import qrcode 
from PIL import Image, ImageEnhance
import numpy as np
from escpos.printer import Usb


def imageCombine(frame_path, image, index):
    # 공백 프레임 가져오기
    main_frame = cv2.imread('./img/frames/bin.png')

    # 프레임 이미지 생성
    frame = cv2.imread(frame_path, cv2.IMREAD_UNCHANGED)
    # frame = cv2.add(frame, 100)

    # 프레임 마스크 생성
    _, mask = cv2.threshold(frame[:,:,3], 0, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)
    mask_inv = cv2.bitwise_not(mask_inv)
    
    # 영상 스크린샷 사이즈 조절
    # image = saturate_contrast2(image, 2)
    dst = cv2.resize(image, dsize=(640 // 2, 480 // 2), interpolation=cv2.INTER_AREA)
    # br = ImageEnhance.Brightness(dst)
    # dst = br.enhance(1.5)
    # dst = cv2.add(dst, 100)

    if index % 2 == 0:
        main_frame[0:240, 160:480] = dst
    else:
        main_frame[0:240, 0:320] = dst

    framed = cv2.bitwise_and(frame, frame, mask_inv)[:, :, :3]
    main_frame[mask_inv > 0] = framed[mask_inv > 0]

    return main_frame


def qrGenerate(url, id):
    qrimg = cv2.imread('./img/sscc.jpg')
    qr = qrcode.QRCode(version=1, box_size=3, border=5)

    qr.add_data(url+"images/"+id)
    qr.make(fit=True)

    qr_temp = qr.make_image(fill_color = "black", back_color="white")
    qr_temp.save('./img/qr.jpg')
    qr_img = cv2.imread('./img/qr.jpg')

    qrimg[0:128, 384:512] = qr_img[0:128, 0:128]


    # print(qr_img)
    cv2.imwrite("img/temp.jpg", qrimg)
    return

def saturate_contrast2(p, num):
    pic = p.copy()
    pic = pic.astype('int32')
    pic = np.clip(pic+(pic-128)*num, 0, 255)
    pic = pic.astype('uint8')
    return pic


def serial_print(target):
    p = Usb(0x1fc9, 0x2016, in_ep=0x81, out_ep=0x01)
    try:
        p.set(font="a", height=2, align="center")
        p.image(target, fragment_height=3)
    except:
        ...

def serial_cut():
    p = Usb(0x1fc9, 0x2016, in_ep=0x81, out_ep=0x01)
    try:
        p.cut()
    except:
        ...