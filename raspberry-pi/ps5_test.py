import os
import time
import pygame

# Allows pygame to run over SSH/headless
os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

pygame.init()
pygame.joystick.init()

count = pygame.joystick.get_count()
print("Controllers found:", count)

if count == 0:
    print("No controller detected.")
    raise SystemExit

pad = pygame.joystick.Joystick(0)
pad.init()

print("Controller name:", pad.get_name())
print("Axes:", pad.get_numaxes())
print("Buttons:", pad.get_numbuttons())
print("Hats:", pad.get_numhats())
print("Move sticks / press buttons. Press CTRL+C to stop.\n")

try:
    while True:
        pygame.event.pump()

        axes = []
        for i in range(pad.get_numaxes()):
            axes.append(round(pad.get_axis(i), 2))

        buttons = []
        for i in range(pad.get_numbuttons()):
            buttons.append(pad.get_button(i))

        hats = []
        for i in range(pad.get_numhats()):
            hats.append(pad.get_hat(i))

        print("Axes:", axes, "Buttons:", buttons, "Hats:", hats)
        time.sleep(0.2)

except KeyboardInterrupt:
    print("\nStopped.")
