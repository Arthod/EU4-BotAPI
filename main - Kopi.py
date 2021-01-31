#import tensorflow as tf
import numpy as np
import cv2 as cv
from PIL import Image, ImageGrab, ImageFilter
import pytesseract
from pytesseract import image_to_string
import pygame as pg
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Ahmad\AppData\Local\Tesseract-OCR\tesseract.exe'
from value import Value
from province import Province
from rect import Rect
import pyautogui
import time
import random
#https://www.youtube.com/watch?v=2CZltXv-Gpk

class Main:
    def __init__(self):
        self.read_locations = [
            Value("cash", Rect(178, 20, 35, 11)),
            Value("manpower", Rect(256, 20, 43, 11)),
            Value("sailors", Rect(347, 20, 35, 11)),
            Value("stability", Rect(487, 20, 9, 11)),
            Value("corruption", Rect(539, 20, 20, 11)),
            Value("prestige", Rect(606, 20, 20, 11)),
            Value("legitimacy", Rect(675, 20, 20, 11))
        ]
        
        #pg init
        pg.init()
        self.screen = pg.display.set_mode((960, 540))
        self.clock = pg.time.Clock()
        pg.font.init()
        self.font = pg.font.Font('freesansbold.ttf', 8) 
        self.frame_count = 0

        # EU4 init
        self.provinces = [""]
        provinces_txt = np.loadtxt('map/provinces.txt', dtype=str, delimiter=",")
        for p in provinces_txt:
            id = int(p[0])
            name = str(p[4])
            color_rgb = (int(p[1]), int(p[2]), int(p[3]))
            position = (int(p[5]), int(p[6]))
            self.provinces.append(Province(id, name, color_rgb, position))
        print(len(self.provinces))

        self.ongoing = True
        self.capital_id = 65
        while self.ongoing:
            if (self.frame_count % 10000 == 0):
                self.draw_game(self.read_locations)
                self.get_values(self.read_locations)
                #self.draw_values(self.read_locations)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.ongoing = False
            key = pg.key.get_pressed()
            if key[pg.K_q]:
                self.move_troops(134, 73)

                
            self.frame_count += 1

    def move_troops(self, from_prov_id, to_prov_id):
        self.camera_to_province(from_prov_id)
        pyautogui.moveTo(10, 180)
        pyautogui.dragTo(1520, 950, 0.25, button='left')

        self.camera_to_province(to_prov_id)

        pyautogui.moveTo(1920/2, 1080/2)
        pyautogui.click(button='right')


    def select_province(self, prov_id):
        time.sleep(0.5)
        self.camera_to_province(prov_id)
        time.sleep(1)
        pyautogui.click(1920/2, 1080/2)

    def camera_to_province(self, prov_id):
        prov_pos = self.provinces[prov_id].get_pos()
        map_box = (1644, 933, 1911, 1031)   #(1645, 933, 1912, 1031)
        w = map_box[2] - map_box[0]
        h = map_box[3] - map_box[1]
        pyautogui.moveTo(prov_pos[0] * (w/5632.0) + map_box[0] + 2, 1 + h - prov_pos[1] * (h/2048.0) + map_box[1])
        pyautogui.click()
        time.sleep(0.5)

    def draw_game(self, read_locations):
        def rect(x, y, w, h, color_rgb):
            pg.draw.rect(self.screen, color_rgb, pg.Rect(x, y, w, h))
        def text(x, y, font, color_rgb, txt):
            text = font.render(txt, False, color_rgb)
            self.screen.blit(text, (x, y))
        self.screen.fill((255, 255, 255))
        image = ImageGrab.grab(bbox=(0, 0, 1920, 1080))
        image = image.resize((960, 540))

        image = pg.image.fromstring(image.tobytes(), image.size, image.mode)
        self.screen.blit(image, (0, 0))
        for read in read_locations:
            b = read.get_rect()
            rect(b[0]/2-6, b[1]/2-6, (b[2]-b[0])/2+12, (b[3]-b[1])/2+12, (0, 0, 0))
            value = str(read.value)
            text(b[0]/2, b[1]/2, self.font, (255, 255, 255), value)
        pg.display.flip()
        
    def draw_values(self, read_locations):
        def rect(x, y, w, h, color_rgb):
            pg.draw.rect(self.screen, color_rgb, pg.Rect(x, y, w, h))
        def text(x, y, font, color_rgb, txt):
            text = font.render(txt, False, color_rgb)
            self.screen.blit(text, (x, y))
        self.screen.fill((255, 255, 255))
        image = ImageGrab.grab(bbox=(0, 0, 1920, 1080))
        image = image.resize((960, 540))

        image = pg.image.fromstring(image.tobytes(), image.size, image.mode)
        self.screen.blit(image, (0, 0))
        for i, read in enumerate(read_locations):
            text(0, i * 32, self.font, (255, 255, 255), read.get_value())
        pg.display.flip()

    def get_values(self, read_locations):
        for read in read_locations:
            value_img = ImageGrab.grab(bbox=read.get_rect())
            value = self.recognize_number(value_img)
            read.value = value
            #print(str(read.get_name()) + ": " + str(read.get_value()))


    def recognize_number(self, image):
        # Works well in vanilla
        image = image.convert("1", dither=Image.NONE)
        image = image.point(lambda p: p < 180 and 255)
        image = image.resize((45*2, 21*2))

        int = image_to_string(image, config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789k')
        return int

main = Main()