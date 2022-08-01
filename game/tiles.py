import random
import pygame, csv, os
from settings import *


class Tile(pygame.sprite.Sprite):  # inherits from built in pygame Sprite class

    def __init__(self, filepath, x, y, group):
        super(Tile, self).__init__()
        group.add(self)
        self.group = group
        self.image = pygame.transform.scale(pygame.image.load(filepath, 'tile'), (TILESIZE, TILESIZE))
        self._layer = 2
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y


class Asteroid(pygame.sprite.Sprite):

    def __init__(self, filepath, mappath, x, y, terrain_group, tile_group, ship_group, rock_group):
        super(Asteroid, self).__init__()
        terrain_group.add(self)
        self.group = tile_group
        self.image = pygame.transform.scale(pygame.image.load(filepath, 'asteroid'), (TILESIZE*2, TILESIZE*2))
        self._layer = 3
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x, self.rect.y = x, y
        self.map = TileMap(mappath, tile_group,terrain_group, ship_group, rock_group, False)

    def collide(self, player):
        return collide(self, player)

class Rock(pygame.sprite.Sprite):

    def __init__(self, filepath, x, y, rock_group):
        super(Rock, self).__init__()
        rock_group.add(self)
        # TODO: Load in rock sprite once rock mining functionality works
        self.image = pygame.transform.scale(pygame.image.load("assets/crypto_rock.png"), (TILESIZE, TILESIZE))
        self._layer = 7
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x, self.rect.y = x, y

    def collide(self, player):
        return collide(self, player)

class ParkSpaceShip(pygame.sprite.Sprite):

    def __init__(self, filepath, x, y, ship_group):
        super(ParkSpaceShip, self).__init__()
        ship_group.add(self)
         # TODO: Load in space ship sprite once rock mining functionality works
        self.image = pygame.transform.scale(pygame.image.load("assets/ShipUpStill.png"), (TILESIZE * 1.5, TILESIZE * 1.5))
        self._layer = 8
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x, self.rect.y = x, y

    def collide(self, player):
        return collide(self, player)

class TileMap:

    def __init__(self, filename, tile_group, terrain_group, ship_group, rock_group, is_space_map):
        self.is_space_map = is_space_map
        self.tile_group = tile_group
        self.terrain_group = terrain_group
        self.ship_group = ship_group
        self.rock_group = rock_group
        self.tile_size = TILESIZE
        self.start_x, self.start_y = 0, 0
        # TODO: below list may prevent garbage collection of sprites
        self.tiles = self.load_tiles(filename)
        self.ships = self.generate_ship()
        self.rock = self.generate_rock()
        # print(self.tiles[0], type(self.tiles[0]), "TileMAP print at init typeof tiles[0]")
        self.map_w, self.map_h = WIN_WIDTH, WIN_HEIGHT

        # TODO: This is a bool that will determine if the map should be populated with rocks/enemies or with asteroids.
        self.terrain = self.generate_terrain()

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
        for ship in self.ships:
            self.ship_group.add(ship)
        for rock in self.rock:
            self.rock_group.add(rock)

    def unload_tiles(self):
        for tile in self.tiles:
            tile.kill()
        for terr in self.terrain:
            terr.kill()
        for ship in self.ships:
            ship.kill()
        for rock in self.rock:
            rock.kill()

    def generate_terrain(self):
        terrain = []
        if self.is_space_map:
            terrain.append(Asteroid("assets/MapTiles/zAstDebris03.png", "game/asttest1.csv", random.randrange(TILESIZE, TILESIZE * 28), random.randrange(TILESIZE, TILESIZE * 10), self.terrain_group, self.tile_group, self.ship_group, self.rock_group))
            terrain.append(
                Asteroid("assets/MapTiles/zAstDebris03.png", "game/asttest1.csv", random.randrange(TILESIZE, TILESIZE * 15),
                         random.randrange(TILESIZE * 10, TILESIZE *18 ), self.terrain_group, self.tile_group, self.ship_group, self.rock_group))
            terrain.append(
                Asteroid("assets/MapTiles/zAstDebris03.png", "game/asttest1.csv", random.randrange(TILESIZE * 16, TILESIZE * 28),
                         random.randrange(TILESIZE * 10, TILESIZE * 18), self.terrain_group, self.tile_group, self.ship_group, self.rock_group))
        return terrain
        pass


    def generate_ship(self):
        ship = []
        if not self.is_space_map:
            ship.append(ParkSpaceShip(None, WIN_WIDTH//2 - TILESIZE, 100, self.ship_group))
        return ship

    def generate_rock(self):
        rock = []
        print("rock")
        if not self.is_space_map:
            rock.append(Rock(None, random.randrange(TILESIZE * 6, TILESIZE * 9), random.randrange(TILESIZE * 5, TILESIZE * 10), self.rock_group))
            rock.append(Rock(None, random.randrange(TILESIZE * 9, TILESIZE * 12), random.randrange(TILESIZE * 5, TILESIZE * 10), self.rock_group))
            rock.append(Rock(None, random.randrange(TILESIZE * 12, TILESIZE * 15), random.randrange(TILESIZE * 5, TILESIZE * 10), self.rock_group))
            rock.append(Rock(None, random.randrange(TILESIZE * 15, TILESIZE * 18), random.randrange(TILESIZE * 5, TILESIZE * 10), self.rock_group))
            rock.append(Rock(None, random.randrange(TILESIZE * 18, TILESIZE * 21), random.randrange(TILESIZE * 5, TILESIZE * 10), self.rock_group))
            rock.append(Rock(None, random.randrange(TILESIZE * 6, TILESIZE * 9), random.randrange(TILESIZE * 11, TILESIZE * 15), self.rock_group))
            rock.append(Rock(None, random.randrange(TILESIZE * 9, TILESIZE * 12), random.randrange(TILESIZE * 11, TILESIZE * 15), self.rock_group))
            rock.append(Rock(None, random.randrange(TILESIZE * 12, TILESIZE * 15), random.randrange(TILESIZE * 11, TILESIZE * 15), self.rock_group))
            rock.append(Rock(None, random.randrange(TILESIZE * 15, TILESIZE * 18), random.randrange(TILESIZE * 11, TILESIZE * 15), self.rock_group))
            rock.append(Rock(None, random.randrange(TILESIZE * 18, TILESIZE * 21), random.randrange(TILESIZE * 11, TILESIZE * 15), self.rock_group))
        return rock

    def load_tiles(self, filename):
        """populates tile sprites to 2D grid and returns it"""
        tiles = []

        zone = self.read_csv(filename)

        x, y = 0, 0

        tile_list = [file for file in os.listdir("assets/MapTiles")]
        tile_list.sort()

        for row in zone:
            x = 0
            for tile in row:
                tiles.append(Tile("assets/MapTiles/"+tile_list[int(tile)], x * self.tile_size, y * self.tile_size, self.tile_group))
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


