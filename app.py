# Import eventlet and monkey patch at the top before any other imports
import eventlet
eventlet.monkey_patch()

from flask import Flask, request, jsonify
from flask_socketio import SocketIO
import os  # Import os to access environment variables

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
    port = int(os.environ.get('PORT', 5000))  # Get the port from the environment or default to 5000
    socketio.run(app, host='0.0.0.0', port=port)  # Bind to 0.0.0.0
