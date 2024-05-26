from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, emit
import requests
import socketio

app = Flask(__name__)
socketio1 = SocketIO(app, async_mode='eventlet')

# Establish a SocketIO connection to App2
sio = socketio.Client()
sio.connect('http://localhost:5001')

@sio.event
def connect():
    print('Connected to App2')

@sio.event
def response(data):
    print('Received response from App2:', data)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/compute', methods=['POST'])
def compute():
    number = request.form['number']
    response = requests.post("http://localhost:5001/receive", json={'number': int(number)})
    result = response.json().get('result', 'Error')
    return render_template('result.html', number=number, result=result)

@app.route('/communicate', methods=['POST'])
def communicate():
    data = request.json
    sio.emit('message', 'Hello from App1!')
    return jsonify({"status": "Message sent"})

if __name__ == '__main__':
    socketio1.run(app, host='0.0.0.0', port=5000)