import cv2
import qrcode
from PIL import Image

class QR:
    def __init__(self, url):
        self.__url = url
        self.__generator = qrcode.QRCode(version=1, box_size=3, border=5)

    def make(self, addr):
        self.__generator = qrcode.QRCode(version=1, box_size=3, border=5)
        self.__generator.add_data(addr)
        self.__generator.make(fit=True)
        img = self.__generator.make_image(fill_color="black", back_color="white")
        img = img.get_image().resize((128, 128))
        return img

    def get_with_logo(self, addr):
        logo = Image.open('./img/sscc.jpg')
        qr = self.make(addr)
        logo.paste(qr, box=(512-128-10, 0))
        return logo

if __name__ == "__main__":
    qrMaker = QR('')
    qrMaker.get_with_logo('1234').show()