"""
keyboard.py
Description: Keyboard class
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


class Keyboard:
    def __init__(self):
        """
        Initializes a Keyboard object.
        """
        # Create a set to track which keys are down.
        self._keys = {}

    def is_key_down(self, key):
        """
        Returns if a key is down.
        """
        # Note that the get method will return False if the key is not in the dict.
        return self._keys.get(key)

    def set_key_down(self, key, is_down):
        """
        Records if a key is down.
        """
        self._keys[key] = is_down
