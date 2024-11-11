"""
main.py
Description:
    Serves as a testing ground for the initial implementation of a platform-style game with level progression,
    obstacles, checkpoints, and basic player control mechanics. The game simulates gravity, jumping, 
    object movement, collision detection, and platform interactions. It provides a main menu, pause functionality, 
    and level progression with checkpoints and a final end-of-level marker.
Programmers:
    Steve Gan
    Sean Hammell
    Jacob Leehy
    Mario Simental
    Matthew Sullivan
Created:
    Oct 23, 2024
Revisions:
    Oct 23, 2024: Added State class, SoundEffect class, Audio functions, Image class, Keyboard class, and Engine class - Sean Hammell
    Oct 24, 2024: Added jumping, gravity, and basic ground logic - Jacob Leehy
    Oct 24, 2024: Added game over state and transition on collision - Matthew Sullivan
    Oct 24, 2024: Added level state and implemented collision detection system - Matthew Sullivan
    Oct 24, 2024: Added an attribute to Object class for storing a rect object to support collision detection - Mario Simental 
    Oct 24, 2024: Further abstracted Cube, Ground, and Spike classes by creating an Object base class - Mario Simental 
    Oct 26, 2024: Added a top ground level for testing collision and movement flags for hazard detection - Mario Simental 
    Oct 26, 2024: Implemented collision detection between player and objects with clamping based on the object being collided with - Mario Simetnal
    Oct 26, 2024: Added level progression (scrolling screen) - Jacob Leehy
    Oct 27, 2024: Added checkpoints, game end, pause menu, platforms, and instructions - Jacob Leehy
    Oct 27, 2024: Cleaned up comments - Sean Hammell
    Nov 2, 2024: Created the opening menu, options menu, and level select menu. Made sure game loads into opening menu. - Steve Gan
    Nov 9, 2024: Split out Level and Object classes to separate files - Sean Hammell
    Nov 9, 2024: Create and implement background for all of the major menus - Jacob Leehy
    Nov 9, 2024: Remove left and right arrow key movement - Jacob Leehy
    Nov 10, 2024: Patch checkpoint bugs and implement speed retention between checkpoints - Jacob Leehy
    Nov 10, 2024: Added volume up and down option to option menu - Steve Gan
    Nov 10, 2024: Split up functionality from test.py into main.py and into their respective modules. - Mario Simental
Preconditions:
    - Pygame and required custom modules (audio, engine, image, sound_effect) are installed and accessible.
    - Assets such as images and sound files are located in the specified file paths.
    - Screen resolution and display settings support the dimensions of game objects.
Postconditions:
    - The game loads the main menu and allows for progression through levels.
    - The player can interact with platforms, checkpoints, and obstacles according to the specified game logic.
    - The main menu and pause menu are responsive to user input.
Error Conditions:
    - Missing assets (images, audio files) could cause load failures or display errors.
    - Invalid input or out-of-bound interactions may cause unexpected object behavior or freezes.
    - Collisions may behave unexpectedly if objects are incorrectly positioned.
Side Effects:
    - Modifies global game state and transitions between game states (e.g., main menu, pause, play).
    - Alters the screen buffer and renders images each frame.
    - Plays background music and sound effects based on game state.
Invariants:
    - The Cube object must remain within level boundaries except when falling off-screen at the game end.
    - Gravity and jump strength values must be non-zero to ensure continuous vertical movement.
    - Collision detection with non-flag objects stops vertical velocity, while flag collisions do not.
    - The main menu selection cycling remains within bounds (0-2).  
Known Faults:
    - It’s possible to jump over the end flag and fall off-screen.
    - The cube sprite may be pushed slightly out of its locked position on rare occasions.
    - Restart after completing the level doesn't ignore checkpoints
"""
import pygame # Import the Pygame library.
from engine import engine_instance  # Imports the engine singleton instance.
from state import OpeningMenuState # Imports the OpeningMenuState class.

# Main function.
def main():
    """
    Sets the initial game state and passes control to the engine.
    """
    engine_instance.state = OpeningMenuState(0)  # Set the initial game state.
    engine_instance.run_loop()              # Pass control to the engine.

# Main entry point.
if __name__ == "__main__": # magic
    main() # call main
