from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, async_mode='eventlet')

@app.route('/')
def home():
    return "Welcome to App2!"

@app.route('/receive', methods=['POST'])
def receive():
    data = request.json
    result = data['number'] ** 3  # Example computation: cube the number
    return jsonify({"result": result})

@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)
    emit('response', {'data': 'Message received!'})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001)