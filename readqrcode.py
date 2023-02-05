
from __future__ import print_function

import pyzbar.pyzbar as pyzbar
import numpy as np
import cv2
import time


import base64
import qrcode
import hashlib
from Crypto.Cipher import AES
from Crypto import Random

BLOCK_SIZE = 16
def pad(s): return s + (BLOCK_SIZE - len(s) %
                        BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)


def unpad(s): return s[:-ord(s[len(s) - 1:])]


def decrypt(enc, password):
    private_key = hashlib.sha256(password.encode("utf-8")).digest()
    enc = base64.b64decode(enc)
    iv = enc[:16]
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(enc[16:]))




# get the webcam:
cap = cv2.VideoCapture(0)

cap.set(3, 640)
cap.set(4, 480)
# 160.0 x 120.0
# 176.0 x 144.0
# 320.0 x 240.0
# 352.0 x 288.0
# 640.0 x 480.0
# 1024.0 x 768.0
# 1280.0 x 1024.0
time.sleep(2)


def decode(im):
    # Find barcodes and QR codes
    decodedObjects = pyzbar.decode(im)
    # Print results
    # for obj in decodedObjects:
        # print('Type : ', obj.type)
        # print('Data : ', obj.data, '\n')
    return decodedObjects


font = cv2.FONT_HERSHEY_SIMPLEX

while (cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()
    # Our operations on the frame come here
    im = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    decodedObjects = decode(im)

    for decodedObject in decodedObjects:
        points = decodedObject.polygon

        # If the points do not form a quad, find convex hull
        if len(points) > 4:
          hull = cv2.convexHull(
              np.array([point for point in points], dtype=np.float32))
          hull = list(map(tuple, np.squeeze(hull)))
        else:
          hull = points

        # Number of points in the convex hull
        n = len(hull)
        # Draw the convext hull
        for j in range(0, n):
          cv2.line(frame, hull[j], hull[(j+1) % n], (255, 0, 0), 3)

        x = decodedObject.rect.left
        y = decodedObject.rect.top

        # print(x, y)

        # print('Type : ', decodedObject.type)
        # print('Data : ', decodedObject.data, '\n')

        barCode = decodedObject.data.decode()
        barCode = barCode[2:]
        barCode = barCode[:-1]
        # print(barCode)
        password = "Va$hi$ht.TECH#@ff@irs"
        # Let us decrypt using our original password
        
        decrypted = decrypt(barCode, password).decode()
        if decrypted:
            cv2.putText(frame, decrypted, (x, y), font, 1,
                    (0, 255, 255), 2, cv2.LINE_AA)
            break

    # Display the resulting frame
    cv2.imshow('frame', frame)
    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        break
    elif key & 0xFF == ord('s'):  # wait for 's' key to save
        cv2.imwrite('Capture.png', frame)

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
