import numpy as np
import cv2



def map_array(src, tile_scale, color_bgr): # array[column[row[colors]]]
    image = cv2.imread(src, cv2.IMREAD_UNCHANGED)
    color = np.array((*color_bgr,255)) # platform color
    # red = enemy crawler, green = enemy floaty, pink = breakable boxes 
    # color = np.array((0,0,255,255)) # red
    lower = np.array(color*0.9, dtype="int").round().clip(0,255)
    upper = np.array(color*1.1, dtype="int").round().clip(0,255)
    matches = cv2.inRange(image, lower, upper)
    coords = np.array(np.where(matches == 255)).T # T = transverse => matrix
    coords = coords*tile_scale
    return coords


if __name__ == '__main__':
    pos = map_array("./imgs/prueba.png")
    print(pos)

#     [[[  0   0   0   0]
#   [  0   0 255 255]
#   [  0   0   0   0]]

#  [[114 255   0 255]
#   [  0   0   0   0]
#   [255   0  42 255]]

#  [[  0   0   0   0]
#   [255   0  42 255]
#   [  0   0   0   0]]]
