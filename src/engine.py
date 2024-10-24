"""
engine.py
Description: Engine class
Programmers:
    Steve Gan
    Sean Hammell
    Jacob Leehy
    Mario Simental
    Matthew Sullivan
Created: Oct 23, 2024
Revisions:
Preconditions:
Postconditions:
Error Conditions:
Side Effects:
Invariants:
Known Faults:
"""

import sys

import pygame

from keyboard import Keyboard
from state import State


class Engine:
    def __init__(self):
        """
        Initializes an Engine object.
        """
        # Initialize pygame.
        pygame.init()

        # Create an 800x600 window with the title "Shape Sprint".
        pygame.display.set_caption("Shape Sprint")
        self.screen = pygame.display.set_mode((800, 600), flags=pygame.SCALED, vsync=1)

        # Start with an empty state.
        self.state = State()

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

            # Cap the FPS at 75.
            clock.tick(75)


# Global Engine instance.
engine_instance = Engine()
