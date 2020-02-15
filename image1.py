from google.cloud import vision
from google.cloud.vision import types
from PIL import Image, ImageDraw
from datetime import datetime
import numpy as np
import cv2
import time
        

client = vision.ImageAnnotatorClient()

def detect_face(face_file, max_results=4):

    content = face_file.read()
    image = types.Image(content=content)

    data = client.face_detection(
        image = image, max_results = max_results).face_annotations

    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')
    if len(data) >= 1:
        # print(data[0])
        send_data = {
            "joy": int(data[0].joy_likelihood),
            "surprise": int(data[0].sorrow_likelihood),
            "angry": int(data[0].anger_likelihood),
            "sorrow": int(data[0].surprise_likelihood)
        }
        
        print(send_data)
        # print('anger: {}'.format(likelihood_name[data[0].anger_likelihood]))
        # print('joy: {}'.format(likelihood_name[data[0].joy_likelihood]))
        # print('surprise: {}'.format(likelihood_name[data[0].surprise_likelihood]))
        # print('roll: {}'.format(data[0].roll_angle))
        # print('pan: {}'.format(data[0].pan_angle))
        # print('tilt: {}'.format(data[0].tilt_angle))
    
    return data
        

def main(input_filename):
    with open(input_filename, 'rb') as image:
        faces = detect_face(image)
        print('Found {} face{}'.format(
            len(faces), '' if len(faces) == 1 else 's'))


if __name__ == "__main__":
    while True:
        file_name = "/Users/shreyshah/Projects/tamumake2020/opencv_frame_1.jpg"
        output_filename = file_name + "out" + ".jpg"
        main(file_name)
        time.sleep(0.33)
