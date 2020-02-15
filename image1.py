from google.cloud import vision
from google.cloud.vision import types
from PIL import Image, ImageDraw
from datetime import datetime
import numpy as np
import cv2

client = vision.ImageAnnotatorClient()

def detect_face(face_file, max_results=4):
    """Uses the Vision API to detect faces in the given file.

    Args:
        face_file: A file-like object containing an image with faces.

    Returns:
        An array of Face objects with information about the picture.
    """
    client = vision.ImageAnnotatorClient()

    content = face_file.read()
    image = types.Image(content=content)

    return client.face_detection(
        image = image, max_results = max_results).face_annotations
        
def detect_face(face_file, max_results=4):
    """Uses the Vision API to detect faces in the given file.

    Args:
        face_file: A file-like object containing an image with faces.

    Returns:
        An array of Face objects with information about the picture.
    """
    client = vision.ImageAnnotatorClient()

    content = face_file.read()
    image = types.Image(content=content)

    data = client.face_detection(
        image = image, max_results = max_results).face_annotations

    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')
    # print(data[0])
    print('anger: {}'.format(likelihood_name[data[0].anger_likelihood]))
    print('joy: {}'.format(likelihood_name[data[0].joy_likelihood]))
    print('surprise: {}'.format(likelihood_name[data[0].surprise_likelihood]))
    print('roll: {}'.format(data[0].roll_angle))
    print('pan: {}'.format(data[0].pan_angle))
    print('tilt: {}'.format(data[0].tilt_angle))
    
    return data

def highlight_faces(image, faces, output_filename):
    """Draws a polygon around the faces, then saves to output_filename.

    Args:
      image: a file containing the image with the faces.
      faces: a list of faces found in the file. This should be in the format
          returned by the Vision API.
      output_filename: the name of the image file to be created, where the
          faces have polygons drawn around them.
    """
    im = Image.open(image)
    draw = ImageDraw.Draw(im)
    # Sepecify the font-family and the font-size
    for face in faces:
        box = [(vertex.x, vertex.y)
               for vertex in face.bounding_poly.vertices]
        draw.line(box + [box[0]], width=5, fill='#00ff00')
        # Place the confidence value/score of the detected faces above the
        # detection box in the output image
        draw.text(((face.bounding_poly.vertices)[0].x,
                   (face.bounding_poly.vertices)[0].y - 30),
                  str(format(face.detection_confidence, '.3f')) + '%',
                  fill='#FF0000')
    im.save(output_filename) 
        

def main(input_filename, output_filename, max_results):
    with open(input_filename, 'rb') as image:
        time1 = datetime.now()
        faces = detect_face(image, max_results)
        print('Found {} face{}'.format(
            len(faces), '' if len(faces) == 1 else 's'))
        print(datetime.now()-time1)
        print('Writing to file {}'.format(output_filename))
        # Reset the file pointer, so we can read the file again
        image.seek(0)
        highlight_faces(image, faces, output_filename)


if __name__ == "__main__":
    file_name = "/Users/shreyshah/Pictures/DP copy.jpg"
    output_filename = file_name + "out" + ".jpg"
    max_res = 5
    main(file_name, output_filename, 5)
#     cap = cv2.VideoCapture(0)

# # Define the codec and create VideoWriter object
#     fourcc = cv2.VideoWriter_fourcc(*'XVID')
#     out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))

#     while(cap.isOpened()):
#         ret, frame = cap.read()
#         if ret==True:
#             frame = cv2.flip(frame,0)

#             # write the flipped frame
#             out.write(frame)

#             # cv2.imshow('frame',frame)
#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break
#         else:
#             break

#     # Release everything if job is finished
#     cap.release()
#     out.release()
#     cv2.destroyAllWindows()
