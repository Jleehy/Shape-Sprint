"""
state.py
Description:
    Defines an abstract base class for game states, including concrete game and menu states
    for handling various phases of gameplay, menu interactions, and game navigation.
Programmers:
    Steve Gan
    Sean Hammell
    Jacob Leehy
    Mario Simental
    Matthew Sullivan
Created:
    Oct 23, 2024
Revisions:
    Oct 24, 2024: Added game over state and connected to level - Matthew Sullivan
    Oct 27, 2024: Finalized prologue comments - Sean Hammell
    Nov 10, 2024: Modularized states and further abstracted menu-related states - Mario Simental
    Nov 10, 2024: Added comments - Jacob Leehy
    Nov 11, 2024: Added click sound asset to selections - Matthew Sullivan
    Nov 23, 2024: Updated GameState for tile-based level changes - Sean Hammell
    Nov 24, 2024: Add help menu state - Jacob Leehy
    Nov 24, 2024: Patch checkpoint bugs - Jacob Leehy
    Nov 24, 2024: Add speed modifier handling - Jacob Leehy
    Nov 24, 2024: Added additional states for sub menus for the options menu - Steve Gan
Preconditions:
    - Requires Pygame and imported dependencies (`engine`, `Image`, `SoundEffect`, etc.) to function.
    - Assets like images and sounds must be correctly formatted and stored in the specified paths.
    - Assumes `engine_instance` has been properly initialized before calling state functions.
Postconditions:
    - Provides modular state management for gameplay and menu handling.
    - Changes the state of the game based on input, Cube interactions, or menu navigation.
    - Ensures visual and auditory feedback for actions like jumping, colliding, or selecting menu options.
Error Conditions:
    - Does not handle missing or corrupted assets (e.g., images, sounds) gracefully.
    - Assumes valid user input; unexpected key presses or misconfigured controls may lead to undefined behavior.
Side Effects:
    - Alters the `engine_instance` state during transitions.
    - Plays music and sound effects as part of gameplay and menu navigation.
    - Updates Cube position, handles collisions, and modifies gameplay physics dynamically.
Invariants:
    - The `engine_instance` must consistently provide input, sound, and graphical capabilities.
    - `Cube` and `Level` objects are assumed to maintain valid states across game updates.
    - Gravity inversion assumes a binary state (normal or inverted) for gameplay consistency.
Known Faults:
    - Direct state transitions via `engine_instance.state` may cause unintended effects if states are mismanaged.
    - Collision logic may not account for edge cases like simultaneous interactions with multiple objects.
    - Background scrolling logic does not dynamically adapt to variable screen sizes or resolutions.
    - Gravity inversion continuously scrolls the screen incorrectly.
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
    def update(self): #update
        pass # pass

    def draw(self): # update
        pass # pass

# GameState manages the main gameplay, handling Cube movement, collisions, and rendering.
class GameState:
    # Initializes GameState, setting up Cube, Level, and other parameters.
    def __init__(self, level_id = 0, startpoint=[0, GROUND_LEVEL]):
        # Initialize objects.
        self._startpoint = startpoint # startpoint var to be used w/ checkpoints
        self._cube = Cube() # Store the Cube data.
        self._level = Level(levels[level_id], startpoint) # Store the Level data.

        # Initialize physics.
        self._gravity = 1  # Store the gravity data.
        self._jump_strength = -24 # Store the jump strength data.
        self._vertical_velocity = 0 # Store the vertical velocity data.

        self._objects_collided = [] # Store all objects collided with
        self._surfaces_collided = [] # Store all surfaces collided with

         # Initialize audio.
        self._landing_sound = SoundEffect("assets/landing_sound.wav") # landing sound
        set_music("assets/music.wav")  # Set the game music.
        play_music()                     # Play the game music.

        # Initialize movement flags.
        self.is_jumping = False # Flag if Cube is currently jumping.
        self.is_on_ground = False # Flag if Cube is grounded.

        # Load instructions asset
        self._instructions_image = Image("assets/instructions.png")  # Load the instructions image.
        self._settings = Image("assets/settings.png")                # Load the settings image.
        if level_id == 0:    
            self._background_image = Image("assets/background.png")  # Load the background
        elif level_id == 1:
            self._background_image = Image("assets/background2.png")  # Load the background
        elif level_id == 2:
            self._background_image = Image("assets/background3.png")  # Load the background
        elif level_id == 3:
            self._background_image = Image("assets/background4.png")  # Load the background
        elif level_id == 4:
            self._background_image = Image("assets/background5.png")  # Load the background

        self._ctr = 0 # counter
        self.jump_frames = 0 # how many frames jump key was held down for
        
    # Updates Cube position and handles input for movement and sound control.
    def update(self):
        """
        Updates the game based on input, movement, and sound control.
        """
        if engine_instance.keyboard.is_key_down("esc"):  # If escape is pressed.
            engine_instance.state = MainMenuState(self)            # Go to the main menu

        was_in_air = not self.is_on_ground # Track whether Cube was in the air in the last frame, for landing detection.
        
        for obj in self._objects_collided:
            if isinstance(obj, CheckpointFlag):
                self._startpoint = [obj._base_x - 4, obj._base_y + 1]  # Update the startpoint.
            elif isinstance(obj, EndFlag):
                engine_instance.state = GameOverState(self._level, self._cube, self._startpoint, 0)  # The user won.
            elif isinstance(obj, Spikes):
                engine_instance.state = GameOverState(self._level, self._cube, self._startpoint, 1)  # The user lost.
            elif isinstance(obj, InvertGravity): #if grav instance
            # Handle gravity inversion.
                if obj.activated == False: # deactivated
                    obj.activated = True # activate
                    if self._gravity > 0:  # If gravity is currently normal.
                        self._gravity = -1 #grav is -1
                        self._vertical_velocity = -2  # Small nudge upwards to ensure movement.
                    else:  # If gravity is currently inverted.
                        self._gravity = 1 #grav is 1
                        self._vertical_velocity = 2  # Small nudge downwards to ensure movement.
                    self.is_jumping = True #jumping is true
                    self.is_on_ground = False #jumping is false
                    print("Gravity inverted!") #test label
            
            
            elif isinstance(obj, SpeedBoost): #if speed boost
            # Handle gravity inversion.
                    self._cube.move(self._vertical_velocity, self._gravity, self._level) #move again - doubles speed
                    print("Speed") #print test

        # Handle jumping.
        if engine_instance.keyboard.is_key_down("up"): #if up
            if self.is_on_ground and not self.is_jumping:  # Allow jumping only if on the ground and not already jumping.
                self.is_jumping = True  # Mark that the cube is now in the air.
                self.jump_frames = 0  # Reset jump frames at the start of a jump.

            if self.is_jumping and self.jump_frames < 5:  # Continue adjusting velocity within a frame limit.
                self.jump_frames += 1  # Increment jump frames.
                jump_direction = 1 if self._gravity > 0 else -1  # Jump direction depends on gravity.
               
                self._vertical_velocity = jump_direction * max(self._jump_strength, self.jump_frames / 5 * self._jump_strength) #calc for var jump
                print(self._vertical_velocity) #print velocity
        else: #else
            if self.is_jumping and self.is_on_ground:  # Reset flags when landing.
                self.is_jumping = False  # Reset jumping state.
                self.jump_frames = 0  # Reset jump frames.
            
         # Update cube position and handle collisions.
        self._surfaces_collided, self._objects_collided = self._cube.move(self._vertical_velocity, self._gravity, self._level)  # Move the cube.
        
        # Apply gravity and check for ground collisions.
        if self._gravity > 0:  # Normal gravity.
            if self._surfaces_collided['bottom']:  # If colliding with ground below.
                self.is_on_ground = True #if on ground                
                if self.is_jumping == True: # check if just jumping
                    self._landing_sound.play() #play sound
                self.is_jumping = False #jump is false
                self._vertical_velocity = 0 #velocity is zero
            else:  # Not colliding with ground below.
                self.is_on_ground = False #on ground false
                self._vertical_velocity += self._gravity # increment vert velocity
            if self._surfaces_collided['top']: #if top collide
                engine_instance.state =GameOverState(self._level, self._cube, self._startpoint, 1) #end game
                
        else:  # Inverted gravity.
            if self._surfaces_collided['top']:  # If colliding with ceiling above (inverted ground).
                self.is_on_ground = True #if on ground
                if self.is_jumping == True: # check if just jumping
                    self._landing_sound.play() #play sound
                self.is_jumping = False #if jumping
                self._vertical_velocity = 0 #vert velocity is 0
            else:  # Not colliding with ceiling above.
                self.is_on_ground = False #on ground is false
                self._vertical_velocity += self._gravity #increace vert velocity
            if self._surfaces_collided['bottom']: #if bottom collision
                engine_instance.state = GameOverState(self._level, self._cube, self._startpoint, 1) #end game

        # Handle game over for collisions with spikes or out-of-bounds.
        if self._surfaces_collided['right'] or self._surfaces_collided['left']: #if left or right collision
            engine_instance.state = GameOverState(self._level, self._cube, self._startpoint, 1) # end game

    def draw(self): #func to draw everything
        self._background_image.blit(self._ctr,self._ctr) # show background
        self._ctr -= 1 #counter
        self._instructions_image.blit(10, 10)  # Adjust the x, y position as needed
        self._settings.blit(1500, 10)  # Adjust the x, y position as needed
        self._cube.draw() # draw cube
        self._level.draw() # draw level

# Base class for menu states to centralize common functionality.
class BaseMenuState(State):
    def __init__(self, options, background_path, last_key_time, font_large_size=72, font_small_size=95): # init
        self.font_large = pygame.font.SysFont(None, font_large_size) # Create a large font.
        self.font_small = pygame.font.SysFont(None, font_small_size) # Create a snakk font.
        self.options = options # Set the available options.
        self.selected_option = 0 # Set the current selected option.
        self.last_key_time = last_key_time # Record the time of the last key press.
        self.key_delay = 0.2 # Delay required before accepting key presses.
        self._background_image = pygame.image.load(background_path) # Set the background image.
        self.select_sound = SoundEffect("assets/click1.ogg") #click sound

    def update(self):
        """Updates menu state with input handling."""
        current_time = time.time() # Record the current time.
        if current_time - self.last_key_time <= self.key_delay: # If enough time has elapsed since the last key press.
            return #return

        if engine_instance.keyboard.is_key_down("down"): # If the down key is pressed.
            self.selected_option = (self.selected_option + 1) % len(self.options) # Cycle through the options.
            self.last_key_time = current_time # Record the time of the key press.
        elif engine_instance.keyboard.is_key_down("up"): # If the up key is pressed.
            self.selected_option = (self.selected_option - 1) % len(self.options) # Cycle through the options.
            self.last_key_time = current_time # Record the time of the key press.
        elif engine_instance.keyboard.is_key_down("select"): # If the return key is pressed.
            self.last_key_time = current_time # Record the time of the key press.
            self.select_sound.play() # Play click1 sound on selection
            self.select_option() # Select the option.

    def draw(self):
        """Draws the menu options with highlight on selected option."""
        engine_instance.screen.fill((0, 0, 0)) # Fill the background screen.
        engine_instance.screen.blit(self._background_image, (0, 0)) # Set the background image.

        for index, option in enumerate(self.options): # Iterate through all possible options.
            color = (240, 86, 86) if self.selected_option == index else (0, 0, 0) # Change button color if hovered.
            option_surface = self.font_small.render(option, True, color) # Render the option as a button.
            engine_instance.screen.blit(option_surface, (625, 400 + index * 65)) # Draw the button.

# Opening menu state with custom select_option logic.
class OpeningMenuState(BaseMenuState):
    def __init__(self, last_key_time): #init
        options = ["Start Game", "Options", "Level Select", "Quit"] # options list
        super().__init__(options, "assets/mainMenuBackground.png", last_key_time, font_large_size=72, font_small_size=110) #super with info

    def select_option(self): #option selector
        if self.selected_option == 0: # if 0
            self.select_sound.play() # Play click1 sound on selection
            engine_instance.state = GameState() #start game
        elif self.selected_option == 1: # if 1
            self.select_sound.play() # Play click1 sound on selection
            engine_instance.state = OptionsMenuState(self.last_key_time) #open options menu
        elif self.selected_option == 2: # if 2
            self.select_sound.play() # Play click1 sound on selection
            engine_instance.state = LevelSelectMenuState(self.last_key_time) # open level select menu
        elif self.selected_option == 3: # if 3
            sys.exit() # exit

class OptionsMenuState(BaseMenuState): #options menu
    def __init__(self, last_key_time): #init
        options = ["Back", "Volume", "Key Binds"] #create options list
        super().__init__(options, "assets/optionsMenuBackground.png", last_key_time)#load assets

    def select_option(self): #func to select options
        if self.selected_option == 0: # if 0
            self.select_sound.play() # Play click1 sound on selection
            engine_instance.state = OpeningMenuState(self.last_key_time) # return to opening menu
        elif self.selected_option == 1: # if 1
            self.select_sound.play() # Play click1 sound on selection
            engine_instance.state = SoundMenuState(self.last_key_time) #open sound menu
        elif self.selected_option == 2: # if 2
            self.select_sound.play() # Play click1 sound on selection
            engine_instance.state = KeysMenuState(self.last_key_time) #open keys menu

# Options menu state with custom select_option logic.
class SoundMenuState(BaseMenuState):
    def __init__(self, last_key_time): # init
        options = ["Back", "Volume Up", "Volume Down"] # opptions list
        super().__init__(options, "assets/optionsMenuBackground.png", last_key_time) # load asset

    def select_option(self): # option selector
        if self.selected_option == 0: # if 0
            self.select_sound.play() # Play click1 sound on selection
            engine_instance.state = OptionsMenuState(self.last_key_time) # return to options menu
        elif self.selected_option == 1: # if 1
            self.select_sound.play() # Play click1 sound on selection
            volume_up() # increace vol
        elif self.selected_option == 2: # if 2
            self.select_sound.play() # Play click1 sound on selection
            volume_down() # decreace vol

class KeysMenuState(BaseMenuState):
    def __init__(self, last_key_time): # init
        options = ["Back", "Arrow Keys", "WASD"] # opptions list
        super().__init__(options, "assets/optionsMenuBackground.png", last_key_time) # load asset

    def select_option(self): # option selector
        if self.selected_option == 0: # if 0
            self.select_sound.play() # Play click1 sound on selection
            engine_instance.state = OptionsMenuState(self.last_key_time) # return to options menu
        elif self.selected_option == 1: # if 1
            self.select_sound.play() # Play click1 sound on selection
            engine_instance.keyboard.set_Arrows() #set the keybinds to the arrow keys
        elif self.selected_option == 2: # if 2
            self.select_sound.play() # Play click1 sound on selection
            engine_instance.keyboard.set_WASD() #set the keybinds to the WASD keybinds

# Level select menu state with custom select_option logic.
class LevelSelectMenuState(BaseMenuState):
    def __init__(self, last_key_time): # init
        options = ["Back", "Level 1", "Level 2", "Level 3", "Level 4", "Level 5"] # options list
        super().__init__(options, "assets/levelMenuBackground.png", last_key_time) # super w/ info

    def select_option(self): # selection list
        if self.selected_option == 0: # if 0
            self.select_sound.play() # Play click1 sound on selection
            engine_instance.state = OpeningMenuState(self.last_key_time) # return to opening menu
        elif self.selected_option == 1: # if 1
            self.select_sound.play() # Play click1 sound on selection
            engine_instance.state = GameState()  # Start at Level 1 (0)
        elif self.selected_option == 2: # if 2
            self.select_sound.play() # Play click1 sound on selection
            engine_instance.state = GameState(1)  # Start at Level 2 (1)
        elif self.selected_option == 3: # if 3
            self.select_sound.play() # Play click1 sound on selection
            engine_instance.state = GameState(2)  # Start at Level 3 (2)
        elif self.selected_option == 4: # if 4
            self.select_sound.play() # Play click1 sound on selection
            engine_instance.state = GameState(3)  # Start at Level 4 (3)
        elif self.selected_option == 5: # if 4
            self.select_sound.play() # Play click1 sound on selection
            engine_instance.state = GameState(4)  # Start at Level 4 (3)

# Main menu state for in-game pause menu.
class MainMenuState(BaseMenuState):
    def __init__(self, previous_state): #init
        options = ["Continue", "Restart", "Help", "Main Menu"] # options list
        super().__init__(options, "assets/mainMenuBackground.png", 0, font_large_size=72, font_small_size=110) # super and send info
        self.previous_state = previous_state # set prev state

    def select_option(self): #options list
        if self.selected_option == 0: # if 0
            self.select_sound.play() # Play click1 sound on selection
            engine_instance.state = self.previous_state  # Resume the game
        elif self.selected_option == 1: # if 1
            self.select_sound.play() # Play click1 sound on selection
            engine_instance.state = GameState(self.previous_state._level.id)  # Restart the game
        elif self.selected_option == 2: # if 1
            self.select_sound.play() # Play click1 sound on selection
            engine_instance.state = HelpMenuState(self.last_key_time)  # Restart the game
        elif self.selected_option == 3: # if 3
            self.select_sound.play() # Play click1 sound on selection
            engine_instance.state = OpeningMenuState(self.last_key_time)  # Return to the main menu

class HelpMenuState(BaseMenuState): #help menu state
    def __init__(self, last_key_time): # init
        options = ["    Back"] # opptions list
        super().__init__(options, "assets/helpMenuBackground.png", last_key_time) # load asset


    def select_option(self): # option selector
        if self.selected_option == 0: # if 0
            self.select_sound.play() # Play click1 sound on selection
            engine_instance.state = OpeningMenuState(self.last_key_time)  # Return to the main menu


class GameOverState(BaseMenuState): # game over menu
    def __init__(self, level, cube, startpoint, endstate, last_key_time=None): # init
        options = ["Continue", "Restart", "Main Menu"] # options list
        if last_key_time is None: # if no key
            last_key_time = time.time()  # Use current time if not provided
        super().__init__(options, "assets/mainMenuBackground.png", last_key_time) # super with info
        
        # Store game-specific references
        self._level = level # store level
        self._cube = cube # store cube
        self._startpoint = startpoint # store start
        self._endstate = endstate # store end state

    def select_option(self): #func to select options
        """Defines actions based on the selected option in the Game Over menu."""
        if self.selected_option == 0:  # Continue
            if (self._level.id + 1 in levels) and (self._endstate == 0):  # If next level is available and endstate is 0
                self.select_sound.play() # Play click1 sound on selection
                engine_instance.state = GameState(self._level.id + 1)  # Continue to the next level
            elif self._endstate == 1:  # Retry the level from the startpoint
                self.select_sound.play() # Play click1 sound on selection
                engine_instance.state = GameState(self._level.id, self._startpoint)
            else:  # Otherwise, return to main menu
                self.select_sound.play() # Play click1 sound on selection
                engine_instance.state = OpeningMenuState(self.last_key_time)
        elif  self.selected_option == 1:  # Restart
            self.select_sound.play() # Play click1 sound on selection
            engine_instance.state = GameState(self._level.id)  # Restart the current level
        elif self.selected_option == 2:  # Quit
            self.select_sound.play() # Play click1 sound on selection
            engine_instance.state = OpeningMenuState(self.last_key_time)  # Return to the main menu

