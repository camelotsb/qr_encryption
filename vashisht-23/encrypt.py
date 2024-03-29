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

cipher1 = AESCipher('Va$hi$ht.TECH#@f')
decrypted = cipher1.decrypt(b'iukyZmekrzYcFWhAPobFpjLAvED9WEaC2Xn5CL+Fbtt6PaOyGlRDzixI2CmzU' )

# encrypted2=cipher2.encrypt('notasecret')
# decrypted2=cipher2.decrypt(encrypted)
print(decrypted)
# print(encrypted2)
# print(decrypted2)