import os
import time
import pygame

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("No controller found.")
    raise SystemExit

pad = pygame.joystick.Joystick(0)
pad.init()

print("Controller:", pad.get_name())
print("Axes:", pad.get_numaxes())
print("Buttons:", pad.get_numbuttons())
print("Hats:", pad.get_numhats())
print()
print("Move ONE stick or press ONE button at a time.")
print("Write down which axis/button changes.")
print("Press CTRL+C to stop.")
print()

old_axes = [0] * pad.get_numaxes()
old_buttons = [0] * pad.get_numbuttons()
old_hats = [(0, 0)] * pad.get_numhats()

try:
    while True:
        pygame.event.pump()

        for i in range(pad.get_numaxes()):
            val = round(pad.get_axis(i), 2)
            if abs(val - old_axes[i]) > 0.15:
                print(f"AXIS {i}: {val}")
                old_axes[i] = val

        for i in range(pad.get_numbuttons()):
            val = pad.get_button(i)
            if val != old_buttons[i]:
                state = "PRESSED" if val else "released"
                print(f"BUTTON {i}: {state}")
                old_buttons[i] = val

        for i in range(pad.get_numhats()):
            val = pad.get_hat(i)
            if val != old_hats[i]:
                print(f"HAT {i}: {val}")
                old_hats[i] = val

        time.sleep(0.05)

except KeyboardInterrupt:
    print("\nStopped.")
