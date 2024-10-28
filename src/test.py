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
import sys # Imports system-specific parameters and functions.
from audio import * # Imports audio-related functions.
from engine import Engine, engine_instance # Imports the Engine class and a singleton instance.
from image import Image # Imports the Image class for handling images.
from sound_effect import SoundEffect # Imports the SoundEffect class for handling sound effects.
import time # Imports the time module for handling delays.

# An Object is a visual entity within the game, which encapsulates image rendering and position handling.
class Object:
    # Initializes an Object given: image_path, position, and size.
    def __init__(self, image_path, x, y, width, height): 
        self._image = Image(image_path) # Create an Image object given image_path.
        self._x = x # Store the x position of the object.
        self._y = y # Store the y position of the object.
        self._width = width # Store the width (pixels) of the object.
        self._height = height # Store the height (pixels) of the object.
        self._rect = pygame.Rect(x, y, width, height) # Store the hitbox of the object.
        self._counter = 0 # counter to be used in calculating acceleration over time
        self._acceleration = 0 # value to store the current speed increace from acceleration
        
    # Draws the object image at the position defined by its hitbox.
    def draw(self):
        self._image.blit(self._rect.x, self._rect.y) #blit the object

    # Draws the hitbox rectangle outline.
    def draw_hitbox(self, screen, color=(255, 0, 0)): 
        pygame.draw.rect(screen, color, self._rect, 2) # draw the object

    # Returns the position of the object as a tuple (x, y).
    def get_position(self):
        return self._x, self._y # return the position components

    # Returns the size of the object as a tuple (width, height).
    def get_size(self):
        return self._width, self._height # return size dimensions

    def moveObject(self, amount):
        """
        Moves the object the specified number of pixels.
        """
        self._counter += 1 #increment counter
        if self._counter == 75: # if 75 frames have passed
            self._counter = 0 #reset frame count
            self._acceleration += 3 #increment acceleration

        self._rect.x -= amount + 5 + self._acceleration # move the object left
        
    def moveX(self, shiftAmmount):
        """
        Shifts the objects left.
        """
        self._rect.x -= shiftAmmount # move x coord

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

        for platform in level._ground: #move every object in the ground list
            platform.moveObject(x) #move each platform

        for hazard in level._hazards: #move every object in the hazard list
            hazard.moveObject(x) # move each hazard
            
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
            
        self._rect.y += y # Update the Cube's vertical position.
        collision_list = level.get_collisions(self) # Get objects colliding with Cube after a vertical movement.
        
        # Handle vertical collisions
        for obj in collision_list: #iterate over objects
            if not (isinstance(obj, CheckpointFlag) or isinstance(obj, EndFlag)): #only handle collisions for objects that shouldnt be moved through
                if y > 0:  # Moving down
                    self._rect.bottom = obj._rect.top  # Snap to the top of the object
                    collision_checks['bottom'] = True # Update bottom-side collision.
                elif y < 0:  # Moving up
                    self._rect.top = obj._rect.bottom  # Snap to the bottom of the object
                    collision_checks['top'] = True # Update top-side collision.
            collides_with.append(obj) # Add object to list of objects the Cube collides with.
            
        return collision_checks, collides_with # Return collision data.

# Ground is an Object which represents a tile platform in the game.
class Ground(Object):
    # Initializes Ground with the image path, size and position.
    def __init__(self, x, y):
        super().__init__("./assets/ground.png", x, y, 800, 150) # super the parameters and set hitbox size

class Ground2(Object): # this is a second ground used to represent platforms
    # Initializes Ground with the image path, size and position.
    def __init__(self, x, y):
        super().__init__("./assets/ground2.png", x, y, 200, 25) # super the parameters and set hitbox size

class EndFlag(Object): # this is a class to represent the end flag
    def __init__(self, x, y): # def the init with x y params
        super().__init__("./assets/end.png", x, y, 60, 120) # super the parameters and set hitbox size

class CheckpointFlag(Object): # class to represent checkpoint flags
    def __init__(self, x, y): # def init w/ x y params
        super().__init__("./assets/checkpoint.png", x, y, 60, 120) # super the parameters and set hitbox size

# Spikes is an Object which represents a tile hazard in the game.
class Spikes(Object):
    # Initializes Ground with the image path, size and position.
    def __init__(self, x, y):
        super().__init__("./assets/spikes.png", x, y, 120, 120) # super the parameters and set hitbox size

# Level holds the ground and hazards and manages their rendering and collision checking.
class Level:
    # Initializes Level with predefined ground and hazard positions.
    def __init__(self, startingX):
        self._ground = [Ground(0, 450), Ground(-700, 300), Ground(-700,-50), Ground(800, 450), Ground(1600, 450), Ground(2400, 450), Ground(3200, 450), Ground(4000, 450), Ground(4800, 450), Ground2(3300, 250), Ground2(3500, 250), CheckpointFlag(3440, 130), EndFlag(5200, 330)] # Ground tiles list.
        self._hazards = [Spikes(600, 330), Spikes(1700, 330), Spikes(3440, 330), Spikes(3800, 330)] # Hazard tiles list.
        for obj in self._ground + self._hazards:
            obj.moveX(startingX)
    
    # Return a list of the ground objects.
    def get_ground(self):
        return self._ground # return ground
    
    # Return a list of the hazard objects.
    def get_hazards(self):
        return self._hazards # return hazards
    
    # Draws all ground and hazard objects on the screen.
    def draw(self):
        for ground in self._ground: # iterate over grounds
            ground.draw() # draw ground
        for hazard in self._hazards: # iterate over hazards
            hazard.draw() # draw hazards

    # Returns a list of objects colliding with the Cube.
    def get_collisions(self, cube):
        collision_list = [] # List holding objects that collide with the Cube.
        for ground in self._ground: # Iterate through every ground object.
            if cube._rect.colliderect(ground._rect): # Check if the object collides with the Cube.
                collision_list.append(ground) # Add it to the collision list if it does collide.
        for hazard in self._hazards: # Iterate through every hazard object.
            if cube._rect.colliderect(hazard._rect): # Check if the object collides with the Cube.
                collision_list.append(hazard) # Add it to the collision list if it does collide.
        return collision_list # Returns the list of objects colliding with the Cube.

class MainMenuState: # class to represent the main menu - this is a bit of a misnomer - needs to be changed to pause menu
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
        menu_surface = self.font_large.render("Main Menu", True, (255, 255, 255)) # make surface for menu
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
    def __init__(self, startpoint=[130, 330]):
        # Initialize objects.
        self._startpoint = startpoint # startpoint var to be used w/ checkpoints
        self._cube = Cube(startpoint[1]) # Store the Cube data.
        self._level = Level(startpoint[0] - 130) # Store the Level data.

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

        if engine_instance.keyboard.is_key_down(pygame.K_UP) and not self.is_jumping:  # If the up arrow is pressed and the cube is not in the air.
                self._vertical_velocity = self._jump_strength                          # Set initial jump velocity.
                self.is_jumping = True                                                 # Set that the cube is in the air.

        self.moving_left = engine_instance.keyboard.is_key_down(pygame.K_LEFT)    # Check if the left arrow is pressed.
        self.moving_right = engine_instance.keyboard.is_key_down(pygame.K_RIGHT)  # Check if the right arrow is pressed.

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
                self._startpoint = [obj._x, obj._y]                                                  # Update the startpoint.
            if isinstance(obj, EndFlag):                                                             # If it's an end flag.
                engine_instance.state = GameOverState(self._level, self._cube, self._startpoint, 0)  # The user won.
                
    def draw(self):
        self._instructions_image.blit(10, 10)  # Adjust the x, y position as needed
        self._settings.blit(700, 10)  # Adjust the x, y position as needed
        self._cube.draw() # draw cube
        self._level.draw() # draw level


class GameOverState:
    def __init__(self, level, cube, startpoint, endstate):
        # Store references to the current level and cube to render the background
        self._level = level # level
        self._cube = cube # cube
        self.font_large = pygame.font.SysFont(None, 72)  # Create a large font.
        self.font_small = pygame.font.SysFont(None, 36)  # Create a small font.
        self.selected_option = 0                         # Set the selected menu option (0 = Restart, 1 = Quit).
        self._startpoint = startpoint                    # Set the startpoint.
        self._endstate = endstate                        # Record the result of the last run.
        
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
        self._level.draw()# Draw the level in the background.
        self._cube.draw()# Draw the cube in the background.

        # Game over menu, can be reformatted to match requirements
        if self._endstate == 0: # If the user won.
            game_result_surface = self.font_large.render("Level Complete", True, (0, 255, 0))# Display "Level Complete".
        elif self._endstate == 1:# If the user lost.
            game_result_surface = self.font_large.render("Game Over", True, (255, 0, 0))# Display "Game Over".
        engine_instance.screen.blit(game_result_surface, (200, 200)) #blit to surface

        # Menu options
        restart_color = (255, 255, 0) if self.selected_option == 0 else (255, 255, 255) # restart color
        quit_color = (255, 255, 0) if self.selected_option == 1 else (255, 255, 255) # quit color

        restart_surface = self.font_small.render("Restart", True, restart_color) # restart surface
        quit_surface = self.font_small.render("Quit", True, quit_color) #quit surface

        engine_instance.screen.blit(restart_surface, (250, 300)) # blit to screen
        engine_instance.screen.blit(quit_surface, (250, 350)) # blit to screen

        pygame.display.flip() #update screen

# Main function.
def main():
    """
    Sets the initial game state and passes control to the engine.
    """
    engine_instance.state = ExampleState()  # Set the initial game state.
    engine_instance.run_loop()              # Pass control to the engine.


# Main entry point.
if __name__ == "__main__": # magic
    main() # call main
