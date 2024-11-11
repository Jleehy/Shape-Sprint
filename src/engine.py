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
    Oct 27, 2024: Finalized prologue comments - Sean Hammell
    Nov 10, 2024: Fixed circular import dependency on states and engine. - Mario Simental
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

class Engine:
    def __init__(self):
        """
        Initializes an Engine object.
        """
        # Initialize pygame.
        pygame.init()

        # Create an 800x600 window with the title "Shape Sprint".
        pygame.display.set_caption("Shape Sprint")
        self.screen = pygame.display.set_mode((1600, 1200), flags=pygame.SCALED, vsync=1)

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

            # Cap the FPS at 75.
            clock.tick(75)


# Global Engine instance.
engine_instance = Engine()
