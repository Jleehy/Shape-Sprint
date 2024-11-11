"""
level.py
Description:
    Represents a level of the game, including environmental features such as ground tiles, platforms,
    checkpoints, and hazards. Provides functionality for loading level specifications, drawing objects,
    and detecting collisions with the Cube character.

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
    Nov 9, 2024: Update all sprites - Jacob Leehy
    Nov 9, 2024: Adjust collision intercations to fix vertical tracking - Jacob Leehy
    Nov 10, 2024: Added extra information about the new layout specifications - Sean Hammell
    Nov 10, 2024: Added Cube object into level.py - Mario Simental
    Nov 10, 2024: Redesign level 0 and add level 1 - Jacob Leehy

Preconditions:
    - Assets such as cube.png, ground.png, platform.png, checkpoint.png, end.png, and spikes.png exist
      in the specified file paths.
    - Input specifications for levels, including ground ranges, platform positions, spike locations,
      checkpoint positions, and end flag positions, must be properly formatted as dictionaries.

Postconditions:
    - A Level object is created with initialized environment and hazard objects that can be used for
      drawing and collision checking.
    - Environment objects and hazards are appropriately offset according to the starting position of the level.

Error Conditions:
    - Missing or improperly formatted level specifications.
    - Invalid asset paths or missing image files.

Side Effects:
    - Modifies the state of objects within the level when moving or colliding with the Cube.
    - Generates drawing calls for all level objects and hazards.

Invariants:
    - Level environment and hazards are properly offset and aligned based on tile dimensions.
    - Collision detection returns accurate results for Cube-object interactions.

Known Faults:
    - The cube can sometimes faze into the ground after landing from jumps. This doesn't affect gameplay, just visuals.
"""


from object import Object

# A Cube is an Object which represents the playable entity in the game.
class Cube(Object):
    # Initializes a Cube with the image path, size and position.
    def __init__(self, startpoint):
        """
        Initializes a Cube object.
        """
        super().__init__("assets/cube.png", 130, startpoint[1], 120, 120) #supers init

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

class Ground(Object): #class for ground
    def __init__(self, x, y):
        """
        Initializes a ground tile.
        """
        super().__init__("assets/ground.png", x, y, 800, 150) #supers with dimensions

class Platform(Object): # class for platform
    def __init__(self, x, y):
        """
        Initializes a platform tile.
        """
        super().__init__("assets/platform.png", x, y, 200, 25)#supers with dimensions

class CheckpointFlag(Object): #class for checkpoint
    def __init__(self, x, y):
        """
        Initializes a flag to serve as a mid-level checkpoint.
        """
        super().__init__("assets/checkpoint.png", x, y, 60, 120)#supers with dimensions

class EndFlag(Object): #class for end flag
    def __init__(self, x, y):
        """
        Initializes a flag to signify the end of a level.
        """
        super().__init__("assets/end.png", x, y, 60, 120)#supers with dimensions

class Spikes(Object): # class for spikes
    def __init__(self, x, y):
        """
        Initializes a hazardous spikes tile.
        """
        super().__init__("assets/spikes.png", x, y, 120, 120)#supers with dimensions


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

# Enhanced Tutorial level layout specification for a more interesting Level 0.
level0 = {
    "id": 0, # level id
    "ground": (-240, 30000),  # Extended ground length to 25,000 units
    "platforms": [], # platforms list
    "checkpoints": [ # checkpoint list
        (5000, 780), # new checkpoint
        (20000, 780),  # New checkpoint added
    ],
    "spikes": [ # list for spikes
        (700, 820, 780),  #spikes
        (1600, 1720, 780), #spikes
        (2500, 2600, 780), #spikes
        (3700, 3820, 780), #spikes
        (6000, 6120, 780), #spikes
        (9200, 9320, 780), #spikes
        (9800, 9920, 780), #spikes
        (11000, 11120, 780), #spikes
        (12500, 12620, 780), #spikes
        (13200, 13320, 780), #spikes
        (14500, 15340, 780), #spikes
        (16800, 16920, 780), #spikes
        (18500, 18620, 780), #spikes
        (19500, 19620, 780),  # New spike segment after the 20,000 checkpoint
        (23000, 24200, 780), #spikes
    ],
    "end": (29000, 780),  # Moved end to 24,500 to complete the longer level
}


# Level 1 layout specification.
level1 = {
    "id": 1, # level id
    "ground": (-240, 40000), # ground range
    "platforms": [
        (3600, 750), #platforms
        (4600, 600), #platforms
        (5600, 750), #platforms
        (8500, 750), #platforms
        (8700, 750), #platforms
        (8900, 750), #platforms
        (10400, 550), #platforms
        (11900, 350), #platforms


        
    ],
    "checkpoints": [(17400, 780)], #checkpoint
    "spikes": [ #spikes
        (1200, 1320, 780), #spikes
        (2400, 2520, 780), #spikes
        (3600, 5880, 780), #spikes
        (7000, 7120, 780), #spikes
        (8500, 11000, 780), #spikes
        (19000, 19120, 780), #spikes
        (21000, 21120, 780), #spikes
        (25000, 25120, 780), #spikes
        (29000, 29120, 780), #spikes


    ],
    "end": (35000, 780), # end flag
}


levels = { # levels
    0: level0, #level 0
    1: level1, # level 1
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
        for obj in self._environment + self._hazards: #iterate over environment anf hazards
            obj.draw() # draw everything

    def get_collisions(self, cube):
        """
        Returns a list of objects colliding with the cube.
        """
        collision_list = []                               # List of objects colliding with the Cube.
        for object in self._environment + self._hazards:  # For each object in the level.
            if cube._rect.colliderect(object._rect):      # If the object collides with the cube.
                collision_list.append(object)             # Add it to the collision list.

        return collision_list  # Return the collision list.
