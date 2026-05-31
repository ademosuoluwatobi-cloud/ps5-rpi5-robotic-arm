import serial
import time

PORT = "/dev/ttyUSB0"
BAUD = 9600

print("Opening Arduino Nano on", PORT)

ser = serial.Serial(PORT, BAUD, timeout=1)
time.sleep(2)

print("Sending command 19...")
ser.write(bytes([19]))
time.sleep(0.5)

print("Stopping...")
ser.write(bytes([0]))

ser.close()
print("Done.")
