# This is the testing grounds for our program.

from audio import *
import sys
from engine import Engine, engine_instance
from image import Image
from sound_effect import SoundEffect
import time

class Level:
    def __init__(self):
        self._ground = Ground()
        self._spikes = [Spikes(300, 330)]

    def get_ground(self):
        return self._ground
    
    def get_spikes(self):
        return self._spikes
    
    def draw(self):
        self._ground.draw()
        for spike in self._spikes:
            spike.draw()
    
    def check_collisions(self, cube):
        for spike in self._spikes:
            if cube._rect.colliderect(spike._rect):
                return True
        return False
    
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

class Object:
    def __init__(self, image_path, x, y, x_size, y_size):
        self._image = Image(image_path)
        self._x = x
        self._y = y
        self._x_size = x_size
        self._y_size = y_size
        self._rect = pygame.Rect(x, y, x_size, y_size)

    def draw(self):
        self._image.blit(self._x, self._y)

    def get_position(self):
        return self._x, self._y

    def get_size(self):
        return self._x_size, self._y_size
    
    def update_rect(self):
        self._rect.topleft = (self._x, self._y)
    
class Cube(Object):
    def __init__(self):
        super().__init__("./assets/cube.png", 0, 330, 120, 120)

    def move(self, x, y):
        self._x += x
        self._y = min(self._y + y, 330)
        self.update_rect()

class Ground(Object):
    def __init__(self):
        super().__init__("./assets/ground.png", 0, 450, 800, 150)

class Spikes(Object):
    def __init__(self, x, y):
        super().__init__("./assets/spikes.png", x, y, 120, 121) # The asset has an extra width pixel.

# Eventually an implemented state will inherit from the abstract state class. 
class ExampleState:
    def __init__(self):
        self._cube = Cube()
        self._level = Level()
        #self._ground = Ground()
        #self._spike = Spikes()
        self._gravity = 1
        self._jump_strength = -24
        self.is_jumping = False
        self._sound = SoundEffect("./assets/sound.wav")
        set_music("./assets/music.wav")
        play_music()

    def update(self):
        
        if engine_instance.keyboard.is_key_down(pygame.K_UP):
            # Only jump if on the ground
            if self._cube.get_position()[1] == 330 and not self.is_jumping:
                self.jump_velocity = self._jump_strength  # Set initial jump velocity
                self.is_jumping = True

        # Apply jump and gravity logic
        if self.is_jumping:
            self._cube.move(0, self.jump_velocity)
            self.jump_velocity += self._gravity  # Gravity gradually increases velocity, simulating a fall

            # Stop jumping and reset when we hit the ground
            if self._cube.get_position()[1] == 330:
                self.is_jumping = False
                self.jump_velocity = 0  # Reset the velocity for the next jump
  
        '''
        if engine_instance.keyboard.is_key_down(pygame.K_DOWN):
            self._cube.move(0, 5)'''

        if engine_instance.keyboard.is_key_down(pygame.K_LEFT):
            self._cube.move(-10, 0)

        if engine_instance.keyboard.is_key_down(pygame.K_RIGHT):
            self._cube.move(10, 0)

        if engine_instance.keyboard.is_key_down(pygame.K_s):
            self._sound.play()

        if engine_instance.keyboard.is_key_down(pygame.K_m):
            unpause_music()

        if engine_instance.keyboard.is_key_down(pygame.K_p):
            pause_music()

        if self._level.check_collisions(self._cube):
            # Transition to game over state on collision
            engine_instance.state = GameOverState(self._level, self._cube)


    def draw(self):
        self._cube.draw()
        self._level.draw()
        #self._ground.draw()
        #self._spike.draw()

# Main function.
def main():
    engine_instance.state = ExampleState()
    engine_instance.run_loop()

# Main entry point.
if __name__ == "__main__":
    main()
