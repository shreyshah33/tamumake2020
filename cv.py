import cv2
import os
import numpy as np
from PIL import ImageGrab
import time
cam = cv2.VideoCapture(0)

# cv2.namedWindow("test")

img_counter = 0

while True:
    ret, frame = cam.read()
    img_name = "opencv_frame_1.jpg"
    cv2.imwrite(img_name, frame)
    time.sleep(0.03)

cam.release()

# cv2.destroyAllWindows()
