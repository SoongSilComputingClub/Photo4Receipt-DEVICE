"""
This module defines a QR class for generating QR codes with an optional logo.
The QR class utilizes the `qrcode` library to generate QR codes and the `PIL` (Python Imaging Library) for image manipulation.
It allows for creating QR codes from a given URL or text and optionally embedding a logo into the generated QR code image.

Attributes:
    __url (str): The base URL or text to be encoded into the QR code.
    __generator (qrcode.QRCode): The QR code generator instance from the `qrcode` library, configured with specific parameters.

Methods:
    make(addr): Generates a QR code image from the given address (URL or text) and returns it as a PIL Image object.
    get_with_logo(addr): Generates a QR code with the specified address (URL or text) and embeds a predefined logo into the QR code image.

Example:
    qrMaker = QR('http://example.com')
    qrWithLogo = qrMaker.get_with_logo('http://example.com/path')
    qrWithLogo.show()
"""
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
