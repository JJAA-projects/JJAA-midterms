import os
import pygame
import sys

try:
    from game.app import Ship
except:
    from app import ship

try:
    from settings import *
except:
    from game.settings import *

pygame.init()
pygame.display.set_caption("Crypto Astroneer")
clock = pygame.time.Clock()

WINDOW = pygame.display.set_mode((screen_width, screen_height))
BG = pygame.image.load(os.path.join("assets", "title_screen.jpg"))
BG = pygame.transform.scale(BG, (960, 640))
player_ship = Ship(screen_width/2, screen_height/2, "temp_ship.png")
player_miner = None
player_is_ship = True


def run():
    movement_timer = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        WINDOW.blit(BG, (0, 0))
        WINDOW.blit(player_ship.img, (player_ship.x, player_ship.y))
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
        return True
    if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and component.intended_x < (screen_width - 16):
        component.move("right")
        return True
    if (keys[pygame.K_UP] or keys[pygame.K_w]) and component.intended_y > (0 + 16):
        component.move("up")
        return True
    if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and component.intended_y < (screen_height - 16):
        component.move("down")
        return True
    if keys[pygame.K_SPACE]:
        player_ship.img = pygame.image.load(
            os.path.join("assets", "player_front.png"))


if __name__ == "__main__":
    run()
