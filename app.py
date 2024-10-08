# app.py

# Import eventlet and monkey patch at the top before any other imports
import eventlet
eventlet.monkey_patch()

from flask import Flask, request, jsonify
from flask_socketio import SocketIO
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# Initialize socketio with eventlet
socketio = SocketIO(app, async_mode='eventlet')

@app.route('/')
def index():
    return "Welcome to the Real-Time Tracking App!"

# Handle data sent from the Android app
@app.route('/track', methods=['POST'])
def track():
    data = request.json
    longitude = data.get('longitude')
    latitude = data.get('latitude')
    floor = data.get('floor')

    # Emit the data to the web app via SocketIO
    socketio.emit('location_update', {'longitude': longitude, 'latitude': latitude, 'floor': floor})
    
    return jsonify({"status": "success"})

if __name__ == '__main__':
    socketio.run(app, debug=True)
