import os
import time
import serial
import pygame

# Headless SSH mode
os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

PORT = "/dev/ttyUSB0"
BAUD = 9600

# Stability settings
DEADZONE = 0.45
DEBOUNCE_TIME = 0.10
SEND_INTERVAL = 0.10
STOP = 0

# Arduino command mapping
# Arm facing you
SERVO5_RIGHT = 18
SERVO5_LEFT  = 19

SERVO3_UP    = 20
SERVO3_DOWN  = 21

GRIPPER_CLOSE = 22
GRIPPER_OPEN  = 23

SERVO2_UP    = 24
SERVO2_DOWN  = 25

BASE_LEFT    = 26
BASE_RIGHT   = 27

SERVO4_UP    = 16
SERVO4_DOWN  = 17

# PS5 button mapping
BTN_X = 0
BTN_CIRCLE = 1
BTN_TRIANGLE = 2
BTN_SQUARE = 3
BTN_L1 = 4
BTN_R1 = 5
BTN_L2 = 6
BTN_R2 = 7
BTN_PS = 10
BTN_L3 = 11
BTN_R3 = 12

# PS5 axis mapping
AXIS_LEFT_X = 0
AXIS_LEFT_Y = 1
AXIS_RIGHT_X = 3
AXIS_RIGHT_Y = 4


def get_axis(pad, axis_number):
    if axis_number < pad.get_numaxes():
        return pad.get_axis(axis_number)
    return 0.0


def get_button(pad, button_number):
    if button_number < pad.get_numbuttons():
        return pad.get_button(button_number)
    return 0


def send_command(ser, cmd):
    ser.write(bytes([cmd]))


def decide_command(pad):
    """
    Final control layout:

    L1 / R1                 -> Servo 1 base left/right
    Left stick left/right   -> Servo 4 up/down
    Left stick up/down      -> Servo 2 up/down

    Right stick left/right  -> Servo 5 left/right
    Right stick up/down     -> Servo 3 up/down

    X / Circle              -> Gripper open/close
    Triangle                -> Emergency stop
    """

    lx = get_axis(pad, AXIS_LEFT_X)
    ly = get_axis(pad, AXIS_LEFT_Y)
    rx = get_axis(pad, AXIS_RIGHT_X)
    ry = get_axis(pad, AXIS_RIGHT_Y)

    # Emergency stop
    if get_button(pad, BTN_TRIANGLE):
        return STOP, "Emergency stop"

    # Gripper
    if get_button(pad, BTN_X):
        return GRIPPER_OPEN, "Gripper open"
    if get_button(pad, BTN_CIRCLE):
        return GRIPPER_CLOSE, "Gripper close"

    # Base servo now on L1/R1
    if get_button(pad, BTN_L1):
        return BASE_LEFT, "Base left"
    if get_button(pad, BTN_R1):
        return BASE_RIGHT, "Base right"

    # Left stick left/right now controls Servo 4
    if lx < -DEADZONE:
        return SERVO4_UP, "Servo 4 up"
    if lx > DEADZONE:
        return SERVO4_DOWN, "Servo 4 down"

    # Left stick up/down controls Servo 2
    if ly < -DEADZONE:
        return SERVO2_UP, "Servo 2 up"
    if ly > DEADZONE:
        return SERVO2_DOWN, "Servo 2 down"

    # Right stick left/right controls Servo 5
    if rx < -DEADZONE:
        return SERVO5_LEFT, "Servo 5 left"
    if rx > DEADZONE:
        return SERVO5_RIGHT, "Servo 5 right"

    # Right stick up/down controls Servo 3
    if ry < -DEADZONE:
        return SERVO3_UP, "Servo 3 up"
    if ry > DEADZONE:
        return SERVO3_DOWN, "Servo 3 down"

    return STOP, "Neutral"


def main():
    print("Opening Arduino Nano on", PORT)

    try:
        ser = serial.Serial(PORT, BAUD, timeout=1)
    except serial.SerialException as e:
        print("Could not open Arduino Nano serial port.")
        print("Error:", e)
        print("Check that the Nano is connected as /dev/ttyUSB0.")
        return

    time.sleep(2)

    pygame.init()
    pygame.joystick.init()

    if pygame.joystick.get_count() == 0:
        print("No PS5 controller found.")
        ser.close()
        pygame.quit()
        return

    pad = pygame.joystick.Joystick(0)
    pad.init()

    print("Controller:", pad.get_name())
    print("Axes:", pad.get_numaxes())
    print("Buttons:", pad.get_numbuttons())
    print()
    print("PS5 robotic arm control started.")
    print("--------------------------------")
    print("L1 / R1                 = Servo 1 base")
    print("Left stick left/right   = Servo 4")
    print("Left stick up/down      = Servo 2")
    print("Right stick left/right  = Servo 5")
    print("Right stick up/down     = Servo 3")
    print("X / Circle              = Gripper open/close")
    print("Triangle                = Emergency stop")
    print("CTRL+C                  = Stop program safely")
    print()

    current_cmd = STOP
    current_label = "Neutral"

    candidate_cmd = STOP
    candidate_label = "Neutral"
    candidate_since = time.time()

    last_sent = 0
    last_printed_cmd = None

    try:
        while True:
            pygame.event.pump()

            new_cmd, new_label = decide_command(pad)
            now = time.time()

            # Start debounce timer when command changes
            if new_cmd != candidate_cmd:
                candidate_cmd = new_cmd
                candidate_label = new_label
                candidate_since = now

            # Accept command only after it remains stable
            if (now - candidate_since) >= DEBOUNCE_TIME:
                current_cmd = candidate_cmd
                current_label = candidate_label

            # Send command at controlled rate
            if (now - last_sent) >= SEND_INTERVAL:
                send_command(ser, current_cmd)
                last_sent = now

                if current_cmd != last_printed_cmd:
                    print(f"Command {current_cmd}: {current_label}")
                    last_printed_cmd = current_cmd

            time.sleep(0.01)

    except KeyboardInterrupt:
        print("\nStopping arm safely...")

    finally:
        for _ in range(5):
            send_command(ser, STOP)
            time.sleep(0.05)

        ser.close()
        pygame.quit()
        print("Done.")


if __name__ == "__main__":
    main()
