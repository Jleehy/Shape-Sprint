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
    Nov 24, 2024: Added the ability to change keybinds - Steve Gan
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
import pygame

class Keyboard:
    def __init__(self):
        """
        Initializes a Keyboard object.
        """
        # Create a set to track which keys are down.
        self._keys = {}
        self._bindings = {  # Default key bindings
            "down": pygame.K_DOWN,
            "up": pygame.K_UP,
            "left": pygame.K_LEFT,
            "right": pygame.K_RIGHT,
            "select": pygame.K_RETURN,
            "esc": pygame.K_ESCAPE,

        }


    #def is_key_down(self, key):
        """
        Returns if a key is down.
        """
        # Note that the get method will return False if the key is not in the dict.
        #return self._keys.get(key)

    def is_key_down(self, action):
        """
        Checks if the key bound to an action is down.
        """
        key = self._bindings.get(action)
        return self._keys.get(key, False)    

    def set_key_down(self, key, is_down):
        """
        Records if a key is down.
        """
        self._keys[key] = is_down

    def set_WASD(self):
        """
        sets keybinds to WASD
        """
        self._bindings["up"] = pygame.K_w
        self._bindings["left"] = pygame.K_a
        self._bindings["down"] = pygame.K_s
        self._bindings["right"] = pygame.K_d

    def set_Arrows(self):
        """
        sets keybinds to WASD
        """
        self._bindings["up"] = pygame.K_UP
        self._bindings["left"] = pygame.K_LEFT
        self._bindings["down"] = pygame.K_DOWN
        self._bindings["right"] = pygame.K_RIGHT
