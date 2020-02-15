import cv2
from time import sleep
cam = cv2.VideoCapture(0)

img_counter = 0

while True:
    ret, frame = cam.read()
    img_name = "opencv_frame_1.jpg"
    cv2.imwrite(img_name, frame)
    sleep(0.1)

cam.release()

