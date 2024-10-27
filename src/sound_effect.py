"""
sound_effect.py
Description:
    Provides a wrapper around a pygame.sound object.
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
    The file passed to the constructor is a valid .ogg or .wav file.
Postconditions:
    A sound effect is available to play.
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
