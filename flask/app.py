from flask import Flask, jsonify, request, send_from_directory, render_template
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud import storage
import json
import requests

cred = credentials.Certificate('key2.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
firestore_document = db.collection('face_follower').document('face_data') 

app = Flask(__name__, static_url_path='')
from random import randint

emotions = ['joy', 'surprise', 'angry', 'sorrow']

@app.route('/')
def index():
    return render_template('index.html', emotions=emotions, stream='4u4E6uIVkKw')

# Serve static files from public folder
@app.route('/public/<path:path>')
def send_public(path):
    return send_from_directory('public', path)

# Proxies BC cross origin
@app.route('/api/weather')
def weather():
    return jsonify(**requests.get('https://api.darksky.net/forecast/a47170938046286e71352254ae0ccc97/30.622104,-96.339161').json())

@app.route('/api/guiUpdate')
def guiUpdate():
    # PUT YOUR CODE IN HERE 
    request = firestore_document.get().to_dict()

    print(request)

    return jsonify(**request)

@app.route('/initiate', methods=['POST'])
def initiate():
    d = json.loads(request.get_data())['initiate']
    if d == 'true':
        firestore_document.update({"start": True})
        return "got it"
    return "wrong input"

@app.route('/deactivate')
def deactivate():
    firestore_document.update({"start": False})
    return "deactivating"

# Run on localhost if targeted by flask
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)