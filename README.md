# PS5-Controlled 6DOF Robotic Arm Using Raspberry Pi 5 (and Arduino Nano)

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Arduino](https://img.shields.io/badge/Arduino-Nano-teal)
![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-5-red)
![Controller](https://img.shields.io/badge/Controller-PS5%20DualSense-purple)
![Status](https://img.shields.io/badge/Status-Working%20Prototype-brightgreen)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

A practical robotics project for controlling a **6DOF servo robotic arm** using a **PS5 DualSense controller**, **Raspberry Pi 5**, **Arduino Nano**, **Python**, **Pygame**, **PySerial**, and **USB serial communication**.

The Raspberry Pi 5 reads the PS5 controller over Bluetooth, then sends command bytes to the Arduino Nano. The Arduino Nano receives those commands and moves the robotic arm servos.

```text
PS5 Controller → Raspberry Pi 5 → Arduino Nano → Servo Robotic Arm
```

---

## Demo Video

Click the image below to watch the demo on YouTube:

[![Watch the demo](https://img.youtube.com/vi/5xndhy3pLp8/0.jpg)](https://youtu.be/5xndhy3pLp8)

---

## Table of Contents

1. [Overview](#1-overview)
2. [Things](#2-things)
3. [Story](#3-story)
4. [System Overview](#4-system-overview)
5. [Hardware Architecture](#5-hardware-architecture)
6. [Setting up the Robotic Arm Kit](#6-setting-up-the-robotic-arm-kit)
7. [Setting up the Arduino Nano](#7-setting-up-the-arduino-nano)
8. [Setting up VS Code for Raspberry Pi 5](#8-setting-up-vs-code-for-raspberry-pi-5)
9. [Pairing the PS5 Controller](#9-pairing-the-ps5-controller)
10. [Mapping the PS5 Gamepad Controls](#10-mapping-the-ps5-gamepad-controls)
11. [Testing Raspberry Pi to Arduino Serial Communication](#11-testing-raspberry-pi-to-arduino-serial-communication)
12. [Raising Your Arm: PS5 Control of the Robotic Arm](#12-raising-your-arm-ps5-control-of-the-robotic-arm)
13. [Final Control Layout](#13-final-control-layout)
14. [The Nitty-Gritty](#14-the-nitty-gritty)
15. [Troubleshooting and Lessons Learned](#15-troubleshooting-and-lessons-learned)
16. [Future Upgrade: Mounting the Arm on an L298N Robot Car](#16-future-upgrade-mounting-the-arm-on-an-l298n-robot-car)
17. [Some Useful References](#17-some-useful-references)
18. [Schematics](#18-schematics)
19. [Code](#19-code)
20. [Credits](#20-credits)
21. [Comments](#21-comments)

---

## 1. Overview

In this project, you will learn how to control a 6DOF robotic arm using a PS5 DualSense controller, a Raspberry Pi 5, and an Arduino Nano.

The PS5 controller connects to the Raspberry Pi 5 through Bluetooth. The Raspberry Pi reads the joystick and button values using Python, then sends simple command numbers to the Arduino Nano through USB serial communication. The Arduino Nano receives those command numbers and moves the correct servo on the robotic arm.

So the full control path looks like this:

```text
PS5 Controller → Raspberry Pi 5 → Arduino Nano → Servo Robotic Arm
```

This project is a good starting point if you want to understand how gamepad teleoperation works in robotics. Instead of controlling the arm from a phone app or directly from Arduino buttons, you will control it with a proper game controller, just like a small robotic manipulation system.

In this version, the focus is only on the robotic arm. Later, the same setup can be extended to control a robot car using an L298N motor driver. That means the PS5 controller can eventually control both the robotic arm and the mobile base.

---

## 2. Things

Before starting, gather the main parts and tools.

### Hardware components

You will need:

* Raspberry Pi 5
* Arduino Nano
* PS5 DualSense controller
* 6DOF aluminium servo robotic arm
* Arduino Nano servo expansion board or servo shield
* 6 servo motors
* External servo power supply
* USB cable for Arduino Nano
* Raspberry Pi 5 power supply
* microSD card with Raspberry Pi OS
* Jumper wires where necessary

### Software and tools

You will also need:

* Raspberry Pi OS
* Python 3
* Pygame
* PySerial
* Arduino IDE
* Arduino Servo library
* Visual Studio Code
* VS Code Remote - SSH extension
* Git
* GitHub for code hosting
* Hackster.io or Instructables for project documentation

### Optional parts for future upgrade

For the next version, where the arm will be mounted on a robot car, you may also need:

* Arduino Uno
* L298N motor driver
* Robot car chassis
* DC motors
* Motor battery
* Extra USB cable or serial connection

---

## 3. Story

I started this project because I wanted a more practical and interesting way to control my robotic arm.

The robotic arm already had servos, brackets, a gripper, and an Arduino Nano servo shield. It could move, but I did not want to control it in a basic way. I wanted something closer to how real robotic systems are controlled — using a joystick or gamepad.

Since I had a PS5 controller and a Raspberry Pi 5, the idea was to use the PS5 controller as the main input device. The Raspberry Pi would read the controller, then send movement commands to the Arduino Nano. The Arduino Nano would then handle the servo movement.

I looked at older projects where Xbox controllers were used with Raspberry Pi and Arduino. Those projects helped me understand the basic idea, but my own setup was different. I was using a PS5 controller, Raspberry Pi 5, and Arduino Nano.

So instead of copying everything directly, I rebuilt the process step by step.

First, I set up the Raspberry Pi 5 in headless mode. Then I used VS Code with the Remote - SSH extension to connect to the Pi. This made the workflow much easier because I could edit the Python files directly from VS Code while still running the code on the Raspberry Pi.

After that, I paired the PS5 controller with the Raspberry Pi through Bluetooth.

Once the controller was working, I connected the Arduino Nano to the Raspberry Pi using USB. The Nano appeared as `/dev/ttyUSB0`, which confirmed that the Raspberry Pi could see it.

The robotic arm’s original Arduino code was designed to receive commands through an HC-05 Bluetooth module. For this project, that was not needed anymore, because the Raspberry Pi was already handling the Bluetooth connection from the PS5 controller. So I changed the Arduino code to receive commands directly from USB serial.

When I sent the first test command from the Raspberry Pi and one servo moved, that confirmed the main control chain was working.

From there, I mapped the PS5 controller buttons, mapped the Arduino command numbers, tested the movement of each servo, and finally wrote a stable Python control script.

---

## 4. System Overview

The system has four main parts:

```text
1. PS5 DualSense controller
2. Raspberry Pi 5
3. Arduino Nano
4. 6DOF robotic arm
```

The PS5 controller does not connect directly to the Arduino. Instead, it connects to the Raspberry Pi through Bluetooth.

The Raspberry Pi runs a Python script. That script reads the PS5 controller input, decides which command should be sent, and sends the command to the Arduino Nano over USB serial.

The Arduino Nano receives the command and moves the correct servo.

Here is the basic system flow:

```text
PS5 DualSense Controller
        ↓ Bluetooth
Raspberry Pi 5
        ↓ USB Serial
Arduino Nano
        ↓ Servo Signals
6DOF Robotic Arm
```

This setup works well because the Raspberry Pi is better for reading Bluetooth controller input and running Python logic, while the Arduino Nano is better for generating stable servo control signals.

In simple terms:

```text
Raspberry Pi = brain and controller reader
Arduino Nano = servo driver
PS5 controller = human input device
Robotic arm = output system
```

---

## 5. Hardware Architecture

The hardware is divided into two important parts:

```text
1. Signal/control connection
2. Power connection
```

The signal connection is responsible for sending commands. The power connection is responsible for supplying enough current to the servos.

The Raspberry Pi 5 is powered through its USB-C power supply. The Arduino Nano is connected to the Raspberry Pi through a USB cable. This USB cable is used for serial communication and also powers the logic side of the Arduino Nano.

However, do not power the servos from the Raspberry Pi or from the Nano USB line. Servo motors can draw a lot of current, especially when many joints move or when the arm is carrying load. If you power the servos from the wrong source, the arm may shake, reset, or behave strangely.

The correct power idea is:

```text
Raspberry Pi 5 power supply → Raspberry Pi only

Raspberry Pi USB port → Arduino Nano logic and serial communication

External servo power supply → Servo shield and servo motors
```

The hardware connection looks like this:

```text
Raspberry Pi 5 USB port
        ↓
Arduino Nano USB port
        ↓
Servo expansion board
        ↓
6 servo motors
```

The external power supply should feed the servo power rail on the servo board. Make sure the servo power supply is suitable for your servos.

---

## 6. Setting up the Robotic Arm Kit

Start by assembling the robotic arm carefully.

This project uses a 6DOF aluminium servo robotic arm. The arm has several servo joints and a two-finger gripper. Your own arm may look slightly different, but the idea is the same: each servo controls one joint or part of the arm.

When building the arm, don’t rush the mechanical part. A wrongly aligned servo horn can make the arm move badly or hit its mechanical limit too early.

Here are a few useful tips:

* Fix the servo horns carefully.
* Do not force any joint by hand.
* Keep the arm near a neutral position before testing.
* Make sure wires are not trapped between brackets.
* Do not overtighten rotating joints.
* Make sure the gripper can open and close freely.
* Check each joint gently before applying full power.

After assembling the arm, the next thing is to know what each command does. This is very important because the Arduino code uses command numbers, but you need to know which command moves which servo.

With the arm facing me, this was the command mapping I got:

```text
18 = Servo 5 right
19 = Servo 5 left

20 = Servo 3 up
21 = Servo 3 down

22 = Servo 6 gripper close
23 = Servo 6 gripper open

24 = Servo 2 up
25 = Servo 2 down

26 = Servo 1 base left
27 = Servo 1 base right

16 = Servo 4 up
17 = Servo 4 down
```

Your own servo direction may differ depending on how the arm was assembled, so it is always good to test one command at a time.

---

## 7. Setting up the Arduino Nano

The Arduino Nano controls the servos.

In the original robotic arm setup, the Arduino code was designed to receive commands from an HC-05 Bluetooth module using `SoftwareSerial`.

For this project, we do not need the HC-05 module. The PS5 controller already connects to the Raspberry Pi through Bluetooth, so the Raspberry Pi will send commands to the Arduino Nano through USB.

That means we need to change the Arduino input method from Bluetooth serial to normal USB serial.

The old idea looked like this:

```cpp
#include <SoftwareSerial.h>
SoftwareSerial Bluetooth(3, 2);

Bluetooth.begin(9600);
dataIn = Bluetooth.read();
```

For this project, change it to:

```cpp
Serial.begin(9600);
dataIn = Serial.read();
```

So anywhere the old code uses:

```cpp
Bluetooth.available()
Bluetooth.read()
```

replace it with:

```cpp
Serial.available()
Serial.read()
```

This allows the Arduino Nano to receive command bytes directly from the Raspberry Pi through USB.

After editing the code, upload it to the Arduino Nano using the Arduino IDE.

If you are using an Arduino Nano clone, you may need to select:

```text
Board: Arduino Nano
Processor: ATmega328P (Old Bootloader)
```

After uploading the sketch, disconnect the Nano from your laptop and connect it to the Raspberry Pi 5.

---

## 8. Setting up VS Code for Raspberry Pi 5

For this project, VS Code is the main working environment.

Instead of opening a separate terminal tool and jumping between different windows, you can use VS Code to connect directly to the Raspberry Pi, edit your files, open the Pi terminal, and run the project from one place.

### Install VS Code

Install Visual Studio Code on your laptop.

After installing VS Code, open it and install the **Remote - SSH** extension.

In VS Code:

```text
Extensions → Search “Remote - SSH” → Install
```

This extension allows VS Code to connect to the Raspberry Pi through SSH.

### Prepare the Raspberry Pi for headless use

The Raspberry Pi 5 was used in headless mode. That means I did not need a monitor or keyboard connected to the Pi during normal use.

I prepared the microSD card using Raspberry Pi Imager. During the setup, I enabled SSH and configured the Wi-Fi.

The important settings were:

```text
Hostname: raspberrypi
Username: pi
SSH: Enabled
SSH authentication: Password authentication
Wi-Fi: Configured
```

After inserting the SD card into the Raspberry Pi and powering it on, wait a few minutes for it to boot.

### Connect VS Code to the Raspberry Pi

In VS Code, press:

```text
Ctrl + Shift + P
```

Then search for:

```text
Remote-SSH: Connect to Host
```

When VS Code asks for the SSH address, enter:

```text
pi@raspberrypi.local
```

If it asks for the platform, select:

```text
Linux
```

Then enter your Raspberry Pi password.

Once the connection is successful, VS Code will open a new window connected to the Raspberry Pi.

You can confirm you are inside the Raspberry Pi by opening the VS Code terminal:

```text
Terminal → New Terminal
```

The terminal should show something like:

```bash
pi@raspberrypi:~ $
```

That means your VS Code terminal is running directly on the Raspberry Pi.

### Open the project folder

Inside the VS Code terminal connected to the Pi, create and open the project folder:

```bash
mkdir -p ~/ps5_arm
cd ~/ps5_arm
```

In VS Code, you can also open the folder through:

```text
File → Open Folder → /home/pi/ps5_arm
```

Now all the Python files can be created and edited directly inside VS Code.

### Update the Raspberry Pi

In the VS Code terminal, run:

```bash
sudo apt update
sudo apt full-upgrade -y
```

Then install the required packages:

```bash
sudo apt install -y python3-pip python3-venv python3-serial python3-pygame joystick evtest bluetooth bluez git
```

These packages are needed because:

```text
python3-serial  → allows Python to talk to Arduino through serial
python3-pygame  → reads the PS5 controller
joystick        → provides jstest for controller testing
bluetooth/bluez → handles Bluetooth pairing
git             → useful for version control
```

From this point, all project commands should be run inside the VS Code terminal connected to the Raspberry Pi.

---

## 9. Pairing the PS5 Controller

Now pair the PS5 controller with the Raspberry Pi.

In the VS Code terminal connected to the Raspberry Pi, check that Bluetooth is running:

```bash
sudo systemctl status bluetooth
```

If it is active and running, continue.

Open the Bluetooth control tool:

```bash
bluetoothctl
```

Inside `bluetoothctl`, run:

```bash
power on
agent on
default-agent
scan on
```

Now put the PS5 controller in pairing mode. Hold:

```text
PS button + Create button
```

Hold both until the controller light starts blinking.

When the controller appears in the Bluetooth scan, pair and connect it:

```bash
pair XX:XX:XX:XX:XX:XX
trust XX:XX:XX:XX:XX:XX
connect XX:XX:XX:XX:XX:XX
quit
```

Replace `XX:XX:XX:XX:XX:XX` with the MAC address shown on your screen.

After pairing, check the joystick device:

```bash
ls /dev/input/js*
```

In this project, the PS5 controller appeared as:

```text
/dev/input/js0
```

Then test it:

```bash
jstest /dev/input/js0
```

Move the sticks and press the buttons. If the numbers change, the controller is working.

---

## 10. Mapping the PS5 Gamepad Controls

Do not assume the PS5 button numbers. Always test them.

The controller mapping can vary depending on how Linux reads the controller. So before writing the final control script, map every stick and button.

You can create a mapping script in VS Code.

Inside your `/home/pi/ps5_arm` folder, create a file named:

```text
map_ps5.py
```

Use that script to identify the button and axis numbers.

In this project, the confirmed PS5 mapping was:

```text
Left stick X  = Axis 0
Left stick Y  = Axis 1
Right stick X = Axis 3
Right stick Y = Axis 4
```

The direction values were:

```text
Left stick left  = Axis 0 negative
Left stick right = Axis 0 positive
Left stick up    = Axis 1 negative
Left stick down  = Axis 1 positive

Right stick left  = Axis 3 negative
Right stick right = Axis 3 positive
Right stick up    = Axis 4 negative
Right stick down  = Axis 4 positive
```

The button mapping was:

```text
X / Cross = Button 0
Circle    = Button 1
Triangle  = Button 2
Square    = Button 3

L1 = Button 4
R1 = Button 5

L2 = Button 6 and Axis 2
R2 = Button 7 and Axis 5

PS button = Button 10
Left stick press / L3 = Button 11
Right stick press / R3 = Button 12

Touchpad click = No input detected
```

The D-pad was mapped as HAT 0:

```text
D-pad up    = (0, 1)
D-pad down  = (0, -1)
D-pad left  = (-1, 0)
D-pad right = (1, 0)
Released    = (0, 0)
```

This mapping is what made the final control script accurate.

---

## 11. Testing Raspberry Pi to Arduino Serial Communication

Before joining the PS5 controller and the robotic arm together, first test if the Raspberry Pi can talk to the Arduino Nano.

Connect the Arduino Nano to the Raspberry Pi using USB.

In the VS Code terminal connected to the Raspberry Pi, run:

```bash
python3 -m serial.tools.list_ports
```

The output showed:

```text
/dev/ttyAMA10
/dev/ttyUSB0
2 ports found
```

The important one is:

```text
/dev/ttyUSB0
```

That is the Arduino Nano.

Now create a small test script in VS Code to send one command to the Nano.

Create a file named:

```text
arduino_test.py
```

Use this basic test:

```python
import serial
import time

PORT = "/dev/ttyUSB0"
BAUD = 9600

ser = serial.Serial(PORT, BAUD, timeout=1)
time.sleep(2)

ser.write(bytes([19]))
time.sleep(0.5)

ser.write(bytes([0]))
ser.close()
```

The important part is this:

```python
ser.write(bytes([19]))
```

Do not send:

```python
ser.write(b"19")
```

`bytes([19])` sends the actual command number `19`.

`b"19"` sends the text characters `1` and `9`, which is not what the Arduino expects.

When the servo moved during this test, that confirmed the Raspberry Pi to Arduino Nano communication was working.

---

## 12. Raising Your Arm: PS5 Control of the Robotic Arm

Now that the controller and Arduino serial communication are working separately, it is time to combine them.

The Raspberry Pi Python script will:

```text
1. Read the PS5 controller
2. Check which button or joystick is active
3. Convert that input into an Arduino command number
4. Send the command to the Arduino Nano through USB serial
5. Stop the arm when no command is active
```

In VS Code, create the final Python file:

```text
ps5_to_arm_final.py
```

This is the main file that joins the PS5 controller, Raspberry Pi, Arduino Nano, and robotic arm together.

At first, direct control worked, but I noticed one issue: when buttons were pressed too fast, the input could fluctuate. That can make a robotic arm jerk or behave unpredictably.

To make the movement more stable, the final script includes:

```text
Deadzone
Debounce
Command hold
Rate limiting
Emergency stop
```

The deadzone ignores small joystick noise.

The debounce helps prevent quick button flicker.

The command hold makes sure the command remains stable for a short time.

The rate limit prevents the Raspberry Pi from sending commands too fast.

The emergency stop sends command `0` to stop the arm.

This made the control much better and safer.

---

## 13. Final Control Layout

After testing different control layouts, I preferred putting the base servo on L1 and R1.

This made the base easier to control, especially when it approached its movement limit.

The final control layout is:

```text
L1 / R1                 = Servo 1 base left/right

Left stick left/right   = Servo 4 up/down
Left stick up/down      = Servo 2 up/down

Right stick left/right  = Servo 5 left/right
Right stick up/down     = Servo 3 up/down

X / Circle              = Gripper open/close
Triangle                = Emergency stop
CTRL + C                = Stop program safely
```

The command mapping behind the layout is:

```text
L1  → Base left  → Command 26
R1  → Base right → Command 27

Left stick left/right → Servo 4 → Commands 16 / 17
Left stick up/down    → Servo 2 → Commands 24 / 25

Right stick left/right → Servo 5 → Commands 19 / 18
Right stick up/down    → Servo 3 → Commands 20 / 21

X      → Gripper open  → Command 23
Circle → Gripper close → Command 22

Triangle → Stop → Command 0
```

This control layout is not compulsory. You can change it to fit your own hand preference, but this version worked well for my setup.

---

## 14. The Nitty-Gritty

The Python script sends only one movement command at a time.

That is intentional.

If the script tries to move too many joints at once, the arm may become harder to control, and the power demand may increase. For a first version, one command at a time is safer and easier to debug.

The deadzone is set like this:

```python
DEADZONE = 0.45
```

This means the joystick must move beyond `0.45` or below `-0.45` before the script accepts it as a real movement.

The debounce time is:

```python
DEBOUNCE_TIME = 0.10
```

That means the input must remain stable for about 100 milliseconds before the command is accepted.

The send interval is:

```python
SEND_INTERVAL = 0.10
```

This means the Raspberry Pi sends commands every 100 milliseconds instead of flooding the Arduino Nano.

The Arduino command system is simple:

```text
Command number sent from Pi → Arduino reads it → Arduino moves servo
```

For example:

```text
26 = base left
27 = base right
22 = gripper close
23 = gripper open
```

This method is simple, but it is also flexible. Later, if you add a car base, you can create another set of command numbers for the car.

---

## 15. Troubleshooting and Lessons Learned

Here are some of the issues I faced and how they were solved.

### VS Code Remote SSH setup

The smoothest workflow was using VS Code with Remote - SSH. Once VS Code connected to the Raspberry Pi, I could edit files and run commands inside the same environment.

The important thing is to confirm that the VS Code terminal is actually connected to the Raspberry Pi.

You should see:

```bash
pi@raspberrypi:~ $
```

If you see that, you are running commands directly on the Pi.

### Raspberry Pi password issue

Since the Pi was used headless, SSH had to be enabled from Raspberry Pi Imager. The username and password also had to be set correctly during flashing.

### Finding the Arduino Nano

The Arduino Nano appeared as:

```text
/dev/ttyUSB0
```

That became the serial port used in the Python script.

### PS5 controller mapping

The PS5 controller mapping was not guessed. Each button and joystick axis was tested manually.

### Fast button fluctuation

Fast button presses caused some fluctuation. This was handled with debounce, command hold, and rate limiting.

### Servo limit issue

When the base servo reached around 180 degrees, it sometimes stopped responding as expected. A better future improvement is to clamp the servo position directly in the Arduino code so it never goes outside its safe range.

### Servo power

The servos must use an external power supply. Do not power them directly from the Raspberry Pi or Nano USB port.

---

## 16. Future Upgrade: Mounting the Arm on an L298N Robot Car

The next upgrade is to mount the robotic arm on a robot car chassis.

The car can be controlled using:

```text
Arduino Uno
L298N motor driver
DC motors
Motor battery
Robot chassis
```

The same PS5 controller can control both the robotic arm and the car.

The future system can look like this:

```text
PS5 Controller
        ↓ Bluetooth
Raspberry Pi 5
        ↓ USB Serial 1
Arduino Nano → Robotic Arm

Raspberry Pi 5
        ↓ USB Serial 2
Arduino Uno → L298N Motor Driver → Robot Car
```

The Raspberry Pi will act as the main controller. It will read the PS5 controller and decide whether the command should go to the robotic arm or to the car.

A simple future control idea is:

```text
Joysticks = robotic arm
D-pad = car movement
L2 / R2 = speed control
Triangle = emergency stop
Square = switch mode
```

Another option is to use one mode for the arm and another mode for the car. That will make the control cleaner and prevent command clashes.

---

## 17. Some Useful References

These references are useful if you want to understand or extend the project:

* Raspberry Pi documentation
* VS Code Remote - SSH documentation
* Pygame joystick documentation
* Python PySerial documentation
* Arduino Servo library documentation
* Linux joystick input tools
* Hackster.io robotic arm controller examples
* GitHub project repository

Older Xbox controller robot arm projects helped with the general idea of using a Raspberry Pi as a bridge between a gamepad and Arduino.

This project builds on that idea, but adapts it for:

```text
PS5 controller
Raspberry Pi 5
Arduino Nano
USB serial communication
6DOF aluminium robotic arm
VS Code Remote SSH workflow
```

---

## 18. Schematics

### Main System Block Diagram

The main block diagram shows how the PS5 controller, Raspberry Pi 5, Arduino Nano, and robotic arm communicate with one another.

<p align="center">
  <img src="images/111.png" alt="PS5 Raspberry Pi 5 Arduino Nano Robotic Arm Block Diagram" width="800">
</p>

### Power diagram

```text
Raspberry Pi 5 power supply
        ↓
Raspberry Pi 5

Raspberry Pi USB port
        ↓
Arduino Nano logic and serial communication

External servo power supply
        ↓
Servo expansion board
        ↓
Servo motors
```

### VS Code workflow diagram

```text
Laptop running VS Code
        ↓ Remote - SSH
Raspberry Pi 5
        ↓ Python scripts
Arduino Nano
        ↓ Servo commands
Robotic Arm
```

### Future car expansion diagram

```text
PS5 Controller
        ↓ Bluetooth
Raspberry Pi 5
        ↓ USB Serial
Arduino Nano → Robotic Arm

Raspberry Pi 5
        ↓ USB Serial
Arduino Uno → L298N → DC motors
```

---

## 19. Code

The code is divided into two main parts.

### Raspberry Pi Python code

File:

```text
raspberry-pi/ps5_to_arm_final.py
```

This script reads the PS5 controller, applies deadzone and debounce, then sends command numbers to the Arduino Nano through `/dev/ttyUSB0`.

It handles:

```text
PS5 joystick input
PS5 button input
Emergency stop
Serial communication
Command stability
```

### Arduino Nano code

File:

```text
arduino/24G6_fixed_USB_SERIAL.ino
```

This Arduino sketch receives command numbers through USB serial and moves the correct servo.

It replaces the old HC-05 Bluetooth input with USB serial input.

### Testing scripts

These test scripts are helpful:

```text
ps5_test.py
map_ps5.py
arduino_test.py
map_arm.py
```

Use `ps5_test.py` to confirm that Python can read the controller.

Use `map_ps5.py` to find the real button and axis numbers.

Use `arduino_test.py` to confirm that the Raspberry Pi can send serial commands to the Arduino Nano.

Use `map_arm.py` to test each Arduino command and see which servo moves.

All Python files can be created, edited, and run directly from VS Code after connecting to the Raspberry Pi through Remote - SSH.

---

## 20. Credits

This project was built and tested by Ademosu Oluwatobi using a Raspberry Pi 5, Arduino Nano, PS5 DualSense controller, and a 6DOF aluminium servo robotic arm.

The idea was inspired by earlier gamepad-controlled robotic arm projects, especially projects that used a Raspberry Pi as a bridge between a controller and Arduino.

This version was adapted and rebuilt for:

```text
PS5 DualSense controller
Raspberry Pi 5
Arduino Nano
USB serial control
6DOF servo robotic arm
VS Code Remote SSH workflow
```

It also serves as the foundation for a future mobile robotic arm project using an L298N robot car base.

---

## 21. Comments

This project proves that a PS5 controller can be used to control a robotic arm through a Raspberry Pi and Arduino Nano.

The most important milestone is that the full control chain works:

```text
PS5 Controller → Raspberry Pi 5 → Arduino Nano → Robotic Arm
```

VS Code made the workflow cleaner because the Raspberry Pi could be controlled remotely, while the code could still be edited like a normal development project.

There is still room to improve the project.

The next improvement is to mount the arm on a robot car and control both the car and arm with the same PS5 controller.

Another improvement is to modify the Arduino servo code so each servo angle is safely clamped between its minimum and maximum range. That will make the arm more predictable and safer near its movement limits.

For now, this version is a solid working base for PS5-controlled robotic arm teleoperation.
