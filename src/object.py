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

class Object:
    """
    Objects represent visual game entities.
    """
    def __init__(self, image_path, x, y, width, height): 
        """
        Initializes an Object given the path to an image, a position, and a size.
        """
        self._image = Image(image_path)                # Create an Image object given image_path.
        self._base_x = x                               # Store the original x position of the object (constant).
        self._base_y = y                               # Store the original y position of the object (constant).
        self._x = x                                    # Store the x position of the object.
        self._y = y                                    # Store the y position of the object.
        self._width = width                            # Store the width (pixels) of the object.
        self._height = height                          # Store the height (pixels) of the object.
        self._rect = pygame.Rect(x, y, width, height)  # Store the hitbox of the object.
        self._counter = 0                              # Counter to be used in calculating acceleration over time.
        self._acceleration = 0                         # Value to store the current speed increace from acceleration.

    def draw(self):
        """
        Draws the object image at the position defined by its hitbox.
        """
        self._image.blit(self._rect.x, self._rect.y)  # Blit the object

    def draw_hitbox(self, screen, color=(255, 0, 0)):
        """
        Draws the outline of the hitbox.
        """
        pygame.draw.rect(screen, color, self._rect, 2)  # Draw the hitbox rect.

    def get_position(self):
        """
        Returns the position of the object as a tuple (x, y).
        """
        return self._x, self._y  # Return the position components.

    def get_size(self):
        """
        Returns the size of the object as a tuple (width, height).
        """
        return self._width, self._height  # Return size dimensions.

    def move_object(self, xamount, yammount=0):
        """
        Moves the object the specified number of pixels.
        """
        self._counter += 1           # Increment counter.
        if self._counter == 60:      # If 60 frames have passed.
            self._counter = 0        # Reset frame count.
            self._acceleration += 1  # Increment acceleration.

        self._rect.x -= xamount + 10 + self._acceleration  # move the object left.  
        self._rect.y -= yammount

        # Update _x and _y to match the new rect position for consistency.
        self._x = self._rect.x
        self._y = self._rect.y
        
    def move_x(self, amount):
        """
        Shifts the objects left.
        """
        self._rect.x -= amount  # Move x coord
