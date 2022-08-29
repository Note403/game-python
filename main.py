import sys

import pygame

pygame.init()


class Game:
    size = height, width = 720, 480
    display = pygame.display.set_mode(size)
    player = pygame.Rect(0, 0, 50, 100)
    running = True

    def __init__(self):
        pygame.display.set_caption("GAME")

    def game(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            pygame.draw.rect(self.display, (0, 200, 0), self.player)
            pygame.display.flip()

        sys.exit()


game = Game()
game.game()
