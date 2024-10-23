# This is the testing grounds for our program.

# https://www.pygame.org/docs/

# Import Pygame
import pygame

# Main function
def main():

    # Pygame setup
    pygame.init() # Initialize Pygame
    infoObject = pygame.display.Info() # Get user's display info
    screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h)) # Set window size to user's monitor resolution.
    clock = pygame.time.Clock() # Create a Pygame clock object to track time.
    running = True # Keep track if the program is running.

    # Game loop
    while running:
        for event in pygame.event.get(): # Iterate throgh Pygame's events. https://www.pygame.org/docs/ref/event.html
            if event.type == pygame.QUIT: # If event is quit, set running to false.
                running = False # Set running to false.
    
        screen.fill("grey") # Fill the screen with a grey background.
        pygame.display.flip() # Display the contents.
        clock.tick(60) # Limit FPS to 60.

# Main entry point.
if __name__ == "__main__":
    main()