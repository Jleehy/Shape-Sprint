"""
test.py
Description: This is the testing grounds of the program.
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
        
        self._counter = 0
        self._acceleration = 0
        

    # Draws the object image at the position defined by its hitbox.
    def draw(self):
        self._image.blit(self._rect.x, self._rect.y) 

    # Draws the hitbox rectangle outline.
    def draw_hitbox(self, screen, color=(255, 0, 0)): 
        pygame.draw.rect(screen, color, self._rect, 2) 

    # Returns the position of the object as a tuple (x, y).
    def get_position(self):
        return self._x, self._y

    # Returns the size of the object as a tuple (width, height).
    def get_size(self):
        return self._width, self._height

    def moveObject(self, amount):
        self._counter += 1
        if self._counter == 75:
            self._counter = 0
            self._acceleration += 3

        self._rect.x -= amount + 5 + self._acceleration


    
    def moveX(self, shiftAmmount):
        self._rect.x -= shiftAmmount

# A Cube is an Object which represents the playable entity in the game.
class Cube(Object):
    # Initializes a Cube with the image path, size and position.
    def __init__(self, startY):
        super().__init__("./assets/cube.png", 130, startY, 120, 120)

    # Moves the Cube and handles collisions.
    def move(self, x, y, level):
        collision_checks = {'top': False, 'bottom': False, 'left': False, 'right': False} # Track collisions on each side.
        collides_with = [] # List of objects the Cube collides with.

        for platform in level._ground:
            platform.moveObject(x)
        for hazard in level._hazards:
            hazard.moveObject(x)

        collision_list = level.get_collisions(self) # Get objects colliding with Cube after a horizontal movement.

        # Handle horizontal collisions.
        for obj in collision_list:
            if not (isinstance(obj, CheckpointFlag) or isinstance(obj, EndFlag)):
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
        for obj in collision_list:
            if not (isinstance(obj, CheckpointFlag) or isinstance(obj, EndFlag)):
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
        super().__init__("./assets/ground.png", x, y, 800, 150)

class Ground2(Object):
    # Initializes Ground with the image path, size and position.
    def __init__(self, x, y):
        super().__init__("./assets/ground2.png", x, y, 200, 25)

class EndFlag(Object):
    def __init__(self, x, y):
        super().__init__("./assets/end.png", x, y, 60, 20)

class CheckpointFlag(Object):
    def __init__(self, x, y):
        super().__init__("./assets/checkpoint.png", x, y, 60, 120)


# Spikes is an Object which represents a tile hazard in the game.
class Spikes(Object):
    # Initializes Ground with the image path, size and position.
    def __init__(self, x, y):
        super().__init__("./assets/spikes.png", x, y, 120, 121)


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
        return self._ground
    
    # Return a list of the hazard objects.
    def get_hazards(self):
        return self._hazards
    
    # Draws all ground and hazard objects on the screen.
    def draw(self):
        for ground in self._ground:
            ground.draw()
        for hazard in self._hazards:
            hazard.draw()

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

# ExampleState manages the main gameplay, handling Cube movement, collisions, and rendering.
class ExampleState:
    # Initializes ExampleState, setting up Cube, Level, and other parameters.
    def __init__(self, startpoint=[130, 330]):
        # Initialize objects.
        self._startpoint = startpoint
        self._cube = Cube(startpoint[1]) # Store the Cube data.
        self._level = Level(startpoint[0] - 130) # Store the Level data.

        # Initialize physics.
        self._gravity = 1  # Store the gravity data.
        self._jump_strength = -24 # Store the jump strength data.
        self._vertical_velocity = 0 # Store the vertical velocity data.

         # Initialize audio.
        self._sound = SoundEffect("./assets/sound.wav")
        set_music("./assets/music.wav")
        play_music()

        # Initialize movement flags.
        self.moving_left = False # Flag if Cube is currently moving left.
        self.moving_right = False # Flag if Cube is currently moving right.
        self.is_jumping = False # Flag if Cube is currently jumping.


    
    # Function to update speed text when the speed or acceleration changes
    def update_speed_text(self, amount):
        self.speed_text_surface = self.font.render(
            f"Current Speed: {amount + 5 + self._acceleration}", True, (255, 255, 255)
        )

    # Updates Cube position and handles input for movement and sound control.
    def update(self):
        
        # Reset vertical velocity if the cube is on the ground
        if (not self._level.get_collisions(self._cube)) or all((isinstance(obj, EndFlag) or isinstance(obj, CheckpointFlag)) for obj in self._level.get_collisions(self._cube)): #this is a long complicated line of code.... checks if no collosions or if all colisions are either EndFlag or CheckpointFlag types
            self._vertical_velocity += self._gravity  # Apply gravity when not grounded
        else:
            self._vertical_velocity = 0  # Reset velocity when grounded

        # Update movement flags based on key states
        self.moving_left = engine_instance.keyboard.is_key_down(pygame.K_LEFT)
        self.moving_right = engine_instance.keyboard.is_key_down(pygame.K_RIGHT)


        if engine_instance.keyboard.is_key_down(pygame.K_UP):
            if not self.is_jumping:
                self._vertical_velocity = self._jump_strength  # Set initial jump velocity
                self.is_jumping = True

        # Determine the horizontal movement based on flags
        horizontal_movement = 0
        if self.moving_left:
            horizontal_movement = -3
        elif self.moving_right:
            horizontal_movement = 10

        # Move the cube with the current vertical velocity
        collisions, collides_with = self._cube.move(horizontal_movement, self._vertical_velocity, self._level)

        # Stop jumping and reset when we hit the ground
        if collisions['bottom']:
            self.is_jumping = False
            self._vertical_velocity = 0  # Reset velocity for the next jump
        '''
        if engine_instance.keyboard.is_key_down(pygame.K_s):
            self._sound.play()

        if engine_instance.keyboard.is_key_down(pygame.K_m):
            unpause_music()

        if engine_instance.keyboard.is_key_down(pygame.K_p):
            pause_music()
        '''
        for obj in collides_with:
            if isinstance(obj, Spikes):
                engine_instance.state = GameOverState(self._level, self._cube, self._startpoint, 1)
            if isinstance(obj, CheckpointFlag):
                self._startpoint = [obj._x, obj._y]
            if isinstance(obj, EndFlag):
                engine_instance.state = GameOverState(self._level, self._cube, self._startpoint, 0)

        

    def draw(self):
        self._cube.draw()
        self._level.draw()

class GameOverState:
    def __init__(self, level, cube, startpoint, endstate):
        # Store references to the current level and cube to render the background
        self._level = level
        self._cube = cube
        self.font_large = pygame.font.SysFont(None, 72)
        self.font_small = pygame.font.SysFont(None, 36)
        self.selected_option = 0  # 0 = Restart, 1 = Quit
        self._startpoint = startpoint
        self._endstate = endstate

        # Prevents the selection from being reset every tick
        self.last_key_time = 0
        self.key_delay = 0.2

    def update(self):
        current_time = time.time()

        if current_time - self.last_key_time > self.key_delay:  # Only accept input after key delay
            if engine_instance.keyboard.is_key_down(pygame.K_DOWN):
                self.selected_option = (self.selected_option + 1) % 2
                self.last_key_time = current_time

            if engine_instance.keyboard.is_key_down(pygame.K_UP):
                self.selected_option = (self.selected_option - 1) % 2
                self.last_key_time = current_time

            if engine_instance.keyboard.is_key_down(pygame.K_RETURN):
                if self.selected_option == 0:  # Restart the game
                    engine_instance.state = ExampleState(self._startpoint)
                elif self.selected_option == 1:  # Quit the game
                    sys.exit()

    def draw(self):
        # Draw level in the background
        self._level.draw()
        self._cube.draw()

        # Game over menu, can be reformatted to match requirements
        if self._endstate == 0:
            game_result_surface = self.font_large.render("Level Complete", True, (0, 255, 0))
        elif self._endstate == 1:
            game_result_surface = self.font_large.render("Game Over", True, (255, 0, 0))
        engine_instance.screen.blit(game_result_surface, (200, 200))

        # Menu options
        restart_color = (255, 255, 0) if self.selected_option == 0 else (255, 255, 255)
        quit_color = (255, 255, 0) if self.selected_option == 1 else (255, 255, 255)

        restart_surface = self.font_small.render("Restart", True, restart_color)
        quit_surface = self.font_small.render("Quit", True, quit_color)

        engine_instance.screen.blit(restart_surface, (250, 300))
        engine_instance.screen.blit(quit_surface, (250, 350))

        pygame.display.flip()

# Main function.
def main():
    engine_instance.state = ExampleState()
    engine_instance.run_loop()

# Main entry point.
if __name__ == "__main__":
    main()
