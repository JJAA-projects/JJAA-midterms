import pygame
import sys
import enum

from sprites import *
from settings import *
from tiles import *

class Game:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Crypto Astroneer")
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.get_default_font()  # can be customized
        self.running = True
        self.playing = False
        self.gameover = False
        # TODO: BOOL for titlescreen. Stop all playerfunction and don't render player while this is true. Set to
        #  false when player starts the game
        self.bg = pygame.image.load("assets/title_screen.jpg")
        self.bg = pygame.transform.scale(self.bg, (960, 640))
        self.current_map = None
        self.current_space_map = None
        self.score = 0
        self.level = 1
        self.main_font = pygame.font.SysFont("Calibri", 40)

    def run(self):
        """run game"""
        self.playing = True
        self.all_sprites_group = pygame.sprite.LayeredUpdates()
        self.current_map_group = pygame.sprite.LayeredUpdates()
        self.terrain_group = pygame.sprite.LayeredUpdates()
        self.rocks_group = pygame.sprite.LayeredUpdates()
        self.ship_group = pygame.sprite.LayeredUpdates()
        self.rock_group = pygame.sprite.LayeredUpdates()
        # TODO: This is just a testmap for the first space map
        self.update_map("cleaned/TestSpaceMap01.csv", True)
        self.current_space_map = self.current_map
        self.switch_map(self.current_map)
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.player = Player(self, 1, 1, self.all_sprites_group)
        self.ship_group.empty()
        self.rock_group.empty()

    def events(self):
        """listens for events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
        # TODO: remove. Only for testing purposes
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_0]):
            self.update_map("cleaned/Testmap02.csv", False)
        if (keys[pygame.K_9]):
            self.update_map("cleaned/Testmap03.csv", True)
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
                    self.player.player_is_ship = False
                    self.player.facing = 'down'
                    self.player.rect.x = WIN_WIDTH//2 - 24
                    self.player.rect.y = TILESIZE * 5
        else:
            for ship in self.ship_group:
                if ship.collide(self.player):
                    self.reload_space_map()
                    self.player.player_is_ship = True
                    self.player.rect.x = WIN_WIDTH//2 - 24
                    self.player.rect.y = WIN_HEIGHT//2 - 24
            for idx, rock in enumerate(self.rock_group):
                if rock.collide(self.player):
                    self.score += 1
                    self.rock_group.remove(rock)
            if self.score >= 30:
                self.gameover = True
            elif self.score >= 20:
                self.level = 3
            elif self.score >= 10:
                self.level = 2


    def draw(self):
        # TODO: Change this to load the tilemap
        self.score_label = self.main_font.render(f"Score: {self.score}", True, (0, 255, 255))
        self.level_label = self.main_font.render(f"Level: {self.level}" , True, (0, 255, 255))
        self.gameover_label = self.main_font.render(f"GAME OVER", True, (255, 0, 0))
        self.current_map_group.draw(self.screen)
        self.terrain_group.draw(self.screen)
        self.all_sprites_group.draw(self.screen)
        self.ship_group.draw(self.screen)
        self.rock_group.draw(self.screen)
        self.screen.blit(self.score_label, (TILESIZE, 10))
        self.screen.blit(self.level_label, (WIN_WIDTH - TILESIZE * 5, 10))
        if self.gameover:
            self.screen.blit(self.gameover_label, (WIN_WIDTH / 2 - 102, WIN_HEIGHT / 2))
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
        self.rock_group.empty()
        self.current_map = None
        self.current_map = TileMap(filepath, self.current_map_group, self.terrain_group, self.ship_group,self.rock_group, is_space_map)
        if is_space_map:
            self.current_space_map = self.current_map


    # TODO: rename
    def reload_space_map(self):
        self.current_map_group.empty()
        self.terrain_group.empty()
        self.ship_group.empty()
        self.rock_group.empty()
        self.current_map = self.current_space_map
        self.current_map.show_tiles()
        self.player.rect.x = 0
        self.player.rect.y = 0

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

