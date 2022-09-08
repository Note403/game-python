import sys

import pygame
from player.player import Player
from enemy.enemy import Enemy
from map.map_generator import MapGenerator

pygame.init()
pygame.font.init()
pygame.key.set_repeat(True)


class Game:
    def __init__(self):
        pygame.display.set_caption("THE CHAMBER OF DEATH")
        self.size = height, width = 720, 480
        self.display = pygame.display.set_mode(self.size)

        self.game_over_font = pygame.font.SysFont('Arial', 45, True)
        self.game_over = self.game_over_font.render('GAME OVER', False, (200, 50, 50))

        self.map_gen = MapGenerator()
        self.player = Player(width, height)

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

        self.room = None

        self.icon = pygame.image.load('assets/icon.gif')
        pygame.display.set_icon(self.icon)

    def game(self):
        self.map_gen.generate_room_layout()

        while self.running:
            self.room = self.map_gen.get_room()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                keys_pressed = pygame.key.get_pressed()

                if self.player.in_attack:
                    self.player.handle_attack(
                        keys_pressed, pygame.time.get_ticks(), self.room)

                if event.type == pygame.KEYDOWN:
                    self.player.handle_movement(keys_pressed, pygame.time.get_ticks(), self.room, self.display)

            door_hit = self.map_gen.player_in_door(self.player, self.room)

            if door_hit != False:
                if door_hit[0] > ((self.display.get_width() / 2) + 32):
                    self.map_gen.room_atm = [self.map_gen.room_atm[0] + 1, self.map_gen.room_atm[1]]
                    self.room = self.map_gen.get_room()
                    self.player.f_x = self.display.get_width() / 2
                    self.player.f_y = self.display.get_height() / 2
                elif door_hit[0] < ((self.display.get_width() / 2) - 32):
                    self.map_gen.room_atm = [self.map_gen.room_atm[0] - 1, self.map_gen.room_atm[1]]
                    self.room = self.map_gen.get_room()
                    self.player.f_x = self.display.get_width() / 2
                    self.player.f_y = self.display.get_height() / 2
                elif door_hit[1] < (self.display.get_height() / 2):
                    self.map_gen.room_atm = [self.map_gen.room_atm[0], self.map_gen.room_atm[1] - 1]
                    self.room = self.map_gen.get_room()
                    self.player.f_x = self.display.get_width() / 2
                    self.player.f_y = self.display.get_height() / 2
                elif door_hit[1] > (self.display.get_height() / 2):
                    self.map_gen.room_atm = [self.map_gen.room_atm[0], self.map_gen.room_atm[1] + 1]
                    self.room = self.map_gen.get_room()
                    self.player.f_x = self.display.get_width() / 2
                    self.player.f_y = self.display.get_height() / 2

            self.player.got_hit(self.room, pygame.time.get_ticks())

            if self.player.health <= 0:
                sys.exit()

            player = self.player.get_loc()

            for enemy in self.room.enemies:
                enemy.move_towards_player(player, pygame.time.get_ticks())

            for enemy in self.room.enemies:
                self.display.blit(enemy.image, enemy.rect)

            self.display.fill((0, 0, 0))
            self.sprites.update()
            self.room.draw(self.display)

            self.display.blit(self.player.image, (self.player.f_x, self.player.f_y))

            for i in range(self.player.health):
                self.display.blit(self.player.heart_sprite, (i * 20, 0))

            pygame.display.flip()
            self.clock.tick(60)


game = Game()
game.game()
