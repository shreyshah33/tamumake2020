from google.cloud import vision
from google.cloud.vision import types
from PIL import Image, ImageDraw
from datetime import datetime
import numpy as np
import cv2
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
        
cam = cv2.VideoCapture(0)

likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE', 'LIKELY', 'VERY_LIKELY')

client = vision.ImageAnnotatorClient()

cred = credentials.Certificate('key2.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
firestore_document = db.collection('face_follower').document('face_data') 

def max_key(jsonData):
    max_data=0 
    maxKey=None
    for i in jsonData:
        if(int(jsonData[i])>max_data):
            max_data=int(jsonData[i])
            maxKey=i
    return maxKey

def detect_face(face_file, max_results=4):

    content = face_file.read()
    image = types.Image(content=content)

    data = client.face_detection(
        image=image, max_results=max_results).face_annotations
        
    if len(data) >= 1:
        emotions = {
            "joy": int(data[0].joy_likelihood),
            "surprise": int(data[0].surprise_likelihood),
            "angry": int(data[0].anger_likelihood),
            "sorrow": int(data[0].sorrow_likelihood)
        }

        roll = int(data[0].roll_angle + 90)
        pan = int(data[0].pan_angle + 90)
        tilt = int(data[0].tilt_angle + 90)

        send_data = {
            "emotion": max_key(emotions),
            "tilt": tilt,
            "pan": pan,
            "roll": roll
        }
        firestore_document.update(send_data)
        print(send_data)
    # return data
        

def main(input_filename):
    with open(input_filename, 'rb') as image:
        detect_face(image)


if __name__ == "__main__":
    while True:
        ret, frame = cam.read()
        img_name = "opencv_frame_1.jpg"
        cv2.imwrite(img_name, frame)
        file_name = "/Users/shreyshah/Projects/tamumake2020/opencv_frame_1.jpg"
        output_filename = file_name + "out" + ".jpg"
        main(file_name)
        time.sleep(0.33)
