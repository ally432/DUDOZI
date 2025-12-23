# mission.py
from camera_manager import get_frame
from steering_model import infer_xy
from line_follow import LineFollower
from motor_controller import drive, stop
from servo_controller import set_line_follow_pose

_running = False

follower = LineFollower(
    speed_gain=0.15,
    steering_gain=0.12,
    steering_dgain=0.0,
    steering_bias=0.0,
)

def start_mission(cycle_id):
    global _running
    _running = True

    set_line_follow_pose()

    print(f"[MISSION] start {cycle_id}")

    while _running:
        frame = get_frame()
        if frame is None:
            continue

        x, y = infer_xy(frame)
        steering, speed = follower.compute(x, y)
        drive(steering, speed)

def stop_mission():
    global _running
    _running = False
    stop()
