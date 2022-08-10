import random

import csv
import os
import pygame

try:
    from settings import *
except e:
    from game.settings import *


class Tile(pygame.sprite.Sprite):  

    def __init__(self, filepath, x, y, group) -> None:
        super(Tile, self).__init__()
        group.add(self)
        self.group = group
        self.image = pygame.transform.scale(pygame.image.load(filepath, 'tile'), (TILESIZE, TILESIZE))
        self._layer: int = 2
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y


class Asteroid(pygame.sprite.Sprite):

    def __init__(self, filepath, mappath, x, y, terrain_group, tile_group, ship_group, rock_group, all_asteroidmaps) \
            -> None:
        super(Asteroid, self).__init__()
        terrain_group.add(self)
        self.group = tile_group
        self.image = pygame.transform.scale(pygame.image.load(filepath, 'asteroid'), (TILESIZE*2, TILESIZE*2))
        self._layer: int = 3
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x, self.rect.y = x, y
        self.map = TileMap(mappath, tile_group,terrain_group, ship_group, rock_group, all_asteroidmaps, False)

    def collide(self, player):
        return collide(self, player)


class Rock(pygame.sprite.Sprite):

    def __init__(self, x, y, rock_group) -> None:
        super(Rock, self).__init__()
        rock_group.add(self)
        self.image = pygame.transform.scale(pygame.image.load("assets/crypto_rock.png"), (TILESIZE, TILESIZE))
        self._layer: int = 3
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def collide(self, player):
        return self.rect.x == player.rect.x and self.rect.y == player.rect.y


class Wormhole(pygame.sprite.Sprite):

    def __init__(self, filepath, x, y, worm_group) -> None:
        super(Wormhole, self).__init__()
        worm_group.add(self)
        self.filepath = filepath
        self.group = worm_group
        self.image = pygame.transform.scale(pygame.image.load(self.filepath, 'wormhole'), (TILESIZE*4, TILESIZE*4))
        self._layer: int = 4
        self.rect = self.image.get_rect()
        self.rect.height, self.rect.width = self.rect.height * 2, self.rect.width * 2
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x, self.rect.y = x, y
        self.x, self.y = x,y
        self.rotation: int = 0
        self.testx, self.testy = self.rect.x, self.rect.y
        self.counter: int = 0

    def spin(self) -> None:
        self.counter += 1
        self.image = pygame.transform.rotate(self.image, 1)
        self.rect.x -= 2
        self.rect.y -= 2
        if self.counter >= 35:
            self.rect.x, self.rect.y = self.x, self.y
            self.rotation += self.counter
            self.rotation = self.rotation % 360
            self.counter = 0
            self.image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(self.filepath, 'wormhole'), \
                (TILESIZE * 4, TILESIZE * 4)), self.rotation)

    def collide(self, player):
        return collide(self, player)


class ParkSpaceShip(pygame.sprite.Sprite):

    def __init__(self, filepath, x, y, ship_group) -> None:
        super(ParkSpaceShip, self).__init__()
        ship_group.add(self)
        self.image = pygame.transform.scale(pygame.image.load("assets/ShipUpStill.png"), \
            (TILESIZE * 1.5, TILESIZE * 1.5))
        self._layer: int = 8
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x, self.rect.y = x, y

    def collide(self, player):
        return collide(self, player)


class TileMap:

    def __init__(self, filename, tile_group, terrain_group, ship_group, rock_group, all_asteroidmaps, is_space_map) \
            -> None:
        self.is_space_map = is_space_map
        self.tile_group = tile_group
        self.terrain_group = terrain_group
        self.ship_group = ship_group
        self.rock_group = rock_group
        self.tile_size = TILESIZE
        self.start_x, self.start_y = 0, 0
        self.collision_map = [[0 for x in range(30)] for y in range(20)]
        self.tiles = self.load_tiles(filename)
        self.ships = self.generate_ship()
        self.rocks = self.generate_rock()
        self.map_w, self.map_h = WIN_WIDTH, WIN_HEIGHT
        self.wormhole = None
        self.all_asteroidmaps = all_asteroidmaps

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
        for rock in self.rocks:
            self.rock_group.add(rock)

    def unload_tiles(self):
        for tile in self.tiles:
            tile.kill()
        for terr in self.terrain:
            terr.kill()
        for ship in self.ships:
            ship.kill()
        for rock in self.rocks:
            rock.kill()

    def generate_terrain(self):
        terrain = []
        if self.is_space_map:
            terrain.append(
                Asteroid("assets/MapTiles/31zAstDebris03.png", "assets/MapsAsteroid/"
                +self.all_asteroidmaps[random.randint(0,len(self.all_asteroidmaps)-1)],
                random.randrange(TILESIZE, TILESIZE * 28), random.randrange(TILESIZE, TILESIZE * 10),
                self.terrain_group, self.tile_group, self.ship_group, self.rock_group, self.all_asteroidmaps)
            )
            terrain.append(Asteroid(
                "assets/MapTiles/31zAstDebris03.png", "assets/MapsAsteroid/"
                +self.all_asteroidmaps[random.randint(0,len(self.all_asteroidmaps)-1)],
                random.randrange(TILESIZE, TILESIZE * 15), random.randrange(TILESIZE * 10, TILESIZE *18 ),
                self.terrain_group, self.tile_group, self.ship_group, self.rock_group, self.all_asteroidmaps)
            )
            terrain.append(
                Asteroid("assets/MapTiles/31zAstDebris03.png", "assets/MapsAsteroid/"
                +self.all_asteroidmaps[random.randint(0,len(self.all_asteroidmaps)-1)],
                random.randrange(TILESIZE * 16, TILESIZE * 28),random.randrange(TILESIZE * 10, TILESIZE * 18),
                self.terrain_group, self.tile_group, self.ship_group, self.rock_group, self.all_asteroidmaps)
            )
        return terrain

    def generate_ship(self):
        ship = []
        if not self.is_space_map:
            ship.append(ParkSpaceShip(None, WIN_WIDTH//2 - TILESIZE, 100, self.ship_group))
        return ship

    def generate_rock(self):
        rocks = []
        if not self.is_space_map:
            for rowidx, row in enumerate(self.collision_map):
                for columnidx, tile in enumerate(row):
                    if tile == 0:
                        if random.randint(1, 100) <= ROCK_SPAWN_PERCENT:
                            rocks.append(Rock(columnidx*TILESIZE, rowidx*TILESIZE, self.rock_group))
        return rocks

    def load_tiles(self, filename):
        """populates tile sprites to 2D grid and returns it"""
        tiles = []
        zone = self.read_csv(filename)
        x, y = 0, 0

        tile_list = [file for file in os.listdir("assets/MapTiles")]
        tile_list.sort()
        if tile_list[0] == ".DS_Store":
            tile_list.pop(0)

        if not self.is_space_map:
            self.collision_map = []
        for row in zone:
            collision_row = []
            x = 0
            for tile in row:
                tiles.append(Tile("assets/MapTiles/"+tile_list[int(tile)], x * self.tile_size, y * self.tile_size,
                    self.tile_group))
                x += 1
                if not self.is_space_map:
                    if (int(tile) < 3) or (7 < int(tile) < 17):
                        collision_row.append(0)
                    else:
                        collision_row.append(1)
            y += 1
            if not self.is_space_map:
                self.collision_map.append(collision_row)
        if self.is_space_map:
            pass
        self.map_w, self.map_h = x * self.tile_size, y * self.tile_size
        return tiles

    def generate_wormhole(self, worm_group) -> None:
        new_wormhole = Wormhole("assets/Wormhole.png", TILESIZE, (WIN_HEIGHT/2)-(TILESIZE*2), worm_group)
        worm_group.add(new_wormhole)
        self.wormhole = new_wormhole


def collide(obj1, obj2):
    offset_x = obj2.rect.x - obj1.rect.x
    offset_y = obj2.rect.y - obj1.rect.y
    if obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None:
        return True


