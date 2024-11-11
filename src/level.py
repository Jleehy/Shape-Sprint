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
    Nov 10, 2024: Added extra information about the new layout specifications - Sean Hammell
    Nov 10, 2024: Added Cube object into level.py - Mario Simental
Preconditions:
Postconditions:
Error Conditions:
Side Effects:
Invariants:
Known Faults:
"""

from object import Object

# A Cube is an Object which represents the playable entity in the game.
class Cube(Object):
    # Initializes a Cube with the image path, size and position.
    def __init__(self, startpoint):
        """
        Initializes a Cube object.
        """
        super().__init__("src/assets/cube.png", 130, startpoint[1], 120, 120) #supers init

    # Moves the Cube and handles collisions.
    def move(self, x, y, level):
        """
        Moves the Cube and handles collisions.
        """
        collision_checks = {'top': False, 'bottom': False, 'left': False, 'right': False} # Track collisions on each side.
        collides_with = [] # List of objects the Cube collides with.
            
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
            
        #self._rect.y += y # Update the Cube's vertical position.
        collision_list = level.get_collisions(self) # Get objects colliding with Cube after a vertical movement.
        
        # Handle vertical collisions
        for obj in collision_list: #iterate over objects
            if not (isinstance(obj, CheckpointFlag) or isinstance(obj, EndFlag)): #only handle collisions for objects that shouldnt be moved through
                if y > 0:  # Moving down
                    self._rect.bottom = obj._rect.top  # Snap to the top of the object
                    collision_checks['bottom'] = True # Update bottom-side collision.
                elif self._rect.top > obj._rect.top:  # Moving up
                    self._rect.top = obj._rect.bottom  # Snap to the bottom of the object
                    collision_checks['top'] = True # Update top-side collision.
            collides_with.append(obj) # Add object to list of objects the Cube collides with.

        for platform in level._environment: #move every object in the environment list
            platform.move_object(x, y) #move each platform

        for hazard in level._hazards: #move every object in the hazard list
            hazard.move_object(x, y) # move each hazard

        return collision_checks, collides_with # Return collision data.

class Ground(Object):
    def __init__(self, x, y):
        """
        Initializes a ground tile.
        """
        super().__init__("src/assets/ground.png", x, y, 800, 150)

class Platform(Object):
    def __init__(self, x, y):
        """
        Initializes a platform tile.
        """
        super().__init__("src/assets/platform.png", x, y, 200, 25)

class CheckpointFlag(Object):
    def __init__(self, x, y):
        """
        Initializes a flag to serve as a mid-level checkpoint.
        """
        super().__init__("src/assets/checkpoint.png", x, y, 60, 120)

class EndFlag(Object):
    def __init__(self, x, y):
        """
        Initializes a flag to signify the end of a level.
        """
        super().__init__("src/assets/end.png", x, y, 60, 120)

class Spikes(Object):
    def __init__(self, x, y):
        """
        Initializes a hazardous spikes tile.
        """
        super().__init__("src/assets/spikes.png", x, y, 120, 120)


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
