
import pygame, csv, os
from settings import *


class Tile(pygame.sprite.Sprite):  # inherits from built in pygame Sprite class

    def __init__(self, filepath, x, y, group):
        pygame.sprite.Sprite.__init__(self, group)
        self.image = pygame.transform.scale(pygame.image.load(filepath, 'tile'), (TILESIZE, TILESIZE))
        self._layer = 1
        self.rect = self.image.get_rect()
        #print(filepath, x, y)
        self.rect.x, self.rect.y = x, y

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))


class TileMap:

    def __init__(self, filename, group):
        self.group = group
        self.tile_size = TILESIZE
        self.start_x, self.start_y = 0, 0
        self.tiles = self.load_tiles(filename)
        self.map_w, self.map_h = WIN_WIDTH, WIN_HEIGHT
        self.map_surface = pygame.Surface((self.map_w, self.map_h))
        # self.map_surface.set_colorkey((0, 0, 0))
        self.load_map()

    def draw_map(self, surface):
        surface.blit(self.map_surface, (30, 30))

    def load_map(self):
        for tile in self.tiles:
            tile.draw(self.map_surface)

    def read_csv(self, filename):
        """opens and reads csv file, appends rows of integers to list, returns the list"""
        zone = []

        with open(os.path.join(filename)) as data:
            data = csv.reader(data, delimiter=',')
            for row in data:
                zone.append(list(row))

            return zone

    def load_tiles(self, filename):
        """populates tile spites to 2D grid and returns it"""
        tiles = []

        zone = self.read_csv(filename)

        x, y = 0, 0

        tile_list = [file for file in os.listdir("assets/MapTiles")]
        tile_list.sort()
        print(tile_list)

        for row in zone:
            x = 0
            for tile in row:
                #print(tile)
                #print(tile_list[int(tile)])
                tiles.append(Tile("assets/MapTiles/"+tile_list[int(tile)], x * self.tile_size, y * self.tile_size, self.group))
                x += 1
            y += 1

        self.map_w, self.map_h = x * self.tile_size, y * self.tile_size
        return tiles


