import os
import time
import serial
import pygame

# Headless SSH mode
os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

PORT = "/dev/ttyUSB0"
BAUD = 9600
DEADZONE = 0.45
SEND_DELAY = 0.10

# Arduino command numbers
STOP = 0

BASE_LEFT = 18
BASE_RIGHT = 19

SHOULDER_DOWN = 20
SHOULDER_UP = 21

ELBOW_DOWN = 22
ELBOW_UP = 23

WRIST_DOWN = 24
WRIST_UP = 25

ROTATE_RIGHT = 26
ROTATE_LEFT = 27

GRIPPER_OPEN = 16
GRIPPER_CLOSE = 17


def get_axis(pad, index):
    if index < pad.get_numaxes():
        return pad.get_axis(index)
    return 0


def get_button(pad, index):
    if index < pad.get_numbuttons():
        return pad.get_button(index)
    return 0


print("Opening Arduino Nano on", PORT)
ser = serial.Serial(PORT, BAUD, timeout=1)
time.sleep(2)

pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("No controller found.")
    ser.close()
    raise SystemExit

pad = pygame.joystick.Joystick(0)
pad.init()

print("Controller:", pad.get_name())
print("Axes:", pad.get_numaxes())
print("Buttons:", pad.get_numbuttons())
print("Control started. Press CTRL+C to stop.\n")

last_cmd = None

try:
    while True:
        pygame.event.pump()

        # Common PS5/Linux axis mapping
        lx = get_axis(pad, 0)   # left stick left/right
        ly = get_axis(pad, 1)   # left stick up/down
        rx = get_axis(pad, 3)   # right stick left/right
        ry = get_axis(pad, 4)   # right stick up/down

        cmd = STOP

        # Left stick X controls base
        if lx < -DEADZONE:
            cmd = BASE_LEFT
        elif lx > DEADZONE:
            cmd = BASE_RIGHT

        # Left stick Y controls shoulder
        elif ly < -DEADZONE:
            cmd = SHOULDER_UP
        elif ly > DEADZONE:
            cmd = SHOULDER_DOWN

        # Right stick Y controls elbow
        elif ry < -DEADZONE:
            cmd = ELBOW_UP
        elif ry > DEADZONE:
            cmd = ELBOW_DOWN

        # Right stick X controls wrist
        elif rx < -DEADZONE:
            cmd = WRIST_DOWN
        elif rx > DEADZONE:
            cmd = WRIST_UP

        # Buttons for rotation and gripper
        # Button numbers may differ slightly, but these are a good first test.
        elif get_button(pad, 4):   # L1
            cmd = ROTATE_LEFT
        elif get_button(pad, 5):   # R1
            cmd = ROTATE_RIGHT
        elif get_button(pad, 0):   # Cross / X
            cmd = GRIPPER_OPEN
        elif get_button(pad, 1):   # Circle
            cmd = GRIPPER_CLOSE

        if cmd != last_cmd:
            print("Command:", cmd)
            last_cmd = cmd

        ser.write(bytes([cmd]))
        time.sleep(SEND_DELAY)

except KeyboardInterrupt:
    print("\nStopping arm...")
    ser.write(bytes([STOP]))
    ser.close()
    pygame.quit()
    print("Done.")
