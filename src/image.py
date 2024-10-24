"""
image.py
Description: Image class
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

import pygame

from engine import Engine, engine_instance


class Image:
    def __init__(self, file):
        """
        Initializes an Image object.
        """
        # Load the image file.
        self._image = pygame.image.load(file)

    def blit(self, x, y):
        """
        Draws the Image to the screen.
        """
        engine_instance.screen.blit(self._image, self._image.get_rect(x=x, y=y))
