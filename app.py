import eventlet
eventlet.monkey_patch()

from flask import Flask, request, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS  # Import CORS for cross-origin requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# Enable CORS for all routes
CORS(app)

# Initialize socketio with eventlet
socketio = SocketIO(app, async_mode='eventlet', cors_allowed_origins="*")

@app.route('/')
def index():
    return "Welcome to the Real-Time Tracking App!"

# Handle data sent from the Android app
@app.route('/track', methods=['POST'])
def track():
    data = request.json
    
    # Extract the required fields from the received data
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    username = data.get('name')  # Adjusted from 'username' to 'name'
    user_id = data.get('id')  # Adjusted from 'user_id' to 'id'
    floor = data.get('floor')

    # Print the received data for debugging
    print(f"Received data: {data}")

    # Emit the data to the web app via SocketIO
    socketio.emit('location_update', {
        'latitude': latitude, 
        'longitude': longitude, 
        'username': username,
        'user_id': user_id,
        'floor': floor
    })
    
    return jsonify({"status": "success"})

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
