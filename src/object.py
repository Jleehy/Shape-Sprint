"""
object.py
Description:
    Represents an entity within the game (e.g., player, ground tiles, hazards).
Programmers:
    Steve Gan
    Sean Hammell
    Jacob Leehy
    Mario Simental
    Matthew Sullivan
Created:
    Nov 9, 2024
Revisions:
    Nov 9, 2024: Moved the Object class out of test.py - Sean Hammell
    Nov 9, 2024: Adjust how movement is handled such that the player is tracked vertically - Jacob Leehy
    Nov 10, 2024: Add more comments - Jacob Leehy
    Nov 23, 2024: Removed acceleration and added TILE_SIZE support - Sean Hammell
    Nov 24, 2024: Reimplement acceleration and add comments- Jacob Leehy
Preconditions:
    - Requires the Pygame library for rendering and collision detection.
    - `image.py` module must define an `Image` class for handling image loading and rendering.
    - Valid image path, x and y coordinates, width, and height values must be provided for initialization.
Postconditions:
    - Creates and manipulates objects within the game, allowing for position updates, rendering, and collision hitbox visualization.
Error Conditions:
    - Invalid file path for image will result in failed image loading.
    - Non-integer values for position or size parameters may result in unexpected behavior.
Side Effects:
    - Alters Pygame display surface by rendering images and hitboxes.
    - Updates internal acceleration and position counters as the game runs.
Invariants:
    - `_x` and `_y` always match `_rect.x` and `_rect.y` for consistent position tracking.
    - `_counter` increments each frame and resets every 30 frames, controlling the acceleration rate.
Known Faults:
    - No known faults at this time.
"""


import pygame

from image import Image
from engine import engine_instance  # Import the engine singleton instance.

TILE_SIZE = 80

class Object:
    """
    Objects represent visual game entities.
    """
    def __init__(self, image_path, x, y, width, height): 
        """
        Initializes an Object given the path to an image, a position, and a size.
        """
        self._image = Image(image_path)                                        # Create an Image object given image_path.
        self._base_x = x                                                       # Store the original x position of the object (constant).
        self._base_y = y                                                       # Store the original y position of the object (constant).
        self._width = width                                                    # Store the width (pixels) of the object.
        self._height = height                                                  # Store the height (pixels) of the object.
        self._rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, width, height)  # Store the hitbox of the object.
        self._speed = int(TILE_SIZE / 5)                                       # Movement speed.
        self._acceleration = 0 #var for accel
        self._counter = 0 #counter for accel
        
    def draw(self):
        """
        Draws the object image at the position defined by its hitbox.
        """
        self._image.blit(self._rect.x, self._rect.y)  # Blit the object

    def draw_hitbox(self, color=(255, 0, 0)):
        """
        Draws the outline of the hitbox.
        """
        pygame.draw.rect(engine_instance.screen, color, self._rect, 2)  # Draw the hitbox rect.

    def scroll_object(self, dy):
        """
        Moves the object the specified number of pixels.
        """
        if self._counter == 120: # if two secs pass
            self._acceleration += 1 #increment accel
            self._counter = 0 #reset coiuunter
        self._counter += 1 #increment couner

        self._rect.x -= self._speed + self._acceleration  # move the object left.  
        self._rect.y -= dy # move the object vertically

    def move_x(self, x):
        """
        Shifts the objects vertically.
        """
        self._rect.x += x  # Move x coord
