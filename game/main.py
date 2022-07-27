import pygame, sys
from pygame.locals import *
from settings import *
import os

pygame.init()
pygame.display.set_caption("Crypto Astroneer")
clock = pygame.time.Clock()

WINDOW = pygame.display.set_mode((screen_width, screen_height))
BG = pygame.image.load(os.path.join("assets", "title_screen.jpg"))
BG = pygame.transform.scale(BG, (960,640))

def run():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


        WINDOW.blit(BG, (0,0))
        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    run()