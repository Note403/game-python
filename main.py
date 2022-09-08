import sys

import pygame
from player.player import Player
from enemy.enemy import Enemy
from enemy.enemygirl import Enemygirl
from enemy.enemyboss import Enemyboss

from map.map_generator import MapGenerator

pygame.init()
pygame.font.init()
pygame.key.set_repeat(True)


class Game:
    def __init__(self):
        pygame.display.set_caption("GAME")
        self.size = height, width = 720, 480
        self.display = pygame.display.set_mode(self.size)

        self.map_gen = MapGenerator()
        self.player = Player(width, height)
        self.enemy = Enemy()
        self.enemygirl = Enemygirl()
        self.enemyboss = Enemyboss()

        self.running = True
        self.clock = pygame.time.Clock()

        self.sprites = pygame.sprite.Group()
        self.sprites.add(self.player)
        self.sprites.add(self.enemy)
        self.sprites.add(self.enemygirl)
        self.sprites.add(self.enemyboss)

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

        self.room = None

        self.icon = pygame.image.load('assets/icon.gif')
        pygame.display.set_icon(self.icon)

    def game(self):
        self.map_gen.generate_room_layout()

        while self.running:
            self.room = self.map_gen.get_room()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                keys_pressed = pygame.key.get_pressed()

                if self.player.in_attack:
                    self.player.handle_attack(
                        keys_pressed, pygame.time.get_ticks())

                if event.type == pygame.KEYDOWN:
                    self.player.handle_movement(
                        keys_pressed, pygame.time.get_ticks(), self.room, self.display)

            player = self.player.get_loc()
            self.enemy.move_towards_player(player, pygame.time.get_ticks())
            self.enemygirl.move_towards_player(
                player, pygame.time.get_ticks())
            self.enemyboss.move_towards_player(
                player, pygame.time.get_ticks())
            self.display.fill((0, 0, 0))
            self.sprites.update()
            self.room.draw(self.display)

            self.display.blit(self.player.image,
                              (self.player.f_x, self.player.f_y))
            self.display.blit(self.enemy.image,
                              (self.enemy.rect.x, self.enemy.rect.y))
            self.display.blit(self.enemygirl.image,
                              (self.enemygirl.rect.x, self.enemygirl.rect.y))
            self.display.blit(self.enemyboss.image,
                              (self.enemyboss.rect.x, self.enemyboss.rect.y))

            for i in range(self.player.health):
                self.display.blit(self.player.heart_sprite, (i * 20, 0))

            for i in range(self.enemyboss.health):
                self.display.blit(
                    self.enemyboss.heart_sprite, (i * 25, 430))

            self.display.blit(self.fps_font.render(
                str(self.clock.get_fps()), False, (255, 255, 255)), (0, 30))
            self.display.blit(self.fps_font.render(
                "PLAYER_X: " + str(self.player.f_x), False, (255, 255, 255)), (0, 50))
            self.display.blit(self.fps_font.render(
                "PLAYER_Y: " + str(self.player.f_y), False, (255, 255, 255)), (0, 600))
            pygame.display.flip()
            self.clock.tick(60)

        sys.exit()


game = Game()
game.game()
