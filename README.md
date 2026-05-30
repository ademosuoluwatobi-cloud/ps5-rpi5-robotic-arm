# PS5 Raspberry Pi 5 Robotic Arm

This project controls a 6DOF robotic arm using a PS5 DualSense controller, Raspberry Pi 5, Arduino Nano, USB serial communication, and servo motors.

## Project Flow

```text
PS5 Controller → Raspberry Pi 5 → USB Serial → Arduino Nano → Servo Shield → 6DOF Robotic Arm

Current Features
PS5 controller paired to Raspberry Pi 5 over Bluetooth
Raspberry Pi reads PS5 joystick and button inputs using Python/Pygame
Raspberry Pi sends serial command bytes to Arduino Nano through /dev/ttyUSB0
Arduino Nano controls six robotic arm servos
Includes deadzone, debounce, command hold, rate limiting, and emergency stop logic
Final Control Layout
PS5 ControlArm Action
L1 / R1Servo 1 base left/right
Left stick left/rightServo 4 up/down
Left stick up/downServo 2 up/down
Right stick left/rightServo 5 left/right
Right stick up/downServo 3 up/down
X / CircleGripper open/close
TriangleEmergency stop
Hardware Used
Raspberry Pi 5
PS5 DualSense controller
Arduino Nano
6DOF aluminium robotic arm
Servo expansion shield
External servo power supply
USB cable from Raspberry Pi to Arduino Nano
Future Upgrade

The next stage is to mount the robotic arm on a mobile robot car using an L298N motor driver and another Arduino. The same PS5 controller can control both the robotic arm and the car through the Raspberry Pi 5.

Author

Ademosu Oluwatobi
