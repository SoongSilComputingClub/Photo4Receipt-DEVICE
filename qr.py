import qrcode
from PIL import Image

class QR:
    """
    A class for generating QR codes with an optional embedded logo.
    
    Attributes:
        url (str): The base URL or text for the QR code.
    
    Methods:
        make(addr): Generates a QR code for the given address.
        get_with_logo(addr): Generates a QR code with an embedded logo for the given address.
    """
    def __init__(self, url):
        self.url = url
        self.generator = qrcode.QRCode(version=1, box_size=3, border=5)

    def make(self, addr):
        """
        Generates a QR code for a given address.
        
        Parameters:
            addr (str): The address to encode in the QR code.
        
        Returns:
            PIL.Image.Image: The generated QR code as a PIL image.
        """
        self.generator.clear()
        self.generator.add_data(addr)
        self.generator.make(fit=True)
        img = self.generator.make_image(fill_color="black", back_color="white")
        return img.get_image().resize((128, 128))

    def get_with_logo(self, addr):
        """
        Generates a QR code for a given address and embeds a logo at its center.
        
        Parameters:
            addr (str): The address to encode in the QR code.
        
        Returns:
            PIL.Image.Image: The generated QR code with an embedded logo as a PIL image.
        """
        qr_img = self.make(addr)
        logo = Image.open('./image/frames/logo/sscc.jpg')  # Ensure this path points to the logo image
        logo.paste(qr_img, box=(512-128-10, 0))
        return qr_img

if __name__ == "__main__":
    qrMaker = QR('http://example.com')
    qr_img_with_logo = qrMaker.get_with_logo('http://example.com/somepath')
    qr_img_with_logo.show()
