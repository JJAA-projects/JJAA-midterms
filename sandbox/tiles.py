
import pygame, csv, os


class Tile(pygame.sprite.Sprite):  # inherits from built in pygame Sprite class

    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))


class TileMap:

    def __init__(self, filename):
        self.tile_size = 16
        self.start_x, self.start_y = 0, 0
        self.tiles = self.load_tiles(filename)
        self.map_surface = pygame.Surface((self.map_w, self.map_h))
        self.map_surface.set_colorkey((0, 0, 0))
        self.load_map()
        self.map_w, self.map_h = 0, 0

    def draw_map(self, surface):
        surface.blit(self.map_surface, (0, 0))

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

        for row in zone:
            x = 0
            for tile in row:
                if tile == '0':
                    self.start_x, self.start_y = x * self.tile_size, y * self.tile_size
                elif tile == '1':
                    tiles.append(Tile('MapAsteroidTopLeft.png', x * self.tile_size, y * self.tile_size))

                x += 1
            y += 1

        self.map_w, self.map_h = x * self.tile_size, y * self.tile_size
        return tiles


