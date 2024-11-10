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
    Nov 9, 2024: Began implementing level 1 - Sean Hammell
    Nov 9, 2024: Added extra information about the new layout specifications - Sean Hammell
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


"""
A note on the level specifications:
    Each level specification is a dictionary storing the positions of the environment
    objects and hazards in the level.

    'ground' stores the range of (x0, x1) range of ground tiles. In other words, this is
    how long the level is.

    'spikes' stores the (x0, x1, y) position of each set of spikes. For example,
    (0, 240, 780) will lay spikes from 0 to 240 on the x-axis at a height of 780.

    Since 'ground' and 'spikes' store ranges, when the Level parses them, it iterates
    over the ranges in steps equal to the width of the tiles (120 at the time of
    writing).

    'platforms' stores the (x, y) position of each platform tile.

    'checkpoints' stores the (x, y) position of each checkpoint flag.

    'end' stores the (x, y) position of the end flag
"""

# Tutorial level layout specification.
level0 = {
    "id": 0,
    "ground": (-240, 10000),
    "platforms": [
        (3300, 750),
        (3500, 750),
    ],
    "checkpoints": [
        (3440, 630),
    ],
    "spikes": [
        (600, 720, 780),
        (1700, 1820, 780),
        (3440, 3560, 780),
        (3800, 3920, 780),
    ],
    "end": (5200, 780),
}

# Level 1 layout specification.
level1 = {
    "id": 1,
    "ground": (-240, 40000),
    "platforms": [
        (3600, 750),
        (4600, 600),
        (5600, 750),
        (8500, 750),
        (8700, 750),
        (8900, 750),
        (10400, 550),
        (11900, 350),


        
    ],
    "checkpoints": [(17400, 780)],
    "spikes": [
        (1200, 1320, 780),
        (2400, 2520, 780),
        (3600, 5880, 780),
        (7000, 7120, 780),
        (8500, 11000, 780),
        (19000, 19120, 780),
        (21000, 21120, 780),
        (25000, 25120, 780),
        (29000, 29120, 780),


    ],
    "end": (35000, 780),
}

'''
# Level 1 layout specification.
level2 = {
    "ground": (0, 50000),
    "platforms": [
        (3600, 750),
        (4600, 600),
        (5600, 750),
        (8500, 750),
        (8700, 750),
        (8900, 750),
        (10400, 550),
        (11900, 350),


        
    ],
    "checkpoints": [(18000, 780)],
    "spikes": [
        (1200, 1320, 780),
        (2400, 2520, 780),
        (3600, 5880, 780),
        (7000, 7120, 780),
        (8500, 11000, 780),
        (19000, 19120, 780),
        (21000, 21120, 780),
        (25000, 25120, 780),
        (29000, 29120, 780),


    ],
    "end": (35000, 780),
}
'''
levels = {
    0: level0,
    1: level1,
}

class Level:
    """
    Levels stores, manages, and checks for collisions with the environment and hazards of the game.
    """
    def __init__(self, specs, start):
        """
        Initializes the level environment, hazards, and starting position.
        """
        self.id = specs["id"]   # Record the level ID.
        self._environment = []  # Create an empty environment list.
        self._hazards = []      # Create an empty hazards list.

        for x in range(specs["ground"][0], specs["ground"][1], 120):  # For the range of x positions in the ground list.
            self._environment.append(Ground(x, 900))                  # Create a ground tile.

        for platform in specs["platforms"]:                               # For each position in the platform list.
            self._environment.append(Platform(platform[0], platform[1]))  # Create a platform.
        
        for checkpoint in specs["checkpoints"]:                                     # For each position in the checkpoint list.
            self._environment.append(CheckpointFlag(checkpoint[0], checkpoint[1]))  # Create a checkpoint flag.

        for spike in specs["spikes"]:                      # For each position in the spikes list.
            for x in range(spike[0], spike[1], 120):       # for the range of x positions in the spike set.
                self._hazards.append(Spikes(x, spike[2]))  # Create a set of spikes.

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
