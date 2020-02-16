from flask import Flask, jsonify, request, send_from_directory, render_template
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud import storage

cred = credentials.Certificate('key2.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
firestore_document = db.collection('face_follower').document('face_data') 

app = Flask(__name__, static_url_path='')
from random import randint

emotions = ['joy', 'surprise', 'angry', 'sorrow']

@app.route('/')
def index():
    return render_template('index.html', emotions=emotions, stream='9lM0D-1qoFo')

# Serve static files from public folder
@app.route('/public/<path:path>')
def send_public(path):
    return send_from_directory('public', path)

@app.route('/api/guiUpdate')
def guiUpdate():
    # PUT YOUR CODE IN HERE 
    request = firestore_document.get().to_dict()
    
    emotion = request["emotion"]
    pills_taken = request['pillstaken']
    

    return jsonify(emotion = emotion)

@app.route('/api/pillsTaken')
def pills():
    pills = firestore_document.get().to_dict()['pillsTaken']
    return jsonify(pills=pills)


# Run on localhost if targeted by flask
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)