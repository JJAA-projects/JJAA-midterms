import pygame
import sys

from sprites import *
from settings import *
from tiles import *

try:
    from app import Ship, Asteroid
except:
    from game.app import Ship, Asteroid

try:
    from settings import *
except:
    from game.settings import *

class Game:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Crypto Astroneer")
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.get_default_font()  # can be customized
        self.running = True
        self.playing = False
        # TODO: BOOL for titlescreen. Stop all playerfunction and don't render player while this is true. Set to
        #  false when player starts the game
        self.bg = pygame.image.load("assets/title_screen.jpg")
        self.bg = pygame.transform.scale(self.bg, (960, 640))
        self.current_map = None
        self.current_space_map = None
        self.score = 0
        self.main_font = pygame.font.SysFont("Calibri", 40)
        self.score_label = self.main_font.render(f"Score: {self.score}", True, (255, 255, 255))
        # self.asteroid_one = Asteroid(random.randrange(100, WIN_WIDTH-100), random.randrange(100, WIN_HEIGHT-100), "MapTiles/zAstDebris03.png")
        # self.asteroid_two = Asteroid(random.randrange(100, WIN_WIDTH-100), random.randrange(100, WIN_HEIGHT-100), "MapTiles/zAstDebris03.png")
        # self.asteroid_three = Asteroid(random.randrange(100, WIN_WIDTH-100), random.randrange(100, WIN_HEIGHT-100), "MapTiles/zAstDebris03.png")


    def run(self):
        """run game"""
        self.playing = True
        self.all_sprites_group = pygame.sprite.LayeredUpdates()
        self.current_map_group = pygame.sprite.LayeredUpdates()
        self.terrain_group = pygame.sprite.LayeredUpdates()
        # TODO: This is just a testmap for the first space map
        self.update_map("sandbox/cleaned/TestSpaceMap01.csv", True)
        self.current_space_map = self.current_map
        self.switch_map(self.current_map)
        # you have some tilemap object named NewMap.
        # To render:
        # NewMap.show_tiles()
        # self.current_map = NewMap
        # To unrender:
        # self.current_map_group.empty()
        # NewMap.group.empty()
        # Typical situation: some other map is loaded, and you want to load your NewMap object:
        # self.current_map_group.empty()
        # NewMap.show_tiles()


        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()

        self.player = Player(self, 1, 1, self.all_sprites_group)

    def events(self):
        """listens for events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
        # TODO: remove. Only for testing purposes
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_0]):
            self.update_map("sandbox/cleaned/Testmap02.csv", False)
        if (keys[pygame.K_9]):
            self.update_map("sandbox/cleaned/Testmap03.csv", True)
        if (keys[pygame.K_8]):
            self.reload_space_map()


    def update(self):
        self.all_sprites_group.update()
        self.current_map_group.update()
        self.terrain_group.update()
        if self.player.player_is_ship:
            for terrain in self.terrain_group:
                if terrain.collide(self.player):
                    self.switch_map(terrain.map)


    def draw(self):
        # TODO: Change this to load the tilemap
        # self.screen.fill((0, 0, 0))
        # self.screen.blit(self.bg, (0, 0))
        # self.tile_map.draw_map(self.screen)
        # self.screen.blit(self.tile_map.map_surface, (0, 0))
        self.current_map_group.draw(self.screen)
        # self.screen.blit(self.asteroid_one.img, (self.asteroid_one.x, self.asteroid_one.y))
        # self.screen.blit(self.asteroid_two.img, (self.asteroid_two.x, self.asteroid_two.y))
        # self.screen.blit(self.asteroid_three.img, (self.asteroid_three.x, self.asteroid_three.y))
        self.terrain_group.draw(self.screen)
        self.all_sprites_group.draw(self.screen)
        self.screen.blit(self.score_label, (10, 10))
        self.clock.tick(FPS)
        pygame.display.update()

    def switch_map(self, map):
        self.current_map.unload_tiles()
        self.current_map = map
        self.current_map.show_tiles()


    def update_map(self, filepath, is_space_map):
        self.current_map_group.empty()
        self.terrain_group.empty()
        self.current_map = None
        self.current_map = TileMap(filepath, self.current_map_group, self.terrain_group, is_space_map)
        if is_space_map:
            self.current_space_map = self.current_map

    # TODO: rename
    def reload_space_map(self):
        # self.current_map.unload_tiles()
        self.current_map_group.empty()
        self.terrain_group.empty()
        self.current_map = self.current_space_map
        self.current_map.show_tiles()
        self.player.rect.x = 96
        self.player.rect.y = 96
        # self.current_map.reload_tiles()

    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()
        self.running = False


if __name__ == '__main__':
    game = Game()
    game.run()
    while game.running:
        game.main()

    pygame.quit()

