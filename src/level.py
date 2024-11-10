"""
level.py
Description:
    Represents a level of the game.
Programmers:
    Steve Gan
    Sean Hammell
    Jacob Leehy
    Mario Simental
    Matthew Sullivan
Created:
    Nov 9, 2024
Revisions:
    Nov 9, 2024: Moved level functionality out of test.py and updated how levels are specified - Sean Hammell
Preconditions:
Postconditions:
Error Conditions:
Side Effects:
Invariants:
Known Faults:
"""

from object import Object

class Ground(Object):
    def __init__(self, x, y):
        """
        Initializes a ground tile.
        """
        super().__init__("./assets/ground.png", x, y, 800, 150)

class Platform(Object):
    def __init__(self, x, y):
        """
        Initializes a platform tile.
        """
        super().__init__("./assets/platform.png", x, y, 200, 25)

class CheckpointFlag(Object):
    def __init__(self, x, y):
        """
        Initializes a flag to serve as a mid-level checkpoint.
        """
        super().__init__("./assets/checkpoint.png", x, y, 60, 120)

class EndFlag(Object):
    def __init__(self, x, y):
        """
        Initializes a flag to signify the end of a level.
        """
        super().__init__("./assets/end.png", x, y, 60, 120)

class Spikes(Object):
    def __init__(self, x, y):
        """
        Initializes a hazardous spikes tile.
        """
        super().__init__("./assets/spikes.png", x, y, 120, 120)

# Tutorial level layout specification.
level0 = {
    "ground": [
        (0, 900),
        (-700, 750),
        (-700, -50),
        (800, 900),
        (1600, 900),
        (2400, 900),
        (3200, 900),
        (4000, 900),
        (4800, 900),
    ],
    "platforms": [
        (3300, 750),
        (3500, 750),
    ],
    "checkpoints": [
        (3440, 630),
    ],
    "spikes": [
        (600, 780),
        (1700, 780),
        (3440, 780),
        (3800, 780),
    ],
    "end": (5200, 780),
}


class Level:
    """
    Levels stores, manages, and checks for collisions with the environment and hazards of the game.
    """
    def __init__(self, specs, start):
        """
        Initializes the level environment, hazards, and starting position.
        """
        self._environment = []  # Create an empty environment list.
        self._hazards = []      # Create an empty hazards list.

        for ground in specs["ground"]:                              # For each position in the ground list.
            self._environment.append(Ground(ground[0], ground[1]))  # Create a ground tile.

        for platform in specs["platforms"]:                               # For each position in the platform list.
            self._environment.append(Platform(platform[0], platform[1]))  # Create a platform.
        
        for checkpoint in specs["checkpoints"]:                                     # For each position in the checkpoint list.
            self._environment.append(CheckpointFlag(checkpoint[0], checkpoint[1]))  # Create a checkpoint flag.

        for spike in specs["spikes"]:                         # For each position in the spikes list.
            self._hazards.append(Spikes(spike[0], spike[1]))  # Create a set of spikes.

        self._environment.append(EndFlag(specs["end"][0], specs["end"][1]))  # Create the end flag.

        for obj in self._environment + self._hazards:    # For each environment object.
            obj.move_x(start)                            # Offset it to the start position.

    def get_environment(self):
        """
        Returns the environment tiles.
        """
        return self._environment

    def get_hazards(self):
        """
        Returns the hazard tiles.
        """
        return self._hazards

    # Draws all ground and hazard objects on the screen.
    def draw(self):
        """
        Draws all environment and hazard objects.
        """
        for obj in self._environment + self._hazards:
            obj.draw()

    def get_collisions(self, cube):
        """
        Returns a list of objects colliding with the cube.
        """
        collision_list = []                               # List of objects colliding with the Cube.
        for object in self._environment + self._hazards:  # For each object in the level.
            if cube._rect.colliderect(object._rect):      # If the object collides with the cube.
                collision_list.append(object)             # Add it to the collision list.

        return collision_list  # Return the collision list.
