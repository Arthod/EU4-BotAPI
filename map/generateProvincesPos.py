import numpy as np
from PIL import Image

provinces_txt = np.loadtxt("definition.txt", dtype=str, delimiter=",")

img = Image.open("provinces.png")
rgbsAtXY = {}
for x in range(img.size[0]):
    for y in range(img.size[1]):
        p_rgb = img.getpixel((x, y))
        if (p_rgb in rgbsAtXY):
            rgbsAtXY[p_rgb][0] += x
            rgbsAtXY[p_rgb][1] += y
            rgbsAtXY[p_rgb][2] += 1

        else:
            rgbsAtXY[p_rgb] = [x, y, 1]

f = open("demofile2.txt", "a")
for p in provinces_txt:
    id = int(p[0])
    r = int(p[1])
    g = int(p[2])
    b = int(p[3])
    name = str(p[4])

    COM = rgbsAtXY[(r, g, b, 255)]
    x = round(COM[0] / COM[2])
    y = round(COM[1] / COM[2])

    f.write("{},{},{},{},{},{},{}\n".format(id, r, g, b, name, x, y))
    
f.close()