# stream_server.py
from flask import Flask, Response
import cv2
from camera_manager import get_frame

app = Flask(__name__)

def gen_frames():
    while True:
        frame = get_frame()
        if frame is None:
            continue

        _, jpeg = cv2.imencode(".jpg", frame)
        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" +
            jpeg.tobytes() +
            b"\r\n"
        )

@app.route("/video")
def video():
    return Response(
        gen_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )

def run_stream_server():
    print("Camera stream server started (port 5000)")
    app.run(host="0.0.0.0", port=5000, threaded=True)
