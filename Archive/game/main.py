import os
import pygame
import sys
import random

try:
    from app import Ship, Asteroid
except:
    from game.app import Ship, Asteroid

try:
    from settings import *
except:
    from game.settings import *


pygame.init()
pygame.display.set_caption("Crypto Astroneer")
clock = pygame.time.Clock()
angle = 5

WINDOW = pygame.display.set_mode((screen_width, screen_height))
BG = pygame.image.load(os.path.join("assets", "title_screen.jpg"))
BG = pygame.transform.scale(BG, (960, 640))
player_ship = Ship(screen_width/2, screen_height/2, "Ship/ShipUpFlying.bmp")
player_miner = None
player_is_ship = True
asteroid_one = Asteroid(random.randrange(100, screen_width-100), random.randrange(100, screen_height-100), "MapTiles/zAstDebris03.png")
asteroid_two = Asteroid(random.randrange(100, screen_width-100), random.randrange(100, screen_height-100), "MapTiles/zAstDebris03.png")
asteroid_three = Asteroid(random.randrange(100, screen_width-100), random.randrange(100, screen_height-100), "MapTiles/zAstDebris03.png")
main_font = pygame.font.SysFont("Calibri", 40)
score = 0
level = 0
score_label = main_font.render(f"Score: {score}", True, (255, 255, 255))
level_label = main_font.render(f"Level: {level}", True, (255, 255, 255))


def run():
    movement_timer = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        WINDOW.blit(BG, (0, 0))
        WINDOW.blit(pygame.transform.rotate(player_ship.img, player_ship.angle), (player_ship.x, player_ship.y))
        WINDOW.blit(asteroid_one.img,(asteroid_one.x, asteroid_one.y))
        WINDOW.blit(asteroid_two.img,(asteroid_two.x, asteroid_two.y))
        WINDOW.blit(asteroid_three.img,(asteroid_three.x, asteroid_three.y))
        WINDOW.blit(score_label, (10,10))
        WINDOW.blit(level_label, (screen_width - level_label.get_width() - 10,10))

        player_ship.collision(asteroid_one)
        player_ship.collision(asteroid_two)
        player_ship.collision(asteroid_three)

        if movement_timer > 7:
            if player_is_ship:
                if key_checking(player_ship):
                    movement_timer = 0
            else:
                if key_checking(player_miner):
                    movement_timer = 0
        else:
            movement_timer += 1
        if player_is_ship:
            player_ship.update()
        else:
            pass
            # player_miner.update()
        pygame.display.update()
        clock.tick(FPS)


def key_checking(component):
    keys = pygame.key.get_pressed()
    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and component.intended_x > (0 + 16):
        component.move("left")
        component.angle = 90
        return True
    if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and component.intended_x < (screen_width - 16):
        component.move("right")
        component.angle = 270
        return True
    if (keys[pygame.K_UP] or keys[pygame.K_w]) and component.intended_y > (0 + 16):
        component.move("up")
        component.angle = 0
        return True
    if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and component.intended_y < (screen_height - 16):
        component.move("down")
        component.angle = 180
        return True
    if keys[pygame.K_SPACE]:
        player_ship.img = pygame.image.load(
            os.path.join("assets", "player_front.png"))

if __name__ == "__main__":
    run()
