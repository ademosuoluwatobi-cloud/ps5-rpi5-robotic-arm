#!/usr/bin/env python3
"""
mediapipe_laptop_arm_control.py

Laptop Webcam -> MediaPipe Hand Tracking -> Arduino Nano USB Serial -> 6DOF Robotic Arm

This version is for Windows laptop use.

Connection:
    Laptop webcam captures hand
    Python + MediaPipe detects gesture
    Laptop sends command byte to Arduino Nano through USB
    Arduino moves the robotic arm servos
"""

import cv2
import mediapipe as mp
import serial
import time
import math


# Change this to your Arduino Nano COM port.
# Check Arduino IDE: Tools -> Port
SERIAL_PORT = "COM4"
BAUD_RATE = 9600
SERIAL_TIMEOUT = 1

# 0 usually means the main laptop webcam.
CAMERA_INDEX = 0

SEND_INTERVAL = 0.10
DEBOUNCE_TIME = 0.10
POSITION_DEADZONE = 0.08
TILT_DEADZONE = 12


# MediaPipe hand landmark indexes
WRIST = 0

INDEX_MCP = 5
INDEX_PIP = 6
INDEX_TIP = 8

MIDDLE_MCP = 9
MIDDLE_PIP = 10
MIDDLE_TIP = 12

RING_TIP = 16
PINKY_TIP = 20

THUMB_TIP = 4


def angle_between(a, b, c):
    ax = a.x - b.x
    ay = a.y - b.y

    cx = c.x - b.x
    cy = c.y - b.y

    dot = ax * cx + ay * cy
    mag = math.sqrt(ax**2 + ay**2) * math.sqrt(cx**2 + cy**2)

    if mag == 0:
        return 0

    cos_angle = max(-1, min(1, dot / mag))
    return math.degrees(math.acos(cos_angle))


def is_finger_curled(lm, mcp_i, pip_i, tip_i):
    angle = angle_between(lm[mcp_i], lm[pip_i], lm[tip_i])
    return angle < 150


def detect_gesture(lm):
    index_curled = is_finger_curled(lm, INDEX_MCP, INDEX_PIP, INDEX_TIP)
    middle_curled = is_finger_curled(lm, MIDDLE_MCP, MIDDLE_PIP, MIDDLE_TIP)

    ring_curled = lm[RING_TIP].y > lm[MIDDLE_MCP].y
    pinky_curled = lm[PINKY_TIP].y > lm[MIDDLE_MCP].y

    thumb_up = lm[THUMB_TIP].y < lm[WRIST].y - 0.15

    if thumb_up and index_curled and middle_curled:
        return "thumbs_up"

    if index_curled and middle_curled and ring_curled and pinky_curled:
        return "fist"

    if (
        not index_curled
        and not middle_curled
        and not ring_curled
        and not pinky_curled
    ):
        return "open_palm"

    return None


def get_hand_tilt_degrees(lm):
    dx = lm[MIDDLE_MCP].x - lm[WRIST].x
    dy = lm[MIDDLE_MCP].y - lm[WRIST].y

    return math.degrees(math.atan2(dx, -dy))


def get_palm_centre(lm):
    cx = (lm[WRIST].x + lm[INDEX_MCP].x + lm[MIDDLE_MCP].x) / 3
    cy = (lm[WRIST].y + lm[INDEX_MCP].y + lm[MIDDLE_MCP].y) / 3

    return cx, cy


def decide_command(lm, paused):
    gesture = detect_gesture(lm)

    if gesture == "thumbs_up":
        return "TOGGLE_PAUSE"

    if paused:
        return None

    if gesture == "fist":
        return 27       # gripper close

    if gesture == "open_palm":
        return 26       # gripper open

    index_curled = is_finger_curled(lm, INDEX_MCP, INDEX_PIP, INDEX_TIP)
    middle_curled = is_finger_curled(lm, MIDDLE_MCP, MIDDLE_PIP, MIDDLE_TIP)

    if index_curled:
        return 21       # elbow up / bend

    if middle_curled:
        return 19       # wrist pitch up

    tilt = get_hand_tilt_degrees(lm)

    if tilt > TILT_DEADZONE:
        return 23       # wrist roll right

    if tilt < -TILT_DEADZONE:
        return 22       # wrist roll left

    cx, cy = get_palm_centre(lm)

    if cx < 0.5 - POSITION_DEADZONE:
        return 16       # base left

    if cx > 0.5 + POSITION_DEADZONE:
        return 17       # base right

    if cy < 0.5 - POSITION_DEADZONE:
        return 25       # shoulder up

    if cy > 0.5 + POSITION_DEADZONE:
        return 24       # shoulder down

    return None


def command_name(command):
    names = {
        16: "Base Left",
        17: "Base Right",
        18: "Wrist Pitch Down",
        19: "Wrist Pitch Up",
        20: "Elbow Down",
        21: "Elbow Up",
        22: "Wrist Roll Left",
        23: "Wrist Roll Right",
        24: "Shoulder Down",
        25: "Shoulder Up",
        26: "Gripper Open",
        27: "Gripper Close",
        0: "STOP",
    }

    return names.get(command, "Unknown")


def main():
    print("-- Laptop MediaPipe Robotic Arm Control --")
    print(f"Serial port: {SERIAL_PORT}")
    print(f"Camera index: {CAMERA_INDEX}")

    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=SERIAL_TIMEOUT)
        time.sleep(2)
        print("Arduino serial connected.")
    except serial.SerialException as e:
        print(f"ERROR: Could not open Arduino serial port: {e}")
        print("Check Arduino IDE -> Tools -> Port, then update SERIAL_PORT.")
        return

    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils

    hands = mp_hands.Hands(
        model_complexity=0,
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.6,
    )

    cap = cv2.VideoCapture(CAMERA_INDEX)

    if not cap.isOpened():
        print("ERROR: Could not open laptop webcam.")
        ser.close()
        hands.close()
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    print()
    print("Ready.")
    print("Controls:")
    print("  Palm left/right      = Base left/right")
    print("  Palm up/down         = Shoulder up/down")
    print("  Index curl           = Elbow up")
    print("  Middle curl          = Wrist pitch up")
    print("  Hand tilt left/right = Wrist roll")
    print("  Fist                 = Gripper close")
    print("  Open palm            = Gripper open")
    print("  Thumbs up            = Pause / Resume")
    print("  Q                    = Quit")
    print()

    paused = False
    last_send_time = 0
    last_command = None

    debounce_command = None
    debounce_start = 0

    thumbs_up_latched = False

    try:
        while True:
            ret, frame = cap.read()

            if not ret or frame is None:
                print("Camera frame not received.")
                break

            frame = cv2.flip(frame, 1)

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = hands.process(rgb)

            now = time.time()
            command = None

            if result.multi_hand_landmarks:
                hand_lm = result.multi_hand_landmarks[0]
                lm = hand_lm.landmark

                mp_drawing.draw_landmarks(
                    frame,
                    hand_lm,
                    mp_hands.HAND_CONNECTIONS,
                )

                raw_cmd = decide_command(lm, paused)

                if raw_cmd == "TOGGLE_PAUSE":
                    if not thumbs_up_latched:
                        paused = not paused
                        thumbs_up_latched = True

                        if paused:
                            print("[PAUSED]")
                            ser.write(bytes([0]))
                        else:
                            print("[RESUMED]")

                    raw_cmd = None
                else:
                    thumbs_up_latched = False

                if raw_cmd != debounce_command:
                    debounce_command = raw_cmd
                    debounce_start = now

                if (now - debounce_start) >= DEBOUNCE_TIME:
                    command = debounce_command

            else:
                debounce_command = None
                thumbs_up_latched = False

            if (now - last_send_time) >= SEND_INTERVAL:
                if command is not None and not paused:
                    if command != last_command:
                        ser.write(bytes([command]))
                        print(f"CMD {command}: {command_name(command)}")
                        last_command = command
                else:
                    if last_command is not None:
                        ser.write(bytes([0]))
                        print("CMD 0: STOP")
                        last_command = None

                last_send_time = now

            if paused:
                status_text = "PAUSED"
            elif command is None:
                status_text = "IDLE"
            else:
                status_text = f"CMD {command}: {command_name(command)}"

            cv2.putText(
                frame,
                status_text,
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2,
            )

            cv2.putText(
                frame,
                "Thumbs up = pause/resume | Q = quit",
                (20, 460),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2,
            )

            cv2.imshow("Laptop MediaPipe Arm Control", frame)

            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                print("Q pressed. Exiting.")
                break

    except KeyboardInterrupt:
        print()
        print("Ctrl+C received. Stopping.")

    finally:
        print("Sending STOP...")
        try:
            ser.write(bytes([0]))
        except Exception:
            pass

        cap.release()
        cv2.destroyAllWindows()
        hands.close()
        ser.close()

        print("Done.")


if __name__ == "__main__":
    main()
