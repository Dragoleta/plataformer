import pygame
from settings import *
from level import Level

pygame.init()
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("PyGame practice")
clock = pygame.time.Clock()
level = Level(levelMap, screen)


def mainGame():
    running = True
    while running:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

        screen.fill('black')
        level.run()
        pygame.display.update()
    mainGame()


if __name__ == '__main__':
    mainGame()
