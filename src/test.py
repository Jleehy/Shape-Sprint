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
    Nov 9, 2024: Split out Level and Object classes to separate files - Sean Hammell
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
import pygame  # Import the Pygame library.
import sys     # Import system-specific parameters and functions.
import time    # Import the time module for handling delays.

from audio import *                         # Import audio-related functions.
from engine import Engine, engine_instance  # Import the Engine class and a singleton instance.
from image import Image                     # Import the Image class for handling images.
from sound_effect import SoundEffect        # Import the SoundEffect class for handling sound effects.

from level import *        # Import the Level class, level objects, and level specifications.
from object import Object  # Import the Object class to create game entities.

# A Cube is an Object which represents the playable entity in the game.
class Cube(Object):
    # Initializes a Cube with the image path, size and position.
    def __init__(self, startY):
        """
        Initializes a Cube object.
        """
        super().__init__("./assets/cube.png", 130, startY, 120, 120) #supers init

    # Moves the Cube and handles collisions.
    def move(self, x, y, level):
        """
        Moves the Cube and handles collisions.
        """
        collision_checks = {'top': False, 'bottom': False, 'left': False, 'right': False} # Track collisions on each side.
        collides_with = [] # List of objects the Cube collides with.
            
        collision_list = level.get_collisions(self) # Get objects colliding with Cube after a horizontal movement.

        # Handle horizontal collisions.
        for obj in collision_list: #iterate over objects
            if not (isinstance(obj, CheckpointFlag) or isinstance(obj, EndFlag)): #only handle collisions for objects that shouldnt be moved through
                if x > 0:  # Moving right
                    self._rect.right = obj._rect.left  # Push cube back to the left edge of the object
                    collision_checks['right'] = True # Update right-side collision.
                elif x < 0:  # Moving left
                    self._rect.left = obj._rect.right  # Push cube back to the right edge of the object
                    collision_checks['left'] = True # Update left-side collision.
            collides_with.append(obj) # Add object to list of objects the Cube collides with.
            
        #self._rect.y += y # Update the Cube's vertical position.
        collision_list = level.get_collisions(self) # Get objects colliding with Cube after a vertical movement.
        
        # Handle vertical collisions
        for obj in collision_list: #iterate over objects
            if not (isinstance(obj, CheckpointFlag) or isinstance(obj, EndFlag)): #only handle collisions for objects that shouldnt be moved through
                if y > 0:  # Moving down
                    self._rect.bottom = obj._rect.top  # Snap to the top of the object
                    collision_checks['bottom'] = True # Update bottom-side collision.
                elif self._rect.top > obj._rect.top:  # Moving up
                    self._rect.top = obj._rect.bottom  # Snap to the bottom of the object
                    collision_checks['top'] = True # Update top-side collision.
            collides_with.append(obj) # Add object to list of objects the Cube collides with.

        for platform in level._environment: #move every object in the environment list
            platform.move_object(x, y) #move each platform

        for hazard in level._hazards: #move every object in the hazard list
            hazard.move_object(x, y) # move each hazard

        return collision_checks, collides_with # Return collision data.

class OpeningMenuState:
    def __init__(self, last_key_time):
        """Initializes an opening menu state"""
        self.font_large = pygame.font.SysFont(None, 72)  # Create a large font.
        self.font_small = pygame.font.SysFont(None, 110)  # Create a small font.
        self.selected_option = 0                         # Set the selected menu option (0 = Start Game, 1 = Options, 2 = Level Select, 3 = Quit).
        self.last_key_time = last_key_time               # Record the time of the last key press.
        self.key_delay = 0.2                             # Delay before accepting key presses.
        self._background_image = Image("./assets/mainMenuBackground.png")  # Load the background

    def update(self):
        current_time = time.time()                                     # Record the current time.
        if current_time - self.last_key_time > self.key_delay:         # If enough time has elapsed since the last key press.
            if engine_instance.keyboard.is_key_down(pygame.K_DOWN):    # If the down arrow is pressed.
                self.selected_option = (self.selected_option + 1) % 4  # Cycle down through the menu options.
                self.last_key_time = current_time                      # Record the time of the key press.
            elif engine_instance.keyboard.is_key_down(pygame.K_UP):    # If the up arrow is pressed.
                self.selected_option = (self.selected_option - 1) % 4  # Cycle down through the menu options.
                self.last_key_time = current_time                      # Record the time of the key press.

            if engine_instance.keyboard.is_key_down(pygame.K_RETURN):  # If the return key is pressed.
                self.last_key_time = current_time
                if self.selected_option == 0:                          # If Start Game is selected.
                    self.last_key_time = current_time
                    engine_instance.state = ExampleState()             # Start the Game.
                elif self.selected_option == 1:                        # If Options is selected.
                    self.last_key_time = current_time
                    engine_instance.state = OptionsMenuState(self.last_key_time)         # Go to the options menu.
                elif self.selected_option == 2:                        # If Level select is selected.
                    self.last_key_time = current_time
                    engine_instance.state = LevelSelectMenuState(self.last_key_time)     # Go to the level select menu.
                elif self.selected_option == 3:
                    self.last_key_time = current_time
                    sys.exit()

    def draw(self):
        """Draws the opening menu"""
        engine_instance.screen.fill((0, 0, 0))                                     # Clear the screen.
        self._background_image.blit(0,0)

        #menu_surface = self.font_large.render("Main Menu", True, (255, 255, 255))  # Create a surface for the menu.
        #engine_instance.screen.blit(menu_surface, (200, 150))                      # Draw the menu.

        # Create the Start Game option.
        start_color = (255, 255, 0) if self.selected_option == 0 else (255, 255, 255)
        start_surface = self.font_small.render("Start Game", True, start_color)
        engine_instance.screen.blit(start_surface, (600, 600))

        # Create the Options menu option.
        options_color = (255, 255, 0) if self.selected_option == 1 else (255, 255, 255)
        options_surface = self.font_small.render("Options", True, options_color)
        engine_instance.screen.blit(options_surface, (600, 700))

        # Create the Level Select option
        levelS_color = (255, 255, 0) if self.selected_option == 2 else (255, 255, 255)
        levelS_surface = self.font_small.render("Level Select", True, levelS_color)
        engine_instance.screen.blit(levelS_surface, (600, 800))

        # Create the Quit option.
        quit_color = (255, 255, 0) if self.selected_option == 3 else (255, 255, 255)
        quit_surface = self.font_small.render("Quit", True, quit_color)
        engine_instance.screen.blit(quit_surface, (600, 900))

class OptionsMenuState:
    def __init__(self, last_key_time):
        """Initializes an opening menu state"""
        self.font_large = pygame.font.SysFont(None, 72)  # Create a large font.
        self.font_small = pygame.font.SysFont(None, 110)  # Create a small font.
        self.selected_option = 0                         # Set the selected menu option (0 = Start Game, 1 = Options, 2 = Level Select, 3 = Quit).
        self.last_key_time = last_key_time               # Record the time of the last key press.
        self.key_delay = 0.2                             # Delay before accepting key presses.

        self._background_image = Image("./assets/optionsMenuBackground.png")  # Load the background


    def update(self):
        """updates the options menu"""
        current_time = time.time()                                     # Record the current time.
        if current_time - self.last_key_time > self.key_delay:         # If enough time has elapsed since the last key press.
            if engine_instance.keyboard.is_key_down(pygame.K_DOWN):    # If the down arrow is pressed.
                self.selected_option = (self.selected_option + 1) % 1  # Cycle down through the menu options.
                self.last_key_time = current_time                      # Record the time of the key press.
            elif engine_instance.keyboard.is_key_down(pygame.K_UP):    # If the up arrow is pressed.
                self.selected_option = (self.selected_option - 1) % 1  # Cycle down through the menu options.
                self.last_key_time = current_time                      # Record the time of the key press.

            if engine_instance.keyboard.is_key_down(pygame.K_RETURN):  # If the return key is pressed.
                self.last_key_time = current_time 
                if self.selected_option == 0:                          # If Back is selected.
                    engine_instance.state = OpeningMenuState(self.last_key_time)         # Return to opening menu

    def draw(self):
        """Draws the options menu"""
        engine_instance.screen.fill((0, 0, 0))                                     # Clear the screen.
        self._background_image.blit(0,0)
        #menu_surface = self.font_large.render("Options", True, (255, 255, 255))  # Create a surface for the menu.
        #engine_instance.screen.blit(menu_surface, (200, 150))                      # Draw the menu.

        # Create the Back option.
        back_color = (255, 255, 0) if self.selected_option == 0 else (255, 255, 255)
        back_surface = self.font_small.render("Back", True, back_color)
        engine_instance.screen.blit(back_surface, (600, 600))

class LevelSelectMenuState:
    def __init__(self, last_key_time):
        """Initializes an opening menu state"""
        self.font_large = pygame.font.SysFont(None, 72)  # Create a large font.
        self.font_small = pygame.font.SysFont(None, 110)  # Create a small font.
        self.selected_option = 0                         # Set the selected menu option (0 = Start Game, 1 = Options, 2 = Level Select, 3 = Quit).
        self.last_key_time = last_key_time                           # Record the time of the last key press.
        self.key_delay = 0.2                             # Delay before accepting key presses.

        self._background_image = Image("./assets/levelMenuBackground.png")  # Load the background

    def update(self):
        """updates the level select menu"""
        current_time = time.time()                                     # Record the current time.
        if current_time - self.last_key_time > self.key_delay:         # If enough time has elapsed since the last key press.
            if engine_instance.keyboard.is_key_down(pygame.K_DOWN):    # If the down arrow is pressed.
                self.selected_option = (self.selected_option + 1) % 1  # Cycle down through the menu options.
                self.last_key_time = current_time                      # Record the time of the key press.
            elif engine_instance.keyboard.is_key_down(pygame.K_UP):    # If the up arrow is pressed.
                self.selected_option = (self.selected_option - 1) % 1  # Cycle down through the menu options.
                self.last_key_time = current_time                      # Record the time of the key press.

            if engine_instance.keyboard.is_key_down(pygame.K_RETURN):  # If the return key is pressed.
                self.last_key_time = current_time 
                if self.selected_option == 0:                          # If Back is selected.
                    engine_instance.state = OpeningMenuState(self.last_key_time)         # Return to opening menu

    def draw(self):
        """Draws the level select menu"""
        engine_instance.screen.fill((0, 0, 0))                                     # Clear the screen.
        self._background_image.blit(0,0)
        #menu_surface = self.font_large.render("Options", True, (255, 255, 255))  # Create a surface for the menu.
        #engine_instance.screen.blit(menu_surface, (200, 150))                      # Draw the menu.

        # Create the Back option.
        back_color = (255, 255, 0) if self.selected_option == 0 else (255, 255, 255)
        back_surface = self.font_small.render("Back", True, back_color)
        engine_instance.screen.blit(back_surface, (600, 600))

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
        engine_instance.screen.fill((0, 0, 0))  # Clear screen for the menu
        menu_surface = self.font_large.render("Pause Menu", True, (255, 255, 255)) # make surface for menu
        engine_instance.screen.blit(menu_surface, (200, 150)) # draw menu

        # Menu options
        continue_color = (255, 255, 0) if self.selected_option == 0 else (255, 255, 255) #color for cont
        restart_color = (255, 255, 0) if self.selected_option == 1 else (255, 255, 255) # color for restart
        quit_color = (255, 255, 0) if self.selected_option == 2 else (255, 255, 255) # color for quit

        continue_surface = self.font_small.render("Continue", True, continue_color) # surface for cont
        restart_surface = self.font_small.render("Restart", True, restart_color) # restart surface
        quit_surface = self.font_small.render("Quit", True, quit_color) # quit surface

        engine_instance.screen.blit(continue_surface, (250, 250)) # blit to screen
        engine_instance.screen.blit(restart_surface, (250, 300)) # blit to screen
        engine_instance.screen.blit(quit_surface, (250, 350)) # blit to screen

        pygame.display.flip() # update screen


# ExampleState manages the main gameplay, handling Cube movement, collisions, and rendering.
class ExampleState:
    # Initializes ExampleState, setting up Cube, Level, and other parameters.
    def __init__(self, level_id = 0, startpoint=[130, 780]):
        # Initialize objects.
        self._startpoint = startpoint # startpoint var to be used w/ checkpoints
        self._cube = Cube(startpoint[1]) # Store the Cube data.
        self._level = Level(levels[level_id], startpoint[0] - 130) # Store the Level data.

        # Initialize physics.
        self._gravity = 1  # Store the gravity data.
        self._jump_strength = -24 # Store the jump strength data.
        self._vertical_velocity = 0 # Store the vertical velocity data.

         # Initialize audio.
        self._sound = SoundEffect("./assets/sound.wav") # sound effects just in case we use them
        set_music("./assets/music.wav")  # Set the game music.
        play_music()                     # Play the game music.

        # Initialize movement flags.
        self.moving_left = False # Flag if Cube is currently moving left.
        self.moving_right = False # Flag if Cube is currently moving right.
        self.is_jumping = False # Flag if Cube is currently jumping.

        # Load instructions asset
        self._instructions_image = Image("./assets/instructions.png")  # Load the instructions image.
        self._settings = Image("./assets/settings.png")                # Load the settings image.
        self._background_image = Image("./assets/background.png")  # Load the background

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
                self._startpoint = [obj._base_x, obj._base_y]                                        # Update the startpoint.
            if isinstance(obj, EndFlag):                                                             # If it's an end flag.
                engine_instance.state = GameOverState(self._level, self._cube, self._startpoint, 0)  # The user won.

    def draw(self):
        self._background_image.blit(self._ctr,self._ctr)
        self._ctr -= 1
        self._instructions_image.blit(10, 10)  # Adjust the x, y position as needed
        self._settings.blit(1500, 10)  # Adjust the x, y position as needed
        self._cube.draw() # draw cube
        self._level.draw() # draw level


class GameOverState:
    def __init__(self, level, cube, startpoint, endstate):
        # Store references to the current level and cube to render the background
        self._level = level # level
        self._cube = cube # cube
        self.font_large = pygame.font.SysFont(None, 72)   # Create a large font.
        self.font_small = pygame.font.SysFont(None, 36)   # Create a small font.
        self.selected_option = 2 if endstate == 0 else 0  # Set the selected menu option (0 = Restart, 1 = Quit, 2 = Continue).
        self._startpoint = startpoint                     # Set the startpoint.
        self._endstate = endstate                         # Record the result of the last run.
        
        # Prevents the selection from being reset every tick
        self.last_key_time = 0                           # Record the time of the last key press.
        self.key_delay = 0.2                             # Delay before accepting key presses.


    def update(self):
        """
        Updates the game over menu.
        """
        current_time = time.time() # Record the current time.
        if current_time - self.last_key_time > self.key_delay:         # If enough time has elapsed since the last key press.
            if engine_instance.keyboard.is_key_down(pygame.K_DOWN):    # If the down arrow is pressed.
                self.selected_option = (self.selected_option + 1)      # Cycle through the menu options.
                self.selected_option %= 3 if self._endstate == 0 else 2
                self.last_key_time = current_time                      # Record the time of the key press.
            elif engine_instance.keyboard.is_key_down(pygame.K_UP):    # If the up arrow is pressed.
                self.selected_option = (self.selected_option - 1)      # Cycle through the menu options.
                self.selected_option %= 3 if self._endstate == 0 else 2
                self.last_key_time = current_time                      # Record the time of the key press.

            if engine_instance.keyboard.is_key_down(pygame.K_RETURN):
                self.last_key_time = current_time        # If the return key is pressed.
                if self.selected_option == 0:                               # If Restart is selected.
                    engine_instance.state = ExampleState(self._level.id, self._startpoint)  # Start a new game.
                elif self.selected_option == 1:                             # If Quit is selected.
                    engine_instance.state = OpeningMenuState(self.last_key_time)                                              # Exit the game.
                elif self.selected_option == 2:
                    if self._level.id + 1 in levels:
                        engine_instance.state = ExampleState(self._level.id + 1)
                    else:
                        engine_instance.state = OpeningMenuState(self.last_key_time)

    def draw(self):
        """
        Draws the game over menu.
        """
        self._level.draw()# Draw the level in the background.
        self._cube.draw()# Draw the cube in the background.

        if self._endstate == 0:                                                                # If the user won.
            game_result_surface = self.font_large.render("Level Complete", True, (0, 255, 0))  # Display "Level Complete".
        elif self._endstate == 1:                                                              # If the user lost.
            game_result_surface = self.font_large.render("Game Over", True, (255, 0, 0))       # Display "Game Over".

        # Create the Restart option.
        restart_color = (255, 255, 0) if self.selected_option == 0 else (255, 255, 255)
        restart_surface = self.font_small.render("Restart", True, restart_color)

        # Create the Quit option.
        menu_color = (255, 255, 0) if self.selected_option == 1 else (255, 255, 255)
        menu_surface = self.font_small.render("Main Menu", True, menu_color)

        if self._endstate == 0:
            # Create the continue option.
            continue_color = (255, 250, 0) if self.selected_option == 2 else (255, 255, 255)
            continue_surface = self.font_small.render("Continue", True, continue_color)

            engine_instance.screen.blit(continue_surface, (250, 300))
            engine_instance.screen.blit(restart_surface, (250, 350))
            engine_instance.screen.blit(menu_surface, (250, 400))
        elif self._endstate == 1:
            engine_instance.screen.blit(restart_surface, (250, 300))
            engine_instance.screen.blit(menu_surface, (250, 350))

def main():
    """
    Sets the initial game state and passes control to the engine.
    """
    engine_instance.state = OpeningMenuState(0)  # Set the initial game state.
    engine_instance.run_loop()              # Pass control to the engine.


# Main entry point.
if __name__ == "__main__": # magic
    main() # call main
