import pygame
import sys

from sprites import *
from settings import *
from tiles import *

try:
    from app import *
except:
    from game.app import *

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

    def run(self):
        """run game"""
        self.playing = True
        self.all_sprites_group = pygame.sprite.LayeredUpdates()
        self.current_map_group = pygame.sprite.LayeredUpdates()
        self.terrain_group = pygame.sprite.LayeredUpdates()
        self.rocks_group = pygame.sprite.LayeredUpdates()
        self.ship_group = pygame.sprite.LayeredUpdates()
        # TODO: This is just a testmap for the first space map
        self.update_map("sandbox/cleaned/TestSpaceMap01.csv", True)
        self.current_space_map = self.current_map
        self.switch_map(self.current_map)
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.player = Player(self, 1, 1, self.all_sprites_group)
        self.ship_group.empty()

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
        else:
            for ship in self.ship_group:
                if ship.collide(self.player):
                    self.reload_space_map()



    def draw(self):
        # TODO: Change this to load the tilemap
        self.current_map_group.draw(self.screen)
        self.terrain_group.draw(self.screen)
        self.all_sprites_group.draw(self.screen)
        self.ship_group.draw(self.screen)
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
        self.ship_group.empty()
        self.current_map = None
        self.current_map = TileMap(filepath, self.current_map_group, self.terrain_group, self.ship_group, is_space_map)
        if is_space_map:
            self.current_space_map = self.current_map

    # TODO: rename
    def reload_space_map(self):
        # self.current_map.unload_tiles()
        self.current_map_group.empty()
        self.terrain_group.empty()
        self.ship_group.empty()
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

