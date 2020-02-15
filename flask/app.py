from flask import Flask, jsonify, request, send_from_directory, render_template

app = Flask(__name__, static_url_path='')
from random import randint

emotions = ['joy', 'suprise', 'angry', 'sorrow']

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
    return jsonify(emotion=emotions[randint(0, len(emotions) - 1)])


# Run on localhost if targeted by flask
if __name__ == "__main__":
    app.run(host='0.0.0.0')