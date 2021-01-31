import numpy as np
import pytesseract
from pytesseract import image_to_string
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Ahmad\AppData\Local\Tesseract-OCR\tesseract.exe'
from province import Province
import pyautogui
import time
import random
#https://www.youtube.com/watch?v=2CZltXv-Gpk

class Main:
    def __init__(self):

        # EU4 init
        self.provinces = []
        provinces_txt = np.loadtxt('provinces.txt', dtype=str, delimiter=",")
        for p in provinces_txt:
            id = int(p[0])
            name = str(p[4])
            color_rgb = (int(p[1]), int(p[2]), int(p[3]))
            position = (int(p[5]), int(p[6]))
            self.provinces.append(Province(id, name, color_rgb, position))
        print("Loaded {} provinces.".format(len(self.provinces)))

        self.camera_to_province(1)
        self.click_center()

    def camera_to_province(self, prov_id):
        prov_pos = self.provinces[prov_id].get_pos()
        map_box = (1644, 933, 1911, 1031)   #(1645, 933, 1912, 1031)
        w = map_box[2] - map_box[0]
        h = map_box[3] - map_box[1]
        x = prov_pos[0] * (w/5632.0) + map_box[0] + 2
        #y = 1 + h - prov_pos[1] * (h/2048.0) - map_box[1]
        y = prov_pos[1] * (h/2048.0) + map_box[1] + 2
        pyautogui.moveTo(x, y)
        pyautogui.click()
        time.sleep(0.5)

    def click_center(self):
        pyautogui.moveTo(960, 540)
        pyautogui.click()
        time.sleep(0.5)

main = Main()