"""
image.py
Description:
    Provides a wrapper around a pygame.image object.
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
Preconditions:
    The Pygame library is initialized.
    The file passed to the constructor is a valid image file
        (https://www.pygame.org/docs/ref/image.html)
Postconditions:
    An image is available to draw to the screen.
Error Conditions:
    __init__ will raise an exception if the image file is invalid or missing.
Side Effects:
    None.
Invariants:
    None.
Known Faults:
    None.
"""

import pygame

from engine import engine_instance


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
