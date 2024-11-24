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
    Oct 24, 2024: Added basic collision detection, level class, modularized level related objects, added game over state - Matthew Sullivan
    Nov 9, 2024: Moved level functionality out of test.py and updated how levels are specified - Sean Hammell
    Nov 9, 2024: Began implementing level 1 - Sean Hammell
    Nov 9, 2024: Added extra information about the new layout specifications - Sean Hammell
    Nov 9, 2024: Update all sprites - Jacob Leehy
    Nov 9, 2024: Adjust collision intercations to fix vertical tracking - Jacob Leehy
    Nov 10, 2024: Added extra information about the new layout specifications - Sean Hammell
    Nov 10, 2024: Added Cube object into level.py - Mario Simental
    Nov 10, 2024: Redesign level 0 and add level 1 - Jacob Leehy
    Nov 11, 2024: Added gravity inverter object - Matthew Sullivan
    Nov 23, 2024: Updated Level and level0 to be tile-based - Sean Hammell

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


from object import Object, TILE_SIZE

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 800

HORIZONTAL_TILES = int(SCREEN_WIDTH / TILE_SIZE) - 1
VERTICAL_TILES = int(SCREEN_HEIGHT / TILE_SIZE) - 1

GROUND_LEVEL = VERTICAL_TILES - 2

# A Cube is an Object which represents the playable entity in the game.
class Cube(Object):
    # Initializes a Cube with the image path, size and position.
    def __init__(self):
        """
        Initializes a Cube object.
        """
        super().__init__("assets/cube.png", 4, GROUND_LEVEL, TILE_SIZE, TILE_SIZE) #supers init

    # Moves the Cube and handles collisions.
    def move(self, y, level):
        """
        Moves the Cube and handles collisions.
        """
        collision_checks = {'top': False, 'bottom': False, 'left': False, 'right': False} # Track collisions on each side.
        collides_with = [] # List of objects the Cube collides with.
            
        collision_list = level.get_collisions(self) # Get objects colliding with Cube after a horizontal movement.

        # Handle horizontal collisions.
        for obj in collision_list: #iterate over objects
            if not (isinstance(obj, Ground) or isinstance(obj, CheckpointFlag) or isinstance(obj, EndFlag)): #only handle collisions for objects that shouldnt be moved through
                self._rect.right = obj._rect.left  # Push cube back to the left edge of the object
                collision_checks['right'] = True # Update right-side collision.
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

        for obj in level._environment: #move every object in the environment list
            obj.move_object(y) #move each object

        for hazard in level._hazards: #move every object in the hazard list
            hazard.move_object(y) # move each hazard

        return collision_checks, collides_with # Return collision data.

class Ground(Object): #class for ground
    def __init__(self, x, y, id):
        """
        Initializes a ground tile.
        """
        if id == 0:
            super().__init__("assets/ground.png", x, y, TILE_SIZE, TILE_SIZE) #supers with dimensions
        elif id == 1:
            super().__init__("assets/lvl2Ground.png", x, y, TILE_SIZE, TILE_SIZE) #supers with dimensions
        elif id == 2:
            super().__init__("assets/sandGround.png", x, y, TILE_SIZE, TILE_SIZE) #supers with dimensions
        elif id == 3:
            super().__init__("assets/iceGround.png", x, y, TILE_SIZE, TILE_SIZE) #supers with dimensions

class GroundLower(Object): #class for ground
    def __init__(self, x, y, id):
        """
        Initializes a ground tile.
        """
        if id == 0:
            super().__init__("assets/groundLower.png", x, y, TILE_SIZE, TILE_SIZE) #supers with dimensions
        elif id == 1:
            super().__init__("assets/lvl2GroundLower.png", x, y, TILE_SIZE, TILE_SIZE) #supers with dimensions
        elif id == 2:
            super().__init__("assets/sandGroundLower.png", x, y, TILE_SIZE, TILE_SIZE) #supers with dimensions
        elif id == 3:
            super().__init__("assets/iceGroundLower.png", x, y, TILE_SIZE, TILE_SIZE) #supers with dimensions

class Platform(Object): # class for platform
    def __init__(self, x, y):
        """
        Initializes a platform tile.
        """
        super().__init__("assets/platform.png", x, y, TILE_SIZE, TILE_SIZE)#supers with dimensions

class CheckpointFlag(Object): #class for checkpoint
    def __init__(self, x, y):
        """
        Initializes a flag to serve as a mid-level checkpoint.
        """
        super().__init__("assets/checkpoint.png", x, y, TILE_SIZE, TILE_SIZE * 2)#supers with dimensions

class EndFlag(Object): #class for end flag
    def __init__(self, x, y):
        """
        Initializes a flag to signify the end of a level.
        """
        super().__init__("assets/end.png", x, y, TILE_SIZE, TILE_SIZE * 2)#supers with dimensions

class Spikes(Object): # class for spikes
    def __init__(self, x, y, id):
        """
        Initializes a hazardous spikes tile.
        """
        if id == 0:
            super().__init__("assets/spikes.png", x, y, TILE_SIZE, TILE_SIZE) #supers with dimensions
        elif id == 1:
            super().__init__("assets/lvl2Spikes.png", x, y, TILE_SIZE, TILE_SIZE) #supers with dimensions
        elif id == 2:
            super().__init__("assets/sandSpikes.png", x, y, TILE_SIZE, TILE_SIZE) #supers with dimensions
        elif id == 3:
            super().__init__("assets/iceSpikes.png", x, y, TILE_SIZE, TILE_SIZE) #supers with dimensions



class InvertGravity(Object):
    def __init__(self, x, y):
        """
        Initializes a gravity inverter object 
        """
        super().__init__("assets/g1.png", x, y, 100, 100) #supers with dimensions


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

# # Enhanced Tutorial level layout specification for a more interesting Level 0.
level0 = {
    "id": 0,
    "ground": (-10, 200),
    "platforms": [
        (110, 112, GROUND_LEVEL - 2),
        (120, 122, GROUND_LEVEL - 4),
    ],
    "checkpoints": [
        (80, GROUND_LEVEL - 1)
    ],
    "spikes":[
        (20, 22, GROUND_LEVEL),
        (30, 32, GROUND_LEVEL),
        (40, 42, GROUND_LEVEL),
        (50, 52, GROUND_LEVEL),
        (108, 124, GROUND_LEVEL)
    ],
    "end": (160, GROUND_LEVEL - 1)
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
    "iceSpikes": [ #spikes
    ],
    "end": (35000, 780), # end flag
}


# Level 1 layout specification.
level2 = {
    "id": 2, # level id
    "ground": (-240, 40000), # ground range
    "platforms": [
        (3600, 750), #platforms
        (4400, 600), #platforms
        (5500, 750), #platforms
        (8300, 750), #platforms
        (8700, 750), #platforms
        (8900, 750), #platforms
        (10400, 550), #platforms
        (11900, 350), #platforms
    ],
    "checkpoints": [(17400, 780)], #checkpoint
    "spikes": [ #spikes
         ],
    "iceSpikes": [ #spikes
        (1200, 1320, 780), #spikes
        (2400, 2520, 780), #spikes
        (3600, 5660, 780), #spikes
        (7000, 7120, 780), #spikes
        (8500, 11000, 780), #spikes
        (19000, 19120, 780), #spikes
        (21000, 21120, 780), #spikes
        (25000, 25120, 780), #spikes
        (29000, 29120, 780), #spikes
    ],
    "end": (35000, 780), # end flag
}
# Level 1 layout specification.
level3 = {
    "id": 3, # level id
    "ground": (-240, 40000), # ground range
    "platforms": [
    ],
    "checkpoints": [(17400, 780)], #checkpoint
    "spikes": [ #spikes
         ],
    "iceSpikes": [ #spikes
    ],
    "end": (35000, 780), # end flag
}

levels = { # levels
    0: level0, #level 0
    1: level1, # level 1
    2: level2,
    3: level3,
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

        for x in range(specs["ground"][0], specs["ground"][1]):  # For the range of x positions in the ground list.
            for i in range(-1, 3):
                if i == -1:
                    self._environment.append(Ground(x, VERTICAL_TILES + i, self.id))                  # Create a ground tile.
                else:
                    self._environment.append(GroundLower(x, VERTICAL_TILES + i, self.id))                  # Create a lower ground tile.


        for group in specs["platforms"]:                               # For each position in the platform list.
            for x in range(group[0], group[1]):
                self._environment.append(Platform(x, group[2]))  # Create a platform.

        for checkpoint in specs["checkpoints"]:                                     # For each position in the checkpoint list.
            self._environment.append(CheckpointFlag(checkpoint[0], checkpoint[1]))  # Create a checkpoint flag.

        for group in specs["spikes"]:                      # For each position in the spikes list.
            for x in range(group[0], group[1]):       # for the range of x positions in the spike set.
                self._hazards.append(Spikes(x, group[2], self.id))  # Create a set of spikes.

        # for IceSpike in specs["iceSpikes"]:                      # For each position in the spikes list.
        #     for x in range(IceSpike[0], IceSpike[1], 120):       # for the range of x positions in the spike set.
        #         self._hazards.append(IceSpikes(x, IceSpike[2]))  # Create a set of spikes.

        self._environment.append(EndFlag(specs["end"][0], specs["end"][1]))  # Create the end flag.

        for obj in self._environment + self._hazards:    # For each environment object.
            obj.move_x(start[0] * TILE_SIZE)                            # Offset it to the start position.

    def draw(self):
        """
        Draws all environment and hazard objects.
        """
        for obj in self._environment + self._hazards: #iterate over environment and hazards
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
