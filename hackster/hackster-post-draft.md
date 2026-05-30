
Controlling a 6DOF Robotic Arm with a PS5 Controller, Raspberry Pi 5, and Arduino Nano
Overview

This project demonstrates how to control a 6DOF robotic arm using a PS5 DualSense controller. The PS5 controller connects to a Raspberry Pi 5 over Bluetooth. The Raspberry Pi reads the gamepad input using Python and sends serial commands to an Arduino Nano. The Arduino Nano then controls the servo motors of the robotic arm.

System Architecture
PS5 Controller → Raspberry Pi 5 → USB Serial → Arduino Nano → Servo Shield → Robotic Arm
Why This Project?

The aim was to build a simple and practical teleoperation system for a physical robotic arm. Instead of controlling the servos directly from the Raspberry Pi, the Raspberry Pi handles the controller input while the Arduino Nano handles servo control.

Hardware
Raspberry Pi 5
PS5 DualSense controller
Arduino Nano
6DOF aluminium robotic arm
Servo shield
External servo power supply
USB cable
Jumper wires
Software
Raspberry Pi OS
Python 3
Pygame
PySerial
Arduino IDE
Arduino Servo library
Control Mapping
PS5 ControlArm Action
L1 / R1Base left/right
Left stick left/rightServo 4 up/down
Left stick up/downServo 2 up/down
Right stick left/rightServo 5 left/right
Right stick up/downServo 3 up/down
X / CircleGripper open/close
TriangleEmergency stop
Safety Features

The Python script includes:

Joystick deadzone
Button debounce
Command hold
Serial rate limiting
Emergency stop

These help prevent unstable or fluctuating controller input from making the robotic arm jerk unnecessarily.

Future Work

The next stage is to mount the robotic arm on a mobile robot car using an L298N motor driver. The same PS5 controller can control both the robotic arm and the car by separating the controls or using mode switching.
