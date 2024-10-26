# This is the testing grounds for our program.

from audio import *
import sys
from engine import Engine, engine_instance
from image import Image
from sound_effect import SoundEffect
import time

class Object:
    def __init__(self, image_path, x, y, width, height):
        self._image = Image(image_path)
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._rect = pygame.Rect(x, y, width, height)

    def draw(self):
        self._image.blit(self._rect.x, self._rect.y)

    # Debug hitbox
    def draw_rect(self, screen, color=(255, 0, 0)): 
        pygame.draw.rect(screen, color, self._rect, 2) 

    def get_position(self):
        return self._x, self._y

    def get_size(self):
        return self._width, self._height
    
class Cube(Object):
    def __init__(self):
        super().__init__("./assets/cube.png", 130, 330, 120, 120)

    def move(self, x, y, level):
        collision_checks = {'top': False, 'bottom': False, 'left': False, 'right': False}
        collides_with = []

        self._rect.x += x
        collision_list = level.get_collisions(self)

        # Handle horizontal collisions
        for obj in collision_list:
            if x > 0:  # Moving right
                self._rect.right = obj._rect.left  # Push cube back to the left edge of the object
                collides_with.append(obj)
                collision_checks['right'] = True
            elif x < 0:  # Moving left
                self._rect.left = obj._rect.right  # Push cube back to the right edge of the object
                collides_with.append(obj)
                collision_checks['left'] = True

        self._rect.y += y
        collision_list = level.get_collisions(self)
        
        # Handle vertical collisions
        for obj in collision_list:
            if y > 0:  # Falling
                self._rect.bottom = obj._rect.top  # Snap to the top of the object
                collides_with.append(obj)
                collision_checks['bottom'] = True
            elif y < 0:  # Jumping up
                self._rect.top = obj._rect.bottom  # Snap to the bottom of the object
                collides_with.append(obj)
                collision_checks['top'] = True

        return collision_checks, collides_with

class Ground(Object):
    def __init__(self, x, y):
        super().__init__("./assets/ground.png", x, y, 800, 150)

class Spikes(Object):
    def __init__(self, x, y):
        super().__init__("./assets/spikes.png", x, y, 120, 121) # The asset has an extra width pixel.

class Level:
    def __init__(self):
        self._ground = [Ground(0, 450), Ground(-700, 300)]
        self._hazards = [Spikes(300, 330), Spikes(600, 330)]

    def get_ground(self):
        return self._ground
    
    def get_hazards(self):
        return self._hazards
    
    def draw(self):
        for ground in self._ground:
            ground.draw()
            ground.draw_rect(engine_instance.screen)
        for hazard in self._hazards:
            hazard.draw()
            hazard.draw_rect(engine_instance.screen)

    def get_collisions(self, cube):
        collision_list = []
        for ground in self._ground:
            if cube._rect.colliderect(ground._rect):
                collision_list.append(ground)
        for hazard in self._hazards:
            if cube._rect.colliderect(hazard._rect):
                collision_list.append(hazard)
        return collision_list

# Eventually an implemented state will inherit from the abstract state class. 
class ExampleState:
    def __init__(self):
        self._cube = Cube()
        self._level = Level()
        self._gravity = 1
        self._jump_strength = -24
        self._vertical_velocity = 0
        self._sound = SoundEffect("./assets/sound.wav")
        set_music("./assets/music.wav")
        play_music()

        # Initialize movement flags
        self.moving_left = False
        self.moving_right = False
        self.is_jumping = False

    def update(self):
        # Reset vertical velocity if the cube is on the ground
        if not self._level.get_collisions(self._cube):
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
            horizontal_movement = -10
        elif self.moving_right:
            horizontal_movement = 10

        # Move the cube with the current vertical velocity
        collisions, collides_with = self._cube.move(horizontal_movement, self._vertical_velocity, self._level)

        # Stop jumping and reset when we hit the ground
        if collisions['bottom']:
            self.is_jumping = False
            self._vertical_velocity = 0  # Reset velocity for the next jump

        if engine_instance.keyboard.is_key_down(pygame.K_s):
            self._sound.play()

        if engine_instance.keyboard.is_key_down(pygame.K_m):
            unpause_music()

        if engine_instance.keyboard.is_key_down(pygame.K_p):
            pause_music()

        for obj in collides_with:
            if isinstance(obj, Spikes):
                engine_instance.state = GameOverState(self._level, self._cube)

    def draw(self):
        self._cube.draw()
        self._cube.draw_rect(engine_instance.screen)
        self._level.draw()

class GameOverState:
    def __init__(self, level, cube):
        # Store references to the current level and cube to render the background
        self._level = level
        self._cube = cube
        self.font_large = pygame.font.SysFont(None, 72)
        self.font_small = pygame.font.SysFont(None, 36)
        self.selected_option = 0  # 0 = Restart, 1 = Quit

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
                    engine_instance.state = ExampleState()
                elif self.selected_option == 1:  # Quit the game
                    sys.exit()

    def draw(self):
        # Draw level in the background
        self._level.draw()
        self._cube.draw()

        # Game over menu, can be reformatted to match requirements
        game_over_surface = self.font_large.render("Game Over", True, (255, 0, 0))
        engine_instance.screen.blit(game_over_surface, (200, 200))

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
