import sys

import pygame


class Engine:
    def __init__(self):
        """
        Initializes and Engine object.
        """
        # Initialize pygame.
        pygame.init()

        # Create an 800x600 window with the title "Shape Sprint".
        pygame.display.set_caption("Shape Sprint")
        self.screen = pygame.display.set_mode((800, 600), flags=pygame.SCALED, vsync=1)

        # Start with no state.
        self.state = None

        # To Do.
        self.keyboard = None

    def run_loop(self):
        """
        Controls the game loop.
        """
        # Create a clock to cap the game's FPS.
        clock = pygame.time.Clock()

        while True:
            # Capture an events.
            for event in pygame.event.get():
                # Quit if the window is closed.
                if event.type == pygame.QUIT:
                    sys.exit()

            # Clear the screen.
            self.screen.fill((64, 64, 64))
            pygame.display.flip()

            # Cap the FPS at 75.
            clock.tick(75)


# Global Engine instance.
engine_instance = Engine()
