"""
audio.py
Description:
    Provides functionality for loading, playing, and pausing music.
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
    Nov 10, 2024: Added volume up and volume down - Steve Gan
    Nov 24, 2024: Fixed bugs with music volume up and down - Steve Gan
Preconditions:
    The Pygame library is initialized.
    The file passed to set_music is a valid .ogg or .wav file.
Postconditions:
    The music is available to play, pause, unpause, increase or decrease the volume.
Error Conditions:
    set_music will raise an exception if the music file is invalid or missing.
    play_music, pause_music, and unpause_music will raise an exception if there is not
        a valid music file loaded.
Side Effects:
    None.
Invariants:
    There can never be more than a single music file loaded at a time.
Known Faults:
    None.
"""

import pygame

mus_vol = .05


def set_music(file):
    """
    Sets the music.
    """
    # Load the music file.
    pygame.mixer.music.load(file)
    pygame.mixer.music.set_volume(mus_vol)


def play_music():
    """
    Begins playing the music.
    """
    pygame.mixer.music.play(-1)


def pause_music():
    """
    Pauses the music.
    """
    pygame.mixer.music.pause()


def unpause_music():
    """
    Unpauses the music.
    """
    pygame.mixer.music.unpause()


def volume_up():
    """
    Turns music volume up
    """
    global mus_vol
    mus_vol = min(mus_vol + 0.1, 1.0)
    pygame.mixer.music.set_volume(mus_vol)

def volume_down():
    """
    Turns music volume down
    """
    global mus_vol
    mus_vol = max(mus_vol - 0.1, 0.0)
    pygame.mixer.music.set_volume(mus_vol)