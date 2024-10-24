# This is the testing grounds for our program.

from audio import *
from engine import Engine, engine_instance
from image import Image
from sound_effect import SoundEffect

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
    
class Cube(Object):
    def __init__(self):
        super().__init__("./assets/cube.png", 0, 330, 120, 120)

    def move(self, x, y):
        self._x += x
        self._y = min(self._y + y, 330)

class Ground(Object):
    def __init__(self):
        super().__init__("./assets/ground.png", 0, 450, 800, 150)

class Spikes(Object):
    def __init__(self):
        super().__init__("./assets/spikes.png", 0, 330, 120, 121) # The asset has an extra width pixel.

# Eventually an implemented state will inherit from the abstract state class. 
class ExampleState:
    def __init__(self):
        self._cube = Cube()
        self._ground = Ground()
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

    def draw(self):
        self._cube.draw()
        self._ground.draw()

# Main function.
def main():
    engine_instance.state = ExampleState()
    engine_instance.run_loop()

# Main entry point.
if __name__ == "__main__":
    main()
