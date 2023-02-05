import qrcode
from PIL import Image

from hashlib import sha256
import base64
from Crypto import Random
from Crypto.Cipher import AES

BS = 16
pad = lambda s: bytes(s + (BS - len(s) % BS) * chr(BS - len(s) % BS), 'utf-8')
unpad = lambda s : s[0:-ord(s[-1:])]

class AESCipher:

    def __init__( self, key ):
        self.key = bytes(key, 'utf-8')

    def encrypt( self, raw ):
        raw = pad(raw)
        iv = Random.new().read( AES.block_size )
        cipher = AES.new(self.key, AES.MODE_CBC, iv )
        return base64.b64encode( iv + cipher.encrypt( raw ) )

    def decrypt( self, enc ):
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv )
        return unpad(cipher.decrypt( enc[16:] )).decode('utf8')

cipher = AESCipher('Va$hi$ht.TECH#@f')


# encrypted2=cipher2.encrypt('notasecret')
# decrypted2=cipher2.decrypt(encrypted)

# print(encrypted2)
# print(decrypted2)

def generate_qr(data):
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=3
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img

def paste_qr_on_ticket(qr_img, ticket_img):
    qr_img = qr_img.resize((263, 263))
    ticket_img.paste(qr_img, (923, 134))
    print(ticket_img.size)
    return ticket_img


for i in range(1,501):

    qr_message= "vashisht'23 pass"+str(i)
    encrypted = cipher.encrypt(qr_message)
    decrypted = cipher.decrypt(encrypted)

    print(encrypted)
    print(decrypted,"\n")

    ticket_img = Image.open("ticket.jpg")
    data = encrypted
    qr_img = generate_qr(data)
    ticket_with_qr = paste_qr_on_ticket(qr_img, ticket_img)
    ticket_name=qr_message+".png"
    ticket_with_qr.save(ticket_name)