import os
from re import T
import pygame
import sys
import enum
import time
import random

try:
    from sprites import Player
    from settings import WIN_WIDTH, WIN_HEIGHT, TILESIZE, FPS, ACTION_TIMER, ASTEROID_COUNT, ROCK_SPAWN_PERCENT, PLAYER_LAYER, GROUND_LAYER
    from tiles import TileMap, Tile, Asteroid
except:
    from game.sprites import Player
    from game.settings import WIN_WIDTH, WIN_HEIGHT, TILESIZE, FPS, ACTION_TIMER, ASTEROID_COUNT, ROCK_SPAWN_PERCENT, PLAYER_LAYER, GROUND_LAYER
    from game.tiles import TileMap, Tile, Asteroid




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
        self.player = None
        self.current_map = None
        self.current_space_map = None
        self.score = 0
        self.level = 1
        self.health = 10
        self.clock = pygame.time.Clock()
        self.minutes = 2
        self.seconds = 60
        self.milliseconds = 0
        self.main_font = pygame.font.SysFont("comicsans", 40, True, True)
        self.game_font = pygame.font.Font("assets/Font/Monoton-Regular.ttf", 60)
        self.game_font_2 = pygame.font.Font("assets/Font/heavy_data.ttf", 50)
        self.current_frames = 0
        self.current_time = time.time()*1000
        self.start = False
        self.all_spacemaps = os.listdir("assets/MapsSpace")
        self.all_spacemaps.sort()
        if self.all_spacemaps[0] == ".DS_Store":
            self.all_spacemaps.pop(0)
        self.all_asteroidmaps = os.listdir("assets/MapsAsteroid")
        self.all_asteroidmaps.sort()
        if self.all_asteroidmaps[0] == ".DS_Store":
            self.all_asteroidmaps.pop(0)

    def run(self):
        """run game"""
        self.playing = True
        self.all_sprites_group = pygame.sprite.LayeredUpdates()
        self.current_map_group = pygame.sprite.LayeredUpdates()
        self.terrain_group = pygame.sprite.LayeredUpdates()
        self.rocks_group = pygame.sprite.LayeredUpdates()
        self.ship_group = pygame.sprite.LayeredUpdates()
        self.rock_group = pygame.sprite.LayeredUpdates()
        self.worm_group = pygame.sprite.LayeredUpdates()
        # TODO: This is just a testmap for the first space map
        self.update_map("assets/MapsSpace/" + self.all_spacemaps[random.randint(0, len(self.all_spacemaps) - 1)], True)
        self.current_space_map = self.current_map
        self.switch_map(self.current_map)
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.player = Player(self, 1, 1, self.all_sprites_group, self.current_map.collision_map)
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
            self.update_map("game/Testmap02.csv", False)
        if (keys[pygame.K_9]):
            self.update_map("game/Testmap03.csv", True)
        if (keys[pygame.K_8]):
            self.reload_space_map()
        if keys[pygame.K_SPACE]:
            self.start = True


    def update(self):
        self.make_labels()
        self.make_sound()
        self.all_sprites_group.update()
        self.current_map_group.update()
        self.terrain_group.update()
        self.worm_group.update()
        if self.gameover:
            self.player.is_game_over = True
        if self.health <= 0:
            self.gameover = True
        if not self.start:
            self.game_intro_sound.play()
        if self.player.player_is_ship:
            self.health = 10
            wormhole_ready = True
            for terrain in self.terrain_group:
                if len(terrain.map.rocks) > 2:
                    wormhole_ready = False
                if terrain.collide(self.player):
                    if self.player.facing == 'right':
                        self.player.last_pos_x = self.player.rect.x - TILESIZE
                        self.player.last_pos_y = self.player.rect.y
                    if self.player.facing == 'left':
                        self.player.last_pos_x = self.player.rect.x + TILESIZE
                        self.player.last_pos_y = self.player.rect.y
                    if self.player.facing == 'up':
                        self.player.last_pos_y = self.player.rect.y + TILESIZE
                        self.player.last_pos_x = self.player.rect.x
                    if self.player.facing == 'down':
                        self.player.last_pos_y = self.player.rect.y - TILESIZE
                        self.player.last_pos_x = self.player.rect.x
                    self.asteroid_sound.play()
                    self.switch_map(terrain.map)
                    self.player.player_is_ship = False
                    self.player.facing = 'down'
                    self.player.rect.x = WIN_WIDTH//2 - TILESIZE
                    self.player.rect.y = TILESIZE * 5
            if wormhole_ready and not self.current_map.wormhole:
                self.current_map.generate_wormhole(self.worm_group)
            if self.current_map.wormhole:
                if self.current_map.wormhole.collide(self.player):
                    new_map = random.randint(0, len(self.all_spacemaps) - 1)
                    self.update_map("assets/MapsSpace/"+self.all_spacemaps[new_map], True)
                    self.worm_group.empty()
                    self.reload_space_map()
                    self.level += 1
        else:
            for ship in self.ship_group:
                if ship.collide(self.player):
                    self.asteroid_sound.play()
                    self.reload_space_map()
                    self.player.player_is_ship = True
                    self.player.rect.x = self.player.last_pos_x
                    self.player.rect.y = self.player.last_pos_y

            for idx, rock in enumerate(self.rock_group):
                if rock.collide(self.player):
                    self.score_sound.play()
                    self.score += self.level
                    self.rock_group.remove(rock)
                    self.current_map.rocks.remove(rock)
            # # if self.score >= 30:
            # #     self.gameover = True
            # #     self.player._layer = 1
            # elif self.score >= 20:
            #     self.level = 3
            #     self.health = 6
            # elif self.score >= 10:
            #     self.level = 2
            #     self.health = 8


    def draw(self):
        # TODO: Change this to load the tilemap
        self.current_map_group.draw(self.screen)
        self.screen.blit(self.score_label, (TILESIZE, 10))
        self.screen.blit(self.level_label, (WIN_WIDTH - TILESIZE * 6, 10))
        if self.start:
            self.game_intro_sound = None
            self.terrain_group.draw(self.screen)
            self.all_sprites_group.draw(self.screen)
            self.rock_group.draw(self.screen)
            self.ship_group.draw(self.screen)
            if self.player.player_is_ship:
                self.worm_group.draw(self.screen)
            if self.gameover:
                self.screen.blit(self.gameover_label, (WIN_WIDTH // 2 - 136, WIN_HEIGHT / 2 - TILESIZE * 2))
            self.countdown()
            pygame.draw.rect(self.screen, (200,0,0), (WIN_WIDTH // 2 - TILESIZE * 3, 24, TILESIZE * 6, 24))
            pygame.draw.rect(self.screen, (0,200,0), (WIN_WIDTH //2 - TILESIZE * 3, 24, ((TILESIZE * 6) - (((TILESIZE * 6)/10) * (10 - self.health))), 24))
        else:
            self.screen.blit(self.game_title, (WIN_WIDTH //2 - TILESIZE * 9, WIN_HEIGHT //2 - TILESIZE * 3))
            self.screen.blit(self.start_intro, (WIN_WIDTH //2 - TILESIZE * 12, WIN_HEIGHT - TILESIZE * 3))
        self.clock.tick(FPS)
        self.current_frames += 1
        pygame.display.update()
        

    def switch_map(self, map):
        self.current_map.unload_tiles()
        self.current_map = map
        self.current_map.show_tiles()
        if self.player:
            self.player.collision_map = self.current_map.collision_map

    def make_labels(self):
        self.score_label = self.main_font.render(f"Score: {self.score}", True, (0, 255, 255))
        self.level_label = self.main_font.render(f"Level: {self.level}" , True, (0, 255, 255))
        self.game_title = self.game_font.render(f"SPACE \t PIONEERS" , True, (140, 255, 140))
        self.start_intro = self.game_font_2.render(f"Press the space key play the game" , True, (255, 255, 255))
        self.gameover_label = self.main_font.render(f"GAME OVER", True, (255, 0, 0))

    def make_sound(self):
        self.game_intro_sound = pygame.mixer.Sound("assets/Sound/8Bit Retro Logo.wav")
        self.game_intro_sound.set_volume(0.01)
        self.score_sound = pygame.mixer.Sound("assets/Sound/score.wav")
        self.score_sound.set_volume(0.1)
        self.asteroid_sound = pygame.mixer.Sound("assets/Sound/asteroid.wav")
        self.asteroid_sound.set_volume(0.1)
        self.level_sound = pygame.mixer.Sound("assets/Sound/level.wav")
        self.level_sound.set_volume(0.1)
        self.level_sound = pygame.mixer.Sound("assets/Sound/level.wav")
        self.level_sound.set_volume(0.1)
        self.gameover_sound = pygame.mixer.Sound("assets/Sound/gameover.wav")
        self.gameover_sound.set_volume(0.1)

    def update_map(self, filepath, is_space_map):
        self.current_map_group.empty()
        self.terrain_group.empty()
        self.ship_group.empty()
        self.rock_group.empty()
        self.current_map = None
        self.current_map = TileMap(filepath, self.current_map_group, self.terrain_group, self.ship_group,self.rock_group, self.all_asteroidmaps, is_space_map)
        if is_space_map:
            self.current_space_map = self.current_map
        if self.player:
            self.player.collision_map = self.current_map.collision_map

    def countdown(self):

        if self.minutes >= 0 and self.seconds >= 0:
            if self.milliseconds > 1000:
                self.milliseconds = self.milliseconds % 1000
                self.seconds -= 1
                self.current_frames = 0
                if not self.player.player_is_ship:
                    self.health -= 1
            if self.seconds < 0:
                self.seconds += 60
                self.minutes -= 1
        if int(self.minutes) == -1:
            self.minutes = 0
            self.seconds = 0
            self.gameover = True
        if self.seconds > 9:
            time_left = "0{}:{}".format(self.minutes, int(self.seconds))
        else:
            time_left = "0{}:0{}".format(self.minutes, int(self.seconds))
        self.time_label=self.main_font.render(time_left, True, (255, 255, 255))
        self.milliseconds += time.time()*1000 - self.current_time
        self.current_time = time.time() * 1000
        self.screen.blit(self.time_label, (WIN_WIDTH//2 - TILESIZE * 1.5, WIN_HEIGHT - TILESIZE * 2))

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
        if self.player:
            self.player.collision_map = self.current_map.collision_map

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

