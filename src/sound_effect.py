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
    Nov 24, 2024: Added some code to allow the sound effect volume to be changed - Steve Gan
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

sfx_vol = .05


class SoundEffect:
    def __init__(self, file):
        """
        Initializes a SoundEffect object.
        """
        # Load the sound file.
        self._sound = pygame.mixer.Sound(file)
        self._sound.set_volume(sfx_vol)


    def play(self):
        """
        Plays the SoundEffect.
        """
        pygame.mixer.Sound.play(self._sound)

    def update_volume(self):
        """
        Updates the volume of this sound effect.
        """
        self._sound.set_volume(sfx_vol)

def sfx_volume_up():
    global sfx_vol
    sfx_vol = min(sfx_vol + 0.1, 1.0)  # Cap at 1.0

def sfx_volume_down():
    global sfx_vol
    sfx_vol = max(sfx_vol - 0.1, 0.0)  # Minimum 0.0
