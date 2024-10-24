# This is the testing grounds for our program.

from audio import *
from engine import Engine, engine_instance
from image import Image
from sound_effect import SoundEffect


class Cube:
    def __init__(self):
        self._image = Image("./assets/cube.png")
        self._x = 0
        self._y = 0

    def move(self, x, y):
        self._x += x
        self._y += y

    def draw(self):
        self._image.blit(self._x, self._y)


class ExampleState:
    def __init__(self):
        self._cube = Cube()
        self._sound = SoundEffect("./assets/sound.wav")
        set_music("./assets/music.wav")
        play_music()

    def update(self):
        if engine_instance.keyboard.is_key_down(pygame.K_UP):
            self._cube.move(0, -5)

        if engine_instance.keyboard.is_key_down(pygame.K_DOWN):
            self._cube.move(0, 5)

        if engine_instance.keyboard.is_key_down(pygame.K_LEFT):
            self._cube.move(-5, 0)

        if engine_instance.keyboard.is_key_down(pygame.K_RIGHT):
            self._cube.move(5, 0)

        if engine_instance.keyboard.is_key_down(pygame.K_s):
            self._sound.play()

        if engine_instance.keyboard.is_key_down(pygame.K_m):
            unpause_music()

        if engine_instance.keyboard.is_key_down(pygame.K_p):
            pause_music()

    def draw(self):
        self._cube.draw()


# Main function.
def main():
    engine_instance.state = ExampleState()
    engine_instance.run_loop()


# Main entry point.
if __name__ == "__main__":
    main()
