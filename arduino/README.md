
Arduino Nano Sketch

This folder is for the Arduino Nano USB Serial servo-control sketch.

The Arduino Nano receives raw byte commands from the Raspberry Pi through USB serial, then moves the robotic arm servos according to the command mapping in docs/arm-command-mapping.md.

Main serial port on Raspberry Pi:

/dev/ttyUSB0

Baud rate:

9600

