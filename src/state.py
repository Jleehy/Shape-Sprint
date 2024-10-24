"""
state.py
Description: State class
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


# State is an abstract base class. This definition is meant to give the Engine class
# visibility of the update and draw methods.
class State:
    def update(self):
        pass

    def draw(self):
        pass
