from flask import Flask, Response, render_template_string, request
from flask_socketio import SocketIO
import cv2
import numpy as np
from mss import mss
import logging
import socket

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secure_key_here'

# Initialize SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

CAMERA_INDEX = 0

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"
    finally:
        s.close()


def camera_generator():
    cap = cv2.VideoCapture(CAMERA_INDEX)
    while True:
        success, frame = cap.read()
        if not success:
            break
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def screen_generator():
    with mss() as sct:
        monitor = sct.monitors[1]
        while True:
            img = np.array(sct.grab(monitor))
            _, buffer = cv2.imencode('.jpg', img)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/camera')
def camera_feed():
    return Response(camera_generator(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/screen')
def screen_feed():
    return Response(screen_generator(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@socketio.on('connect')
def handle_connect():
    logging.info(f"Client connected: {request.sid}")


@socketio.on('disconnect')
def handle_disconnect():
    logging.info(f"Client disconnected: {request.sid}")


@app.route('/')
def control_panel():
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Remote Control</title>
        <style>
            body { font-family: Arial, sans-serif; padding: 20px; }
            .video-feed {
                width: 45%;
                margin: 10px;
                border: 2px solid #ddd;
                border-radius: 5px;
            }
        </style>
    </head>
    <body>
        <h1>Remote Control Panel</h1>
        <div>
            <img class="video-feed" src="/camera">
            <img class="video-feed" src="/screen">
        </div>

        <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
        <script>
            const socket = io('http://' + window.location.hostname + ':5000');
        </script>
    </body>
    </html>
    ''')


if __name__ == '__main__':
    local_ip = get_local_ip()
    print("\n" + "=" * 50)
    print(f"  Access via: http://{local_ip}:5000")
    print("=" * 50 + "\n")

    socketio.run(app, host='0.0.0.0', port=5000, debug=False, allow_unsafe_werkzeug=True)
