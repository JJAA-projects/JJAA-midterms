import random
import pygame, csv, os
from settings import *


class Tile(pygame.sprite.Sprite):  # inherits from built in pygame Sprite class

    def __init__(self, filepath, x, y, group):
        # pygame.sprite.Sprite.__init__(self)
        super(Tile, self).__init__()
        group.add(self)
        self.group = group
        self.image = pygame.transform.scale(pygame.image.load(filepath, 'tile'), (TILESIZE, TILESIZE))
        self._layer = 2
        self.rect = self.image.get_rect()
        # print(filepath, x, y)
        self.rect.x, self.rect.y = x, y

    # def draw(self, surface):
    #     surface.blit(self.image, (self.rect.x, self.rect.y))


class Asteroid(pygame.sprite.Sprite):

    def __init__(self, filepath, mappath, x, y, terrain_group, tile_group):
        super(Asteroid, self).__init__()
        terrain_group.add(self)
        self.group = tile_group
        self.image = pygame.transform.scale(pygame.image.load(filepath, 'asteroid'), (TILESIZE*2, TILESIZE*2))
        self._layer = 3
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x, self.rect.y = x, y
        self.map = TileMap(mappath, tile_group, terrain_group, False)

    def collide(self, player):
        return collide(self, player)


class TileMap:

    def __init__(self, filename, tile_group, terrain_group, is_space_map):
        self.tile_group = tile_group
        self.terrain_group = terrain_group
        self.tile_size = TILESIZE
        self.start_x, self.start_y = 0, 0
        # TODO: below list may prevent garbage collection of sprites
        self.tiles = self.load_tiles(filename)
        # print(self.tiles[0], type(self.tiles[0]), "TileMAP print at init typeof tiles[0]")
        self.map_w, self.map_h = WIN_WIDTH, WIN_HEIGHT

        # TODO: This is a bool that will determine if the map should be populated with rocks/enemies or with asteroids.
        self.is_space_map = is_space_map
        self.terrain = self.generate_terrain()
        # self.map_surface = pygame.Surface((self.map_w, self.map_h))
        # self.map_surface.set_colorkey((0, 0, 0))
        # self.load_map()

    # def draw_map(self, surface):
    #     surface.blit(self.map_surface, (30, 30))

    # def load_map(self):
    #     for tile in self.tiles:
    #         tile.draw(self.map_surface)

    def read_csv(self, filename):
        """opens and reads csv file, appends rows of integers to list, returns the list"""
        zone = []

        with open(os.path.join(filename)) as data:
            data = csv.reader(data, delimiter=',')
            for row in data:
                zone.append(list(row))

            return zone

    def show_tiles(self):
        for tile in self.tiles:
            self.tile_group.add(tile)
        for terr in self.terrain:
            self.terrain_group.add(terr)

    def unload_tiles(self):
        for tile in self.tiles:
            tile.kill()
        for terr in self.terrain:
            terr.kill()

    def generate_terrain(self):
        terrain = []
        if self.is_space_map:
            terrain.append(Asteroid("assets/MapTiles/zAstDebris03.png", "sandbox/cleaned/asttest1.csv", random.randint(3, 15) * self.tile_size,
                                    random.randint(3, 15) * self.tile_size, self.terrain_group, self.tile_group))
            terrain.append(
                Asteroid("assets/MapTiles/zAstDebris03.png", "sandbox/cleaned/asttest2.csv", random.randint(3, 15) * self.tile_size,
                         random.randint(3, 15) * self.tile_size, self.terrain_group, self.tile_group))
            terrain.append(
                Asteroid("assets/MapTiles/zAstDebris03.png", "sandbox/cleaned/asttest3.csv", random.randint(3, 15) * self.tile_size,
                         random.randint(3, 15) * self.tile_size, self.terrain_group, self.tile_group))
            # for i in range(ASTEROID_COUNT):
            #     terrain.append(Asteroid("assets/MapTiles/zAstDebris03.png", ADDMAPPATH, random.randint(3,15)*self.tile_size, random.randint(3,15)*self.tile_size, self.terrain_group, self.tile_group))
        return terrain
        pass

    def load_tiles(self, filename):
        """populates tile spites to 2D grid and returns it"""
        tiles = []

        zone = self.read_csv(filename)

        x, y = 0, 0

        tile_list = [file for file in os.listdir("assets/MapTiles")]
        tile_list.sort()

        for row in zone:
            x = 0
            for tile in row:
                #print(tile)
                #print(tile_list[int(tile)])
                tiles.append(Tile("assets/MapTiles/"+tile_list[int(tile)], x * self.tile_size, y * self.tile_size, self.tile_group))
                # print(type(tiles[0]))
                x += 1
            y += 1

        self.map_w, self.map_h = x * self.tile_size, y * self.tile_size
        return tiles


def collide(obj1, obj2):
    offset_x = obj2.rect.x - obj1.rect.x
    offset_y = obj2.rect.y - obj1.rect.y
    if obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None:
        print("collided")
        return True


