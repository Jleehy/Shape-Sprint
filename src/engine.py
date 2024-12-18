"""
engine.py
Description:
    Serves as the main wrapper for the Pygame library and controls the game loop.
Programmers:
    Steve Gan
    Sean Hammell
    Jacob Leehy
    Mario Simental
    Matthew Sullivan
Created:
    Oct 23, 2024
Revisions:
    Oct 24, 2024: Modularized engine class - Matthew Sullivan
    Oct 27, 2024: Finalized prologue comments - Sean Hammell
    Nov 10, 2024: Fixed circular import dependency on states and engine. - Mario Simental
    Nov 23, 2024: Update resolution - Sean Hammell
    Dec 07, 2024: Moved screen resolution constants into engine.py - Sean Hammell
Preconditions:
    The Pygame library is available.
    The Keyboard class is defined.
    The State class is defined.
Postconditions:
    The Pygame library is initialized.
    The game window is visible.
    the game loop is running.
Error Conditions:
    None.
Side Effects:
    The Pygame library is initialized for all modules.
Invariants:
    None.
Known Faults:
    None.
"""

import sys

import pygame

from keyboard import Keyboard

SCREEN_WIDTH = 1600  # Screen width
SCREEN_HEIGHT = 800  # Screen height


class Engine:
    def __init__(self):
        """
        Initializes an Engine object.
        """
        # Initialize pygame.
        pygame.init()

        # Create an 1600x800 window with the title "Shape Sprint".
        pygame.display.set_caption("Shape Sprint")
        self.screen = pygame.display.set_mode((1600, 800), flags=pygame.SCALED, vsync=1)

        # Start with an empty state.
        self.state = None

        # Track key presses.
        self.keyboard = Keyboard()

    def run_loop(self):
        """
        Controls the game loop.
        """
        # Create a clock to cap the game's FPS.
        clock = pygame.time.Clock()

        while True:
            # Capture an events.
            for event in pygame.event.get():
                # Quit if the window is closed.
                if event.type == pygame.QUIT:
                    sys.exit()

                # Record the KEYDOWN event for the pressed key.
                if event.type == pygame.KEYDOWN:
                    self.keyboard.set_key_down(event.key, True)

                # Record the KEYUP event for the released key.
                if event.type == pygame.KEYUP:
                    self.keyboard.set_key_down(event.key, False)

            # Update the current state.
            self.state.update()

            # Draw the current state.
            self.screen.fill((64, 64, 64))
            self.state.draw()
            pygame.display.flip()

            # Cap the FPS at 60.
            clock.tick(60)


# Global Engine instance.
engine_instance = Engine()
