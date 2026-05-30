
Block Diagram
┌──────────────────────────┐
│   PS5 DualSense Gamepad  │
└─────────────┬────────────┘
              │ Bluetooth
              ▼
┌──────────────────────────┐
│      Raspberry Pi 5      │
│ Python + Pygame          │
│ Serial command sender    │
└─────────────┬────────────┘
              │ USB Serial
              │ /dev/ttyUSB0
              ▼
┌──────────────────────────┐
│      Arduino Nano        │
│ Serial command receiver  │
│ Servo control sketch     │
└─────────────┬────────────┘
              │ PWM signals
              ▼
┌──────────────────────────┐
│ Servo Shield + 6 Servos  │
│ 6DOF Robotic Arm         │
└──────────────────────────┘
Power Note

The Raspberry Pi and Arduino Nano should not power the servos directly. Use an external servo power supply for the robotic arm servos.
