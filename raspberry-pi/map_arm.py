import serial
import time

PORT = "/dev/ttyUSB0"
BAUD = 9600

# Commands from your Arduino Nano sketch
commands = [18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 16, 17]

RUN_TIME = 0.25   # short movement to avoid stressing the arm
STOP = 0

ser = serial.Serial(PORT, BAUD, timeout=1)
time.sleep(2)

print("Arduino Robotic Arm Command Mapper")
print("----------------------------------")
print("For each command, watch the arm carefully.")
print("Write down: joint name + direction.")
print("Example: 18 = base left, 19 = base right")
print()
print("Press CTRL+C anytime to stop.")
print()

try:
    for cmd in commands:
        input(f"Press ENTER to test command {cmd}...")
        print(f"Sending command {cmd}")

        ser.write(bytes([cmd]))
        time.sleep(RUN_TIME)

        ser.write(bytes([STOP]))
        print("Stopped.")
        print("Write down what moved.\n")

        time.sleep(0.5)

except KeyboardInterrupt:
    print("\nEmergency stop.")

finally:
    ser.write(bytes([STOP]))
    ser.close()
    print("Done.")
