import sys

import pygame
from player.player import Player

pygame.init()
pygame.font.init()
pygame.key.set_repeat(True)


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

        self.fps_font = pygame.font.SysFont('Arial', 15)

        self.background = pygame.image.load('assets/background.png')
        self.background = pygame.transform.scale(
            self.background,
            (self.background.get_width() * 2.5, self.background.get_height() * 2.5)
        )

        self.bg_data = {
            'min_x': 0 - (self.display.get_width() / 2)
        }

        self.bg_min_x = 0 - (self.display.get_width() / 2)
        self.bg_min_y = 0 - (self.display.get_width() / 2)

        self.bg_max_x = self.bg_min_x + self.display.get_width()
        self.bg_max_y = self.bg_min_y + self.display.get_height()

        self.icon = pygame.image.load('assets/icon.gif')
        pygame.display.set_icon(self.icon)

    def draw_camera(self):
        if (self.player.f_x - (self.display.get_width() / 2)) <= self.bg_min_x:
            bg_x = 0

            if self.player.f_x >= self.bg_min_x:
                player_x = (self.display.get_width() / 2) + self.player.f_x
            else:
                player_x = self.bg_min_x
                self.player.f_x = self.bg_min_x + 1
        else:
            bg_x = 0 - self.player.f_x
            player_x = self.display.get_width() / 2

        self.display.blit(self.background, (bg_x, 0 - self.player.f_y))
        self.display.blit(self.player.image, [player_x, self.display.get_height() / 2])

    def game(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                keys_pressed = pygame.key.get_pressed()

                if self.player.in_attack:
                    self.player.handle_attack(keys_pressed, pygame.time.get_ticks())

                if event.type == pygame.KEYDOWN:
                    self.player.handle_movement(keys_pressed, pygame.time.get_ticks())

            self.sprites.update()
            self.draw_camera()

            for i in range(self.player.lifes):
                self.display.blit(self.player.heart_sprite, (i * 20, 0))

            self.display.blit(self.fps_font.render(str(self.clock.get_fps()), False, (255, 255, 255)), (0, 30))
            self.display.blit(self.fps_font.render("PLAYER_X: " + str(self.player.f_x), False, (255, 255, 255)), (0, 50))
            self.display.blit(self.fps_font.render("PLAYER_Y: " + str(self.player.f_y), False, (255, 255, 255)), (0, 600))
            pygame.display.flip()
            self.clock.tick(60)

        sys.exit()


game = Game()
game.game()
