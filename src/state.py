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
    Oct 27, 2024: Finalized prologue comments - Sean Hammell
    Nov 10, 2024: Modularized states and further abstracted menu related states. - Mario Simental
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

import pygame  # Import the Pygame library.
import sys     # Import system-specific parameters and functions.
import time    # Import the time module for handling delays.

from image import Image                     # Import the Image class for handling images.
from audio import *                         # Import audio-related functions.
from engine import engine_instance  # Import the engine singleton instance.
from sound_effect import SoundEffect        # Import the SoundEffect class for handling sound effects.

from level import *        # Import the Level class, level objects, and level specifications.
from object import Object  # Import the Object class to create game entities.

# State is an abstract base class. This definition is meant to give the Engine class
# visibility of the update and draw methods.
class State:
    def update(self):
        pass

    def draw(self):
        pass

# GameState manages the main gameplay, handling Cube movement, collisions, and rendering.
class GameState:
    # Initializes GameState, setting up Cube, Level, and other parameters.
    def __init__(self, level_id = 0, startpoint=[130, 780, 0]):
        # Initialize objects.
        self._startpoint = startpoint # startpoint var to be used w/ checkpoints
        self._cube = Cube(startpoint) # Store the Cube data.
        self._level = Level(levels[level_id], startpoint[0] - 130) # Store the Level data.

        if startpoint[2] != 0:
            for platform in self._level._environment: #move every object in the environment list
                platform._acceleration = startpoint[2] #move each platform

            for hazard in self._level._hazards: #move every object in the hazard list
                hazard._acceleration = startpoint[2] # move each hazard

        # Initialize physics.
        self._gravity = 1  # Store the gravity data.
        self._jump_strength = -24 # Store the jump strength data.
        self._vertical_velocity = 0 # Store the vertical velocity data.

         # Initialize audio.
        self._sound = SoundEffect("src/assets/sound.wav") # sound effects just in case we use them
        set_music("src/assets/music.wav")  # Set the game music.
        play_music()                     # Play the game music.

        # Initialize movement flags.
        self.moving_left = False # Flag if Cube is currently moving left.
        self.moving_right = False # Flag if Cube is currently moving right.
        self.is_jumping = False # Flag if Cube is currently jumping.

        # Load instructions asset
        self._instructions_image = Image("src/assets/instructions.png")  # Load the instructions image.
        self._settings = Image("src/assets/settings.png")                # Load the settings image.
        self._background_image = Image("src/assets/background.png")  # Load the background

        self._ctr = 0

    # Updates Cube position and handles input for movement and sound control.
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
            self.is_jumping = False


        if engine_instance.keyboard.is_key_down(pygame.K_UP) and not self.is_jumping:  # If the up arrow is pressed and the cube is not in the air.
                self._vertical_velocity = self._jump_strength                          # Set initial jump velocity.
                self.is_jumping = True                                                 # Set that the cube is in the air.

        #self.moving_left = engine_instance.keyboard.is_key_down(pygame.K_LEFT)    # Check if the left arrow is pressed.
        #self.moving_right = engine_instance.keyboard.is_key_down(pygame.K_RIGHT)  # Check if the right arrow is pressed.

        if engine_instance.keyboard.is_key_down(pygame.K_UP):
            if not self.is_jumping:
                self._vertical_velocity = self._jump_strength  # Set initial jump velocity
                self.is_jumping = True

        # Determine the horizontal movement based on flags

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
                self._startpoint = [obj._base_x, obj._base_y, obj._acceleration]                                        # Update the startpoint.
            if isinstance(obj, EndFlag):                                                             # If it's an end flag.
                engine_instance.state = GameOverState(self._level, self._cube, self._startpoint, 0)  # The user won.

    def draw(self):
        self._background_image.blit(self._ctr,self._ctr)
        self._ctr -= 1
        self._instructions_image.blit(10, 10)  # Adjust the x, y position as needed
        self._settings.blit(1500, 10)  # Adjust the x, y position as needed
        self._cube.draw() # draw cube
        self._level.draw() # draw level

# Base class for menu states to centralize common functionality.
class BaseMenuState(State):
    def __init__(self, options, background_path, last_key_time, font_large_size=72, font_small_size=36):
        self.font_large = pygame.font.SysFont(None, font_large_size) # Create a large font.
        self.font_small = pygame.font.SysFont(None, font_small_size) # Create a snakk font.
        self.options = options # Set the available options.
        self.selected_option = 0 # Set the current selected option.
        self.last_key_time = last_key_time # Record the time of the last key press.
        self.key_delay = 0.2 # Delay required before accepting key presses.
        self._background_image = pygame.image.load(background_path) # Set the background image.

    def update(self):
        """Updates menu state with input handling."""
        current_time = time.time() # Record the current time.
        if current_time - self.last_key_time <= self.key_delay: # If enough time has elapsed since the last key press.
            return

        if engine_instance.keyboard.is_key_down(pygame.K_DOWN): # If the down key is pressed.
            self.selected_option = (self.selected_option + 1) % len(self.options) # Cycle through the options.
            self.last_key_time = current_time # Record the time of the key press.
        elif engine_instance.keyboard.is_key_down(pygame.K_UP): # If the up key is pressed.
            self.selected_option = (self.selected_option - 1) % len(self.options) # Cycle through the options.
            self.last_key_time = current_time # Record the time of the key press.
        elif engine_instance.keyboard.is_key_down(pygame.K_RETURN): # If the return key is pressed.
            self.last_key_time = current_time # Record the time of the key press.
            self.select_option() # Select the option.

    def draw(self):
        """Draws the menu options with highlight on selected option."""
        engine_instance.screen.fill((0, 0, 0)) # Fill the background screen.
        engine_instance.screen.blit(self._background_image, (0, 0)) # Set the background image.

        for index, option in enumerate(self.options): # Iterate through all possible options.
            color = (255, 255, 0) if self.selected_option == index else (255, 255, 255) # Change button color if hovered.
            option_surface = self.font_small.render(option, True, color) # Render the option as a button.
            engine_instance.screen.blit(option_surface, (650, 600 + index * 100)) # Draw the button.

# Opening menu state with custom select_option logic.
class OpeningMenuState(BaseMenuState):
    def __init__(self, last_key_time):
        options = ["Start Game", "Options", "Level Select", "Quit"]
        super().__init__(options, "src/assets/mainMenuBackground.png", last_key_time, font_large_size=72, font_small_size=110)

    def select_option(self):
        if self.selected_option == 0:
            engine_instance.state = GameState()
        elif self.selected_option == 1:
            engine_instance.state = OptionsMenuState(self.last_key_time)
        elif self.selected_option == 2:
            engine_instance.state = LevelSelectMenuState(self.last_key_time)
        elif self.selected_option == 3:
            sys.exit()

# Options menu state with custom select_option logic.
class OptionsMenuState(BaseMenuState):
    def __init__(self, last_key_time):
        options = ["Back", "Volume Up", "Volume Down"]
        super().__init__(options, "src/assets/optionsMenuBackground.png", last_key_time)

    def select_option(self):
        if self.selected_option == 0:
            engine_instance.state = OpeningMenuState(self.last_key_time)
        elif self.selected_option == 1:
            volume_up()
        elif self.selected_option == 2:
            volume_down()

# Level select menu state with custom select_option logic.
class LevelSelectMenuState(BaseMenuState):
    def __init__(self, last_key_time):
        options = ["Back", "Level 1", "Level 2"]
        super().__init__(options, "src/assets/levelMenuBackground.png", last_key_time)

    def select_option(self):
        if self.selected_option == 0:
            engine_instance.state = OpeningMenuState(self.last_key_time)
        elif self.selected_option == 1:
            engine_instance.state = GameState()  # Start at Level 1
        elif self.selected_option == 2:
            engine_instance.state = GameState(1)  # Start at Level 2

# Main menu state for in-game pause menu.
class MainMenuState(BaseMenuState):
    def __init__(self, previous_state):
        options = ["Continue", "Restart", "Quit"]
        super().__init__(options, "src/assets/mainMenuBackground.png", 0, font_large_size=72, font_small_size=36)
        self.previous_state = previous_state

    def select_option(self):
        if self.selected_option == 0:
            engine_instance.state = self.previous_state  # Resume the game
        elif self.selected_option == 1:
            engine_instance.state = GameState()  # Restart the game
        elif self.selected_option == 2:
            sys.exit()  # Quit the game

class GameOverState(BaseMenuState):
    def __init__(self, level, cube, startpoint, endstate, last_key_time=None):
        options = ["Continue", "Restart", "Quit"]
        if last_key_time is None:
            last_key_time = time.time()  # Use current time if not provided
        super().__init__(options, "src/assets/mainMenuBackground.png", last_key_time)
        
        # Store game-specific references
        self._level = level
        self._cube = cube
        self._startpoint = startpoint
        self._endstate = endstate

    def select_option(self):
        """Defines actions based on the selected option in the Game Over menu."""
        if self.selected_option == 0:  # Continue
            if (self._level.id + 1 in levels) and (self._endstate == 0):  # If next level is available and endstate is 0
                engine_instance.state = GameState(self._level.id + 1)  # Continue to the next level
            elif self._endstate == 1:  # Retry the level from the startpoint
                engine_instance.state = GameState(self._level.id, self._startpoint)
            else:  # Otherwise, return to main menu
                engine_instance.state = OpeningMenuState(self.last_key_time)
        elif  self.selected_option == 1:  # Restart
            engine_instance.state = GameState(self._level.id)  # Restart the current level
        elif self.selected_option == 2:  # Quit
            engine_instance.state = OpeningMenuState(self.last_key_time)  # Return to the main menu


