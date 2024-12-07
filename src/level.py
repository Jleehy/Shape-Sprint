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
    Nov 21, 2024: Implement new backgrounds and updated assets - Jacob Leehy
    Nov 23, 2024: Updated Level and level0 to be tile-based - Sean Hammell
    Nov 23, 2024: Update and rescale all assets - Jacob Leehy
    Nov 24, 2024: Reimplement levels 1 and 2 - Jacob Leehy
    Nov 24, 2024: Add spped modifier - Jacob Leehy
    Nov 24, 2024: Add automatic asset visual handling - Jacob Leehy
    Dec 07, 2024: Moved screen resolution constants to engine.py - Sean Hammell

Preconditions:
    - Game assets such as 'cube.png', 'ground.png', 'platform.png', 'checkpoint.png', 'end.png', and 
      'spikes.png' must exist and be accessible at their specified paths.
    - Level specifications must be provided in dictionary format with correct key-value mappings for 
      ground, platforms, spikes, checkpoints, and end flag positions.
    - The `Object` class and `TILE_SIZE` constant must be defined and imported correctly.

Postconditions:
    - The `Level` and its components (ground tiles, platforms, spikes, checkpoints, and end flag) are 
      fully initialized and correctly positioned based on the input specifications.
    - Collisions with environmental features and hazards are detectable during gameplay.
    - All graphical elements are drawn correctly within the game window.

Error Conditions:
    - Raises an exception if level specifications are missing or improperly formatted.
    - Raises an exception if required assets are missing or paths to these assets are invalid.
    - Potential game crashes or misbehavior if incompatible level layouts or object types are provided.

Side Effects:
    - Updates the positions of objects relative to the Cube’s movement, creating a scrolling effect.
    - Modifies the state of the Cube or triggers gameplay mechanics (e.g., checkpoint activation, game over)
      based on interactions with level objects or hazards.

Invariants:
    - Tile-based objects (ground, spikes, platforms) are aligned to the tile grid.
    - Collision detection consistently returns accurate results for all object interactions.
    - Hazardous objects (e.g., spikes) always remain within the game’s visible boundaries or scrolling limits.

Known Faults:
    - Occasionally, the Cube visually phases into the ground after landing from jumps, creating a minor 
      visual glitch without affecting gameplay mechanics.

"""

from engine import SCREEN_WIDTH, SCREEN_HEIGHT
from object import Object, TILE_SIZE # import obj and tile size

TOLERANCE = 1 # set tolerance

HORIZONTAL_TILES = int(SCREEN_WIDTH / TILE_SIZE) - 1 # set horizinal tiles
VERTICAL_TILES = int(SCREEN_HEIGHT / TILE_SIZE) - 1 # set vert tiles

GROUND_LEVEL = VERTICAL_TILES - 2 # set ground level

# A Cube is an Object which represents the playable entity in the game.
class Cube(Object):
    # Initializes a Cube with the image path, size, and position.
    def __init__(self):
        """
        Initializes a Cube object.
        """
        super().__init__("assets/cube.png", 4, GROUND_LEVEL, TILE_SIZE, TILE_SIZE)  # super's init

    def move(self, y, level):
        """
        Updates the Cube's state and handles collisions with moving level objects.
        """
        collision_checks = {'top': False, 'bottom': False, 'left': False, 'right': False}  # Track collisions on each side.
        collides_with = []  # List of objects the Cube collides with.
        
        expanded_cube_rect = self._rect.inflate(TOLERANCE, TOLERANCE) # expand cube rect

        # Move all level objects first.
        for obj in level._environment: # iterate over objs
            obj.scroll_object(y) # scroll objs
        for hazard in level._hazards: # iterate over hazards
            hazard.scroll_object(y) # scroll hazards
        # Handle horizontal collisions.
        collision_list = level.get_collisions(self)  # Check collisions after objects have moved.
        for obj in collision_list: # iterate over collisions
            if not isinstance(obj, InvertGravity) and not isinstance(obj, CheckpointFlag) and not isinstance(obj, EndFlag) and not isinstance(obj, SpeedBoost):  # Skip phaseable objects.
                if y > 0 and abs(self._rect.bottom - obj._rect.top) > TOLERANCE*48 or\
                    y < 0 and abs(self._rect.bottom - obj._rect.top) < TOLERANCE*48: # check for needed sdjustments and adjust as needed
                    if self._rect.right > obj._rect.left:  # Moving right into an object.
                        collision_checks['right'] = True # set right collision
                        self._rect.right = obj._rect.left # move rect to left
            collides_with.append(obj) # append to collisions
            collision_list.remove(obj) # remove obj from collision list
        
        # Handle vertical collisions.
        for obj in collision_list: # iterate over objects in collision list
            if not isinstance(obj, InvertGravity) and not isinstance(obj, CheckpointFlag) and not isinstance(obj, EndFlag) and not isinstance(obj, SpeedBoost):  # Skip phaseable objects.
                if y >= 0 and expanded_cube_rect.bottom > obj._rect.top: # if y is greater than 0 aand bottom greater than top
                    collision_checks['bottom'] = True # set bottom to true
                    self._rect.bottom = obj._rect.top # set bottom to rect top
                elif expanded_cube_rect.top < obj._rect.bottom: # if expanded cube less than bottom
                    collision_checks['top'] = True # set collision to true
                    self._rect.top = obj._rect.bottom # set rect top to bottom
            collides_with.append(obj) # append to collisions

        return collision_checks, collides_with # return the lists

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

class InvertGravity(Object): # class to represent grav inversion
    def __init__(self, x, y):
        """
        Initializes a gravity inverter object 
        """
        super().__init__("assets/gravity_flip.png", x, y, TILE_SIZE, TILE_SIZE * 2) #supers with dimensions
        self.activated = False # set activatioon bool to false

class SpeedBoost(Object): # class to represent speed boost
    def __init__(self, x, y):
        """
        Initializes a gravity inverter object 
        """
        super().__init__("assets/speed.png", x, y, TILE_SIZE, TILE_SIZE * 2) #supers with dimensions

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
    "id": 0, # id
    "ground": (-10, 500), #ground
    "platforms": [
        #(20, 28, GROUND_LEVEL - 2),
        #(110, 112, GROUND_LEVEL - 2),
        #(120, 122, GROUND_LEVEL - 4),
    ],
    "checkpoints": [ #checkpotins
        (270, GROUND_LEVEL - 1) #checkpoints
    ],
    "spikes":[ #spikes
        (40, 42, GROUND_LEVEL), #spikes
        (50, 52, GROUND_LEVEL), #spikes
        (78, 84, GROUND_LEVEL), #spikes

        (100, 107, GROUND_LEVEL), #spikes
        (130, 138, GROUND_LEVEL), #spikes
        (180, 190, GROUND_LEVEL), #spikes
        (230, 240, GROUND_LEVEL), #spikes

        (290, 291, GROUND_LEVEL), #spikes
        (310, 311, GROUND_LEVEL), #spikes
        (330, 331, GROUND_LEVEL), #spikes
        (350, 351, GROUND_LEVEL), #spikes
        (370, 371, GROUND_LEVEL), #spikes
        (390, 391, GROUND_LEVEL), #spikes
        (410, 411, GROUND_LEVEL), #spikes
    ],
    "invertGravity":[ #invert grav
    ],
    "speed":[ #speed

    ],
    "end": (460, GROUND_LEVEL - 1) #end flag
}

# Level 1 layout specification.
level1 = { #level 1
    "id": 1, # id
    "ground": (-10, 500), #ground
    "platforms": [ #platforms
        (68, 76, GROUND_LEVEL - 2), #platforms
        (110, 114, GROUND_LEVEL - 2), #platforms
        (120, 124, GROUND_LEVEL - 4), #platforms

        (144, 154, GROUND_LEVEL - 2), #platforms
        (158, 171, GROUND_LEVEL - 4), #platforms
        (180, 220, GROUND_LEVEL - 6), #platforms
        (228, 270, GROUND_LEVEL - 8), #platforms
        (282, 350, GROUND_LEVEL - 6) #platforms
    ],
    "checkpoints": [ #checkpoints
        (70, GROUND_LEVEL - 1), #checkpoints
        (380, GROUND_LEVEL - 1) #checkpoints

    ],
    "spikes":[ #spikes
        (40, 42, GROUND_LEVEL), #spikes
        (50, 52, GROUND_LEVEL), #spikes
        (108, 124, GROUND_LEVEL), #spikes

        (190, 192, GROUND_LEVEL - 7), #spikes
        (238, 240, GROUND_LEVEL - 9), #spikes
        (258, 260, GROUND_LEVEL - 9), #spikes

        (298, 302, GROUND_LEVEL - 7), #spikes
        (315, 316, GROUND_LEVEL - 7), #spikes

        (140, 360, GROUND_LEVEL), #spikes

        (390, 391, GROUND_LEVEL), #spikes
        (410, 411, GROUND_LEVEL), #spikes
        (425, 430, GROUND_LEVEL), #spikes

    ],
    "invertGravity":[ #grav
    ],
    "speed":[#speed

    ],
    "end": (460, GROUND_LEVEL - 1) #end flag
}


# Level 1 layout specification.
level2 = {
    "id": 2, #id
    "ground": (-10, 600),  # Extend ground for a longer level
    "platforms": [ #platforms
        # Platforms are not used in this level
    ],
    "checkpoints": [ #checkpoints
        (170, GROUND_LEVEL - 1),  # Early checkpoint after the first speed and spike challenge
        (300, GROUND_LEVEL - 1),  # Midpoint checkpoint after a high-speed section
    ],
    "spikes": [ #spikes
        (35, 40, GROUND_LEVEL),  # Initial spike section before speed boost
        (60, 65, GROUND_LEVEL),  # A quick challenge during the first speed boost

        (100, 105, GROUND_LEVEL),  # Spikes overlapping with speed boost
        (140, 150, GROUND_LEVEL),  # Another overlapping section

        (200, 205, GROUND_LEVEL),  # A brief break, then tightly spaced spikes
        (220, 225, GROUND_LEVEL), #spikes

        (270, 275, GROUND_LEVEL),  # High-speed challenge

        (350, 354, GROUND_LEVEL),  # Longer section with alternating gaps
        (361, 365, GROUND_LEVEL),

        (430, 440, GROUND_LEVEL),  # A longer section with little margin for error

        (480, 485, GROUND_LEVEL),  # Final spike challenge before the end flag
    ],
    "invertGravity": [ #grav
        # No gravity inversion for this level
    ],
    "speed": [ #speed
        (40, 150, GROUND_LEVEL),  # Initial speed boost overlapping with spikes
        (250, 350, GROUND_LEVEL),  # A long stretch of high speed with spikes
        (400, 460, GROUND_LEVEL),  # Final high-speed section
    ],
    "end": (580, GROUND_LEVEL - 1),  # End flag positioned further out for a longer level
}



# Level 1 layout specification.
level3 = {
    "id": 3, #id
    "ground": (-10, 500), #ground
    "platforms": [ #platfomrms
        (50, 100, GROUND_LEVEL - 8), #platforms
        (70, 220, GROUND_LEVEL - 2), #platforms
        (228, 270, GROUND_LEVEL - 4), #platforms
    ],
    "checkpoints": [ # #checkpoints
        (280, GROUND_LEVEL - 1), #checkpoints
    ],
    "spikes":[ #spikes
        (20, 22, GROUND_LEVEL), #spikes

        (60, 200, GROUND_LEVEL), #spikes

        (58, 59, GROUND_LEVEL - 7),    #spikes     

        (110, 111, GROUND_LEVEL - 3),    #spikes     
        (125, 126, GROUND_LEVEL - 3),   #spikes      
        (144, 150, GROUND_LEVEL - 3), #spikes
        (170, 171, GROUND_LEVEL - 3), #spikes
        (190, 194, GROUND_LEVEL - 3), #spikes

        (240, 241, GROUND_LEVEL), #spikes
        (260, 261, GROUND_LEVEL), #spikes

        (228, 270, GROUND_LEVEL-5), #spikes

        (390, 391, GROUND_LEVEL), #spikes
        (410, 411, GROUND_LEVEL), #spikes
        
        (290, 291, GROUND_LEVEL), #spikes
        (310, 311, GROUND_LEVEL), #spikes
        (330, 331, GROUND_LEVEL), #spikes
        (350, 351, GROUND_LEVEL), #spikes
        (390, 391, GROUND_LEVEL), #spikes
        (410, 411, GROUND_LEVEL), #spikes
    ],
    "invertGravity":[ #invert grav
        (45, 46, GROUND_LEVEL), #invert grav
        (70, 71, GROUND_LEVEL-7), #invert grav
    ],
    "speed":[ #speed

    ],
    "end": (460, GROUND_LEVEL - 1) #end flag
}

levels = { # levels
    0: level0, #level 0
    1: level1, # level 1
    2: level2, #level 2
    3: level3, #level 3
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

        if specs["ground"]:
            for x in range(specs["ground"][0], specs["ground"][1]):  # For the range of x positions in the ground list.
                for i in range(-1, 3): #add four total tiles
                    if i == -1: #if top tile
                        self._environment.append(Ground(x, VERTICAL_TILES + i, self.id))                  # Create a ground tile.
                    else: #not top tile
                        self._environment.append(GroundLower(x, VERTICAL_TILES + i, self.id))                  # Create a lower ground tile.
        if specs["platforms"]: # if platforms
            for group in specs["platforms"]:                               # For each position in the platform list.
                for x in range(group[0], group[1]): #iterate
                    self._environment.append(Platform(x, group[2]))  # Create a platform.
        if specs["checkpoints"]: #if checkpoints
            for checkpoint in specs["checkpoints"]:                                     # For each position in the checkpoint list.
                self._environment.append(CheckpointFlag(checkpoint[0], checkpoint[1]))  # Create a checkpoint flag.
        if specs["spikes"]: #if spieks
            for group in specs["spikes"]:                      # For each position in the spikes list.
                for x in range(group[0], group[1]):       # for the range of x positions in the spike set.
                    self._hazards.append(Spikes(x, group[2], self.id))  # Create a set of spikes.
        if specs["invertGravity"]: #if grav
            for group in specs["invertGravity"]:                      # For each position in the gravity inverter list.
                for x in range(group[0], group[1]):       # for the range of x positions in the gravity inverter set.
                    self._environment.append(InvertGravity(x, group[2]))  # Create a set of gravity inverters.
        if specs["speed"]: #if speed
            for group in specs["speed"]:                      # For each position in the speed list.
                for x in range(group[0], group[1]):       # for the range of x positions in the speed set.
                    self._environment.append(SpeedBoost(x, group[2]))  # Create a set of speed.

        self._environment.append(EndFlag(specs["end"][0], specs["end"][1]))  # Create the end flag.

        for obj in self._environment + self._hazards:    # For each environment object.
            obj.move_x(-1 * start[0] * TILE_SIZE)                             # Offset it to the start position.

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

        # Expand the cube's rect and each object's rect by the tolerance
        expanded_cube_rect = cube._rect.inflate(TOLERANCE, TOLERANCE)

        for object in self._environment + self._hazards:  # For each object in the level.
            # Expand the object's rect by the tolerance
            # If the expanded rectangles collide (or touch)
            if expanded_cube_rect.colliderect(object._rect):
                collision_list.append(object)  # Add it to the collision list.

        return collision_list  # Return the collision list.
