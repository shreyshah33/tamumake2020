from flask import Flask, jsonify, request, send_from_directory, render_template
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud import storage
import json
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

@app.route('/pillstaken')
def pillstaken():
    firestore_document.update({"pills": True})

@app.route('/pillsreset')
def pillsreset():
    firestore_document.update({"pills": False})

@app.route('/orderadd', methods=['POST'])
def add():
    data = firestore_document.get().to_dict()
    if 'order' in data:
        data['order'].append((str(json.loads(request.get_data())["order"])))
        data['order'].append((int(json.loads(request.get_data())["quantity"])))
        firestore_document.update({"order": data['order']})
    else:
        firestore_document.update({"order": [(str(json.loads(request.get_data())["order"])), (int(json.loads(request.get_data())["quantity"]))]})

# Run on localhost if targeted by flask
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)