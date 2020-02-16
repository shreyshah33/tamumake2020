from flask import Flask, jsonify, request, send_from_directory, render_template
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json

cred = credentials.Certificate('key2.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
firestore_document = db.collection('face_follower').document('face_data') 

app = Flask(__name__, static_url_path='')
from random import randint

emotions = ['joy', 'surprise', 'angry', 'sorrow']

@app.route('/')
def index():
    return render_template('index.html', emotions=emotions)

# Serve static files from public folder
@app.route('/public/<path:path>')
def send_public(path):
    return send_from_directory('public', path)

@app.route('/api/emotion')
def emotion():
    # PUT YOUR CODE IN HERE 
    emotion = firestore_document.get().to_dict()["emotion"]
    return jsonify(emotion= emotion)
    # return {}

@app.route('/initiate', methods=['POST'])
def initiate():
    d = json.loads(request.get_data())['initiate']
    if d== 'true':
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