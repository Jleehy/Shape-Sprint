"""
audio.py
Description: Audio functions
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


def set_music(file):
    """
    Sets the music.
    """
    # Load the music file.
    pygame.mixer.music_load(file)


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
