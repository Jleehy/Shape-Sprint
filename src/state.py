"""
state.py
Description:
    Defines an abstract base class for game states.
Programmers:
    Steve Gan
    Sean Hammell
    Jacob Leehy
    Mario Simental
    Matthew Sullivan
Created:
    Oct 23, 2024
Revisions:
    Oct 27th, 2024: Finalized prologue comments - Sean Hammell
Preconditions:
    None.
Postconditions:
    None.
Error Conditions:
    None.
Side Effects:
    None.
Invariants:
    None.
Known Faults:
    None.
"""


# State is an abstract base class. This definition is meant to give the Engine class
# visibility of the update and draw methods.
class State:
    def update(self):
        pass

    def draw(self):
        pass
