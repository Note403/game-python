import sys

import pygame
from player.player import Player

pygame.init()


class Game:
    def __init__(self):
        pygame.display.set_caption("GAME")
        self.size = height, width = 720, 480
        self.display = pygame.display.set_mode(self.size)

        self.player = Player()

        self.running = True
        self.clock = pygame.time.Clock()

        self.sprites = pygame.sprite.Group()
        self.sprites.add(self.player)

    def game(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    keys_pressed = pygame.key.get_pressed()
                    self.player.handle_movement(keys_pressed)

            self.sprites.update()
            self.display.fill((0, 0, 0))
            self.sprites.draw(self.display)
            pygame.display.flip()
            self.clock.tick(60)

        sys.exit()


game = Game()
game.game()
