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
Preconditions:
    The Pygame library is initialized.
    The file passed to set_music is a valid .ogg or .wav file.
Postconditions:
    The music is available to play, pause, and unpause.
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


def set_music(file):
    """
    Sets the music.
    """
    # Load the music file.
    pygame.mixer.music.load(file)


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
