# camera_manager.py
from jetbot import Camera

_camera = None

def system_on():
    global _camera
    if _camera is None:
        _camera = Camera.instance(width=400, height=400)
        print("Camera ON")

def system_off():
    global _camera
    if _camera:
        _camera.stop()
        _camera = None
        print("Camera OFF")

def get_frame():
    if _camera is None:
        return None
    return _camera.value
