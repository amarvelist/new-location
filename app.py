# Import eventlet and monkey patch at the top before any other imports
import eventlet
eventlet.monkey_patch()

from flask import Flask, request, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# Enable CORS to allow cross-origin requests
CORS(app)

# Initialize socketio with eventlet
socketio = SocketIO(app, async_mode='eventlet')

@app.route('/')
def index():
    return "Welcome to the Real-Time Tracking App!"

# Handle data sent from the Android app
@app.route('/track', methods=['POST'])
def track():
    # Debugging: Print incoming data to logs
    data = request.json
    print("Data received:", data)  # Debugging print

    # Extract longitude, latitude, and floor details from the request
    longitude = data.get('longitude')
    latitude = data.get('latitude')
    floor = data.get('floor')

    # Emit the data to the web app via SocketIO
    socketio.emit('location_update', {'longitude': longitude, 'latitude': latitude, 'floor': floor})
    
    # Return success response
    return jsonify({"status": "success"})

if __name__ == '__main__':
    # Debugging: Run the app with SocketIO and eventlet
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
