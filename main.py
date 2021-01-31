#import tensorflow as tf
import numpy as np
from PIL import Image, ImageFilter, ImageGrab

import cv2
import pytesseract
from province import Province
from pytesseract import image_to_string
from rect import Rect
from valueLocation import ValueLocation

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Ahmad\AppData\Local\Tesseract-OCR\tesseract.exe'
#https://www.youtube.com/watch?v=2CZltXv-Gpk

class Main:
    def __init__(self):
        self.value_locations = [
            ValueLocation("cash", Rect(178, 19, 35, 12)),
            ValueLocation("manpower", Rect(256, 19, 43, 12)),
            ValueLocation("sailors", Rect(347, 19, 35, 12)),
            ValueLocation("stability", Rect(438, 19, 9, 12)),
            ValueLocation("corruption", Rect(489, 19, 20, 12)),
            ValueLocation("prestige", Rect(556, 19, 20, 12)),
            ValueLocation("legitimacy", Rect(625, 19, 20, 12))
        ]

        count_frames = 0

        self.ongoing = True
        while self.ongoing:
            if (count_frames % 10000 == 0):
                values = self.get_values()
                print(values)
            count_frames += 1

    def get_values(self):
        values = []
        for value_location in self.value_locations:
            img = ImageGrab.grab(bbox=value_location.get_rect())
            img = img.convert("1", dither=Image.NONE).point(lambda p: p < 255)#.resize((45*2, 21*2))
            img.save("imgs/" + value_location.name + ".png")
            v = image_to_string(img, config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789k+-,')
            values.append(v)

        return values

main = Main()
