import math

MAP_DIM_COLS = 395
MAP_DIM_ROWS = 500


class Pixel:
    LATITUDE = 7.55
    LONGITUDE = 10.29

    def __init__(self, coordinates, elevation, ttype):
        self.coordinates = coordinates
        self.elevation = elevation
        self.ttype = ttype

    def __str__(self):
        return f"px: [ coords: {self.coordinates} ]"

    def __repr__(self):
        return f"px: [ coords: {self.coordinates} ]"

    def __eq__(self, other):
        return self.coordinates == other.coordinates

    def __hash__(self):
        return int(self.coordinates[0] + self.coordinates[1] + self.elevation)

    def __lt__(self, other):
        return self.coordinates > other.coordinates

    def get_pixel_heuristic(self, target_pixel):
        # return how far to the target pixel depending on the type of terrain(S) between
        # this pixel and the target pixel

        # for now, we're just calculating the euclidian distance
        x_diff_sq = ((self.coordinates[1] - target_pixel.coordinates[1]) * self.LONGITUDE) ** 2
        y_diff_sq = ((self.coordinates[0] - target_pixel.coordinates[0]) * self.LATITUDE) ** 2
        z_diff_sq = (self.elevation - target_pixel.elevation) ** 2
        dist = math.sqrt(x_diff_sq + y_diff_sq + z_diff_sq) + self.ttype.penalty

        return dist

    def get_pixel_neighbors(self, terrain):
        nb = []

        # top
        top = (self.coordinates[0] - 1, self.coordinates[1])
        if top[0] >= 0 and not terrain[top[0]][top[1]].ttype.impassible:
            nb.append(terrain[top[0]][top[1]])

        # bottom
        bottom = (self.coordinates[0] + 1, self.coordinates[1])
        if bottom[0] < MAP_DIM_ROWS and not terrain[bottom[0]][bottom[1]].ttype.impassible:
            nb.append(terrain[bottom[0]][bottom[1]])

        # left
        left = (self.coordinates[0], self.coordinates[1] - 1)
        if left[1] >= 0 and not terrain[left[0]][left[1]].ttype.impassible:
            nb.append(terrain[left[0]][left[1]])

        # right
        right = (self.coordinates[0], self.coordinates[1] + 1)
        if right[1] < MAP_DIM_COLS and not terrain[right[0]][right[1]].ttype.impassible:
            nb.append(terrain[right[0]][right[1]])

        return nb


def load_terrains():
    # the 3rd arg is the penalty applied if travelling in this terrain
    return [TerrainType("OPEN_LAND", (248, 148, 18, 255), 1, False),
            TerrainType("ROUGH_MEADOW", (255, 192, 0, 255), 1, False),
            TerrainType("EASY_MOVEMENT_FOREST", (255, 255, 255, 255), 1, False),
            TerrainType("SLOW_RUN_FOREST", (2, 208, 60, 255), 1, False),
            TerrainType("WALK_FOREST", (2, 136, 40, 255), 1, False),
            TerrainType("IMPASSIBLE_VEGETATION", (5, 73, 24, 255), 100000, True),
            TerrainType("LAKE_SWAMP_MARSH", (0, 0, 255, 255), 100000, False),
            TerrainType("PAVED_ROAD", (71, 51, 3, 255), 1, False),
            TerrainType("FOOT_PATH", (0, 0, 0, 255), 1, False),
            TerrainType("OUT_OF_BOUNDS", (205, 0, 101, 255), 1, True),
            ]


def get_terrain_from_color(rgb):
    for ter in load_terrains():
        if ter.rgb == rgb or (len(rgb) == 3 and rgb == ter.rgb[0:3]):
            return ter
    return None


class TerrainType:
    def __init__(self, name, rgb, penalty, impassible):
        self.name = name
        self.rgb = rgb
        self.penalty = penalty
        self.impassible = impassible
