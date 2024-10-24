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


class SoundEffect:
    def __init__(self, file):
        """
        Initializes a SoundEffect object.
        """
        # Load the sound file.
        self._sound = pygame.mixer.Sound(file)

    def play(self):
        """
        Plays the SoundEffect.
        """
        pygame.mixer.Sound.play(self._sound)
