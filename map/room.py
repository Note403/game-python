import pygame
import random

from enemy.enemy import Enemy


class Room:
    def __init__(self, x, y, room_layout):
        self.x = x
        self.y = y

        self.sprite_img = pygame.image.load('assets/dungeon_tiles.png').convert()
        self.floor = self.sprite_img.subsurface(31, 31, 82, 93)
        self.floor = pygame.transform.scale(self.floor, (350, 350))

        self.door = self.sprite_img.subsurface(192, 212, 16, 16)
        self.door = pygame.transform.scale(self.door, (32, 32))

        self.enemies_alive = 0

        self.doors = {
            'top': 0,
            'bottom': 0,
            'left': 0,
            'right': 0
        }

        self.door_cords = []

        self.enemies = []

        self.boss_room = False
        self.entered = False

        self.set_doors(room_layout)
        self.spawn_enemies()

    def set_doors(self, room_layout):
        if self.x > 0:
            self.doors['left'] = room_layout[self.y][self.x - 1]
        else:
            self.doors['left'] = 0

        if self.x < 4:
            self.doors['right'] = room_layout[self.y][self.x + 1]
        else:
            self.doors['right'] = 0

        if self.y > 0:
            self.doors['top'] = room_layout[self.y - 1][self.x]
        else:
            self.doors['top'] = 0

        if self.y < (len(room_layout) - 1):
            self.doors['bottom'] = room_layout[self.y + 1][self.x]
        else:
            self.doors['bottom'] = 0

    def draw(self, display):
        display.blit(
            self.floor,
            (
                (display.get_width() / 2) + - (self.floor.get_width() / 2),
                (display.get_height() / 2) - (self.floor.get_height() / 2)
            )
        )

        self.get_door_cords(display)

        for cords in self.door_cords:
            display.blit(self.door, cords)

        for enemy in self.enemies:
            display.blit(enemy.image, enemy.rect)

    def get_door_cords(self, display):

        display_mid = [display.get_width() / 2, display.get_height() / 2]

        if self.doors['top']:
            self.door_cords.append(
                [
                    display_mid[0] - (self.door.get_width() / 2),
                    display_mid[1] - (self.floor.get_height() / 2) + 10
                ]
            )

        if self.doors['bottom']:
            self.door_cords.append(
                [
                    display_mid[0] - (self.door.get_width() / 2),
                    display_mid[1] + (self.floor.get_height() / 2) - self.door.get_height() - 40
                ]
            )

        if self.doors['right']:
            self.door_cords.append(
                [
                    display_mid[0] + (self.floor.get_width() / 2) - self.door.get_width() - 10,
                    display_mid[1] - (self.door.get_height() / 2)
                ]
            )

        if self.doors['left']:
            self.door_cords.append(
                [
                    display_mid[0] - (self.floor.get_width() / 2) + self.door.get_width() - 20,
                    display_mid[1] - (self.door.get_height() / 2)
                ]
            )

    def spawn_enemies(self):
        if self.entered:
            return

        self.enemies_alive = random.randint(2, 4)

        for i in range(self.enemies_alive):
            self.enemies.append(Enemy(self, 720, 480))

    def remove_enemy(self, enemy):
        self.enemies.remove(enemy)
        self.enemies_alive -= 1
