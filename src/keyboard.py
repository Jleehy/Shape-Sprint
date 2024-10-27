"""
keyboard.py
Description:
    Provides getting and setting the pressed state of keyboard keys.
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
    The key parameter of is_key_down and set_key_down is a Pygame key constant.
    is_down is a boolean.
Postconditions:
    The pressed state of a given key is recorded in the _keys dict.
Error Conditions:
    None.
Side Effects:
    None.
Invariants:
    There will never be more than one dict entry for a given key.
Known Faults:
    None.
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
