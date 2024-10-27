"""
test.py
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
    Oct 24, 2024: Added jumping, gravity, and basic ground logic - Jacob Leehy
    Oct 26, 2024: Added level progression (scrolling screen) - Jacob Leehy
    Oct 27, 2024: Added checkpoints, game end, pause menu, platforms, and instructions - Jacob Leehy
    Oct 27, 2024: Cleaned up comments - Sean Hammell
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
"""

import sys   # Import system-specific parameters and functions.
import time  # Import the time module for handling delays.

import pygame  # Import the Pygame library.

from audio import *                         # Import audio functions.
from engine import Engine, engine_instance  # Imports the Engine class and a singleton instance.
from image import Image                     # Import the Image class.
from sound_effect import SoundEffect        # Import the SoundEffect.

# An Object is a visual entity within the game, which encapsulates image rendering and
# position handling.
class Object:
    def __init__(self, image_path, x, y, width, height):
        """
        Initializes an Object given a path to an image file, a position, and a size.
        """
        self._image = Image(image_path)               # Create an Image object.
        self._x = x                                   # Store the x position of the object.
        self._y = y                                   # Store the y position of the object.
        self._width = width                           # Store the width (pixels) of the object.
        self._height = height                         # Store the height (pixels) of the object.
        self._rect = pygame.Rect(x, y, width, height) # Store the hitbox of the object.
        self._offset = 0                              # Store the offset (pixels) from the (x, y) position of the object.
        self._acceleration = 0                        # Track the object's acceleration.

    def draw(self):
        """
        Draws the object at the position defined by its hitbox.
        """
        self._image.blit(self._rect.x, self._rect.y) 

    def draw_hitbox(self, screen, color=(255, 0, 0)):
        """
        Draws the outline of the object's hitbox.
        """
        pygame.draw.rect(screen, color, self._rect, 2) 

    def get_position(self):
        """
        Returns the position of the object.
        """
        return self._x, self._y

    def get_size(self):
        """
        Returns the size of the object.
        """
        return self._width, self._height

    def moveObject(self, amount):
        """
        Moves the object the specified number of pixels.
        """
        self._offset += 1            # Increment the offset.
        if self._offset == 75:       # If the object has moved a full tile.
            self._offset = 0         # Reset the offset.
            self._acceleration += 3  # Increase the acceleration.

        self._rect.x -= amount + 5 + self._acceleration  # Shift the object left.
        
    def moveX(self, shiftAmmount):
        """
        Shifts the objects left.
        """
        self._rect.x -= shiftAmmount

# A Cube is an Object which represents the playable entity in the game.
class Cube(Object):
    def __init__(self, startY):
        """
        Initializes a Cube object.
        """
        super().__init__("./assets/cube.png", 130, startY, 120, 120)

    def move(self, x, y, level):
        """
        Moves the Cube and handles collisions.
        """
        collides_with = []    # List of objects the Cube collides with.
        collision_checks = {  # Track collisions on each side.
            'top': False,
            'bottom': False,
            'left': False, 
            'right': False
        }

        self._rect.y += y  # Update the Cube's vertical position.

        for platform in level._ground:  # For each platform object.
            platform.moveObject(x)      # Move it x pixels to the left.

        for hazard in level._hazards:  # For each hazard object.
            hazard.moveObject(x)       # Move it x pixels to the left.
            
        collision_list = level.get_collisions(self)  # Record any objects colliding with the cube.

        for obj in collision_list:                                                 # For each object in the collision list.
            if not (isinstance(obj, CheckpointFlag) or isinstance(obj, EndFlag)):  # If the object is not a flag.
                if x > 0:                                                          # If the cube is moving right
                    self._rect.right = obj._rect.left                              # Push the cube to the left edge of the object.
                    collision_checks['right'] = True                               # Record the right-side collision.
                elif y > 0:                                                        # If the cube is moving down.
                    self._rect.bottom = obj._rect.top                              # Push the cube to the top of the object.
                    collision_checks['bottom'] = True                              # Record the bottom-side collision.
                elif y < 0:                                                        # If the cube is moving up.
                    self._rect.top = obj._rect.bottom                              # Push the cube to the bottom of the object.
                    collision_checks['top'] = True                                 # Record the top-side collision.
            
        return collision_checks, collision_list  # Return collision data.

# Ground represents a floor tile.
class Ground(Object):
    def __init__(self, x, y):
        """
        Initializes a Ground object.
        """
        super().__init__("./assets/ground.png", x, y, 800, 150)

# Platform represents a hovering tile.
class Platform(Object):
    def __init__(self, x, y):
        """
        Initializes a Platform object.
        """
        super().__init__("./assets/ground2.png", x, y, 200, 25)

# EndFlag represents the end-of-level marker.
class EndFlag(Object):
    def __init__(self, x, y):
        """
        Initializes an EndFlag object.
        """
        super().__init__("./assets/end.png", x, y, 60, 120)

# CheckpointFlag represents a mid-level checkpoint.
class CheckpointFlag(Object):
    def __init__(self, x, y):
        """
        Initializes a CheckpointFlag object.
        """
        super().__init__("./assets/checkpoint.png", x, y, 60, 120)

# Spikes represents a hazard tile.
class Spikes(Object):
    def __init__(self, x, y):
        """
        Initializes a Spikes object.
        """
        super().__init__("./assets/spikes.png", x, y, 120, 120)

# Level manages tile layout, rendering, and collision checking.
class Level:
    def __init__(self, startingX):
        """
        Initializes the level layout.
        """
        # Initializes non-hazardous objects.
        self._ground = [
            Ground(0, 450),
            Ground(-700, 300),
            Ground(-700,-50),
            Ground(800, 450),
            Ground(1600, 450),
            Ground(2400, 450),
            Ground(3200, 450),
            Ground(4000, 450),
            Ground(4800, 450),
            Platform(3300, 250),
            Platform(3500, 250),
            CheckpointFlag(3440, 130),
            EndFlag(5200, 330)
        ]

        # Initializes hazardous objects.
        self._hazards = [
            Spikes(600, 330),
            Spikes(1700, 330),
            Spikes(3440, 330),
            Spikes(3800, 330)
        ]

        for obj in self._ground + self._hazards:  # For all layout objects.
            obj.moveX(startingX)                  # Move the object to its starting position.
    
    def get_ground(self):
        """
        Returns a list of the non-hazardous objects.
        """
        return self._ground

    def get_hazards(self):
        """
        Returns a list of the hazardous objects.
        """
        return self._hazards
    
    def draw(self):
        """
        Draws the level.
        """
        for object in self._ground + self._hazards:  # For all level objects.
            object.draw()                            # Draw the object to the screen.

    def get_collisions(self, cube):
        """
        Returns a list of objects colliding with the cube.
        """
        collision_list = []                          # List of objects colliding with the Cube.
        for object in self._ground + self._hazards:  # Iterate through every level object.
            if cube._rect.colliderect(object._rect): # If the object collides with the cube.
                collision_list.append(object)        # Add it to the collision list.

        return collision_list  # Return the collision list.

class MainMenuState:
    def __init__(self, previous_state):
        """
        Initializes a MainMenuState.
        """
        self.font_large = pygame.font.SysFont(None, 72)  # Create a large font.
        self.font_small = pygame.font.SysFont(None, 36)  # Create a small font.
        self.selected_option = 0                         # Set the selected menu option (0 = Continue, 1 = Restart, 2 = Quit).
        self.previous_state = previous_state             # Store the game state to resume later.
        self.last_key_time = 0                           # Record the time of the last key press.
        self.key_delay = 0.2                             # Delay before accepting key presses.

    def update(self):
        """
        Updates the main menu.
        """
        current_time = time.time()                                     # Record the current time.
        if current_time - self.last_key_time > self.key_delay:         # If enough time has elapsed since the last key press.
            if engine_instance.keyboard.is_key_down(pygame.K_DOWN):    # If the down arrow is pressed.
                self.selected_option = (self.selected_option + 1) % 3  # Cycle down through the menu options.
                self.last_key_time = current_time                      # Record the time of the key press.
            elif engine_instance.keyboard.is_key_down(pygame.K_UP):    # If the up arrow is pressed.
                self.selected_option = (self.selected_option - 1) % 3  # Cycle down through the menu options.
                self.last_key_time = current_time                      # Record the time of the key press.

            if engine_instance.keyboard.is_key_down(pygame.K_RETURN):  # If the return key is pressed.
                if self.selected_option == 0:                          # If Continue is selected.
                    engine_instance.state = self.previous_state        # Resume the game.
                elif self.selected_option == 1:                        # If Restart is selected.
                    engine_instance.state = ExampleState()             # Start a new game.
                elif self.selected_option == 2:                        # If Quit is selected.
                    sys.exit()                                         # Exit the game.

    def draw(self):
        """
        Draws the main menu.
        """
        engine_instance.screen.fill((0, 0, 0))                                     # Clear the screen.
        menu_surface = self.font_large.render("Main Menu", True, (255, 255, 255))  # Create a surface for the menu.
        engine_instance.screen.blit(menu_surface, (200, 150))                      # Draw the menu.

        # Create the Continue option.
        continue_color = (255, 255, 0) if self.selected_option == 0 else (255, 255, 255)
        continue_surface = self.font_small.render("Continue", True, continue_color)
        engine_instance.screen.blit(continue_surface, (250, 250))

        # Create the Restart option.
        restart_color = (255, 255, 0) if self.selected_option == 1 else (255, 255, 255)
        restart_surface = self.font_small.render("Restart", True, restart_color)
        engine_instance.screen.blit(restart_surface, (250, 300))

        # Create the Quit option.
        quit_color = (255, 255, 0) if self.selected_option == 2 else (255, 255, 255)
        quit_surface = self.font_small.render("Quit", True, quit_color)
        engine_instance.screen.blit(quit_surface, (250, 350))


# ExampleState represents an example level of the game.
class ExampleState:
    def __init__(self, startpoint=[130, 330]):
        """
        Initializes an ExampleState.
        """
        self._startpoint = startpoint             # Record the startpoint.
        self._cube = Cube(startpoint[1])          # Store the cube startpoint.
        self._level = Level(startpoint[0] - 130)  # Store the level startpoint.

        # Initialize physics.
        self._gravity = 1            # Store the gravity.
        self._jump_strength = -24    # Store the jump strength.
        self._vertical_velocity = 0  # Store the vertical velocity.

        set_music("./assets/music.wav")  # Set the game music.
        play_music()                     # Play the game music.

        self.moving_left = False   # Is the cube is currently moving left?
        self.moving_right = False  # Is the cube is currently moving right?
        self.is_jumping = False    # Is the cube is currently jumping?

        self._instructions_image = Image("./assets/instructions.png")  # Load the instructions image.
        self._settings = Image("./assets/settings.png")                # Load the settings image.

    def update(self):
        """
        Updates the game based on input, movement, and sound control.
        """
        if engine_instance.keyboard.is_key_down(pygame.K_ESCAPE):  # If escape is pressed.
            engine_instance.state = MainMenuState(self)            # Go to the main menu

        collisions = self._level.get_collisions(self._cube)                               # Get all collisions.
        non_flag_collision = False                                                        # Check for non-flag collisions.
        for obj in collisions:                                                            # For each colliding object.
            if (not isinstance(obj, CheckpointFlag)) and (not isinstance(obj, EndFlag)):  # If the object is not a flag.
                non_flag_collision = True                                                 # The cube hit a non-flag object.

        if not non_flag_collision:                    # If the cube is in the air.
            self._vertical_velocity += self._gravity  # Apply gravity.
        else:                                         # If the cube is on the ground.
            self._vertical_velocity = 0               # Reset vertical velocity.

        if engine_instance.keyboard.is_key_down(pygame.K_UP) and not self.is_jumping:  # If the up arrow is pressed and the cube is not in the air.
                self._vertical_velocity = self._jump_strength                          # Set initial jump velocity.
                self.is_jumping = True                                                 # Set that the cube is in the air.

        self.moving_left = engine_instance.keyboard.is_key_down(pygame.K_LEFT)    # Check if the left arrow is pressed.
        self.moving_right = engine_instance.keyboard.is_key_down(pygame.K_RIGHT)  # Check if the right arrow is pressed.

        horizontal_movement = 0       # Update the horizontal movement.
        if self.moving_left:          # If its moving left.
            horizontal_movement = -3  # Set the horizontal movement to -3.
        elif self.moving_right:       # If its moving right.
            horizontal_movement = 10  # Set the horizontal movement to 10.

        collisions, collides_with = self._cube.move(horizontal_movement, self._vertical_velocity, self._level)  # Move the cube.

        if collisions['bottom']:         # If the cube is colliding with something under it.
            self.is_jumping = False      # Set that the cube is on the ground.
            self._vertical_velocity = 0  # Reset the vertical velocity.

        for obj in collides_with:                                                                    # For each object the cube is colliding with.
            if isinstance(obj, Spikes):                                                              # If it's spikes.
                engine_instance.state = GameOverState(self._level, self._cube, self._startpoint, 1)  # The user lost.
            if isinstance(obj, CheckpointFlag):                                                      # If it's a checkpoint.
                self._startpoint = [obj._x, obj._y]                                                  # Update the startpoint.
            if isinstance(obj, EndFlag):                                                             # If it's an end flag.
                engine_instance.state = GameOverState(self._level, self._cube, self._startpoint, 0)  # The user won.
                
    def draw(self):
        """
        Draws the state.
        """
        self._instructions_image.blit(10, 10)  # Draw the instructions.
        self._settings.blit(700, 10)           # Draw the settings.
        self._cube.draw()                      # Draw the cube.
        self._level.draw()                     # Draw the level.

class GameOverState:
    def __init__(self, level, cube, startpoint, endstate):
        """
        Initializes a GameOverState.
        """
        self._level = level
        self._cube = cube
        self.font_large = pygame.font.SysFont(None, 72)  # Create a large font.
        self.font_small = pygame.font.SysFont(None, 36)  # Create a small font.
        self.selected_option = 0                         # Set the selected menu option (0 = Restart, 1 = Quit).
        self._startpoint = startpoint                    # Set the startpoint.
        self._endstate = endstate                        # Record the result of the last run.
        self.last_key_time = 0                           # Record the time of the last key press.
        self.key_delay = 0.2                             # Delay before accepting key presses.

    def update(self):
        """
        Updates the game over menu.
        """
        current_time = time.time()  # Record the current time.

        if current_time - self.last_key_time > self.key_delay:         # If enough time has elapsed since the last key press.
            if engine_instance.keyboard.is_key_down(pygame.K_DOWN):    # If the down arrow is pressed.
                self.selected_option = (self.selected_option + 1) % 2  # Cycle through the menu options.
                self.last_key_time = current_time                      # Record the time of the key press.
            elif engine_instance.keyboard.is_key_down(pygame.K_UP):    # If the up arrow is pressed.
                self.selected_option = (self.selected_option - 1) % 2  # Cycle through the menu options.
                self.last_key_time = current_time                      # Record the time of the key press.

            if engine_instance.keyboard.is_key_down(pygame.K_RETURN):       # If the return key is pressed.
                if self.selected_option == 0:                               # If Restart is selected.
                    engine_instance.state = ExampleState(self._startpoint)  # Start a new game.
                elif self.selected_option == 1:                             # If Quit is selected.
                    sys.exit()                                              # Exit the game.

    def draw(self):
        """
        Draws the game over menu.
        """
        self._level.draw()  # Draw the level in the background.
        self._cube.draw()   # Draw the cube in the background.

        if self._endstate == 0:                                                                # If the user won.
            game_result_surface = self.font_large.render("Level Complete", True, (0, 255, 0))  # Display "Level Complete".
        elif self._endstate == 1:                                                              # If the user lost.
            game_result_surface = self.font_large.render("Game Over", True, (255, 0, 0))       # Display "Game Over".

        # Create the Restart option.
        restart_color = (255, 255, 0) if self.selected_option == 0 else (255, 255, 255)
        restart_surface = self.font_small.render("Restart", True, restart_color)
        engine_instance.screen.blit(restart_surface, (250, 300))

        # Create the Quit option.
        quit_color = (255, 255, 0) if self.selected_option == 1 else (255, 255, 255)
        quit_surface = self.font_small.render("Quit", True, quit_color)
        engine_instance.screen.blit(quit_surface, (250, 350))

def main():
    """
    Sets the initial game state and passes control to the engine.
    """
    engine_instance.state = ExampleState()  # Set the initial game state.
    engine_instance.run_loop()              # Pass control to the engine.

if __name__ == "__main__":
    main()
