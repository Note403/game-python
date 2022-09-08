import math
import pygame

VELOCITY = 5
LERP_FACTOR = 0.05
minimum_distance = 25
maximum_distance = 100
#


class Enemyboss(pygame.sprite.Sprite):
    speed = 2.5

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(
            'assets/zombie_boss.png').convert().subsurface(73, 10, 20, 20)
        self.image = pygame.transform.scale(self.image, (80, 80))

        self.heart_sprite = pygame.image.load(
            'assets/heart_enemy.png').convert_alpha()
        self.heart_sprite = pygame.transform.scale(self.heart_sprite, (24, 24))
        self.rect = self.heart_sprite.get_rect()
        self.rect.center = (720 / 2, 480 / 2)
        self.health = 20

        self.rect = self.image.get_rect()
        self.animation_index = 0
        self.last_change_tick = 0

        self.animation_forwards1 = pygame.image.load(
            'assets/zombie_boss.png').convert().subsurface(9, 10, 40, 45)
        self.animation_forwards1 = pygame.transform.scale(
            self.animation_forwards1, (80, 80))

        self.animation_forwards2 = pygame.image.load(
            'assets/zombie_boss.png').convert().subsurface(140, 10, 40, 45)
        self.animation_forwards2 = pygame.transform.scale(
            self.animation_forwards2, (80, 80))

        self.animation_backwards1 = pygame.image.load(
            'assets/zombie_boss.png').convert().subsurface(9, 137, 40, 45)
        self.animation_backwards1 = pygame.transform.scale(
            self.animation_backwards1, (80, 80))

        self.animation_backwards2 = pygame.image.load(
            'assets/zombie_boss.png').convert().subsurface(140, 138, 40, 45)
        self.animation_backwards2 = pygame.transform.scale(
            self.animation_backwards2, (80, 80))

        self.animation_forwards = [
            self.animation_forwards1,
            self.animation_forwards2,
        ]

        self.animation_backwards = [
            self.animation_backwards1,
            self.animation_backwards2,
        ]

        self.velocity = 3
        self.checkY = 0
        self.checkX = 0

    def move_towards_player(self, player, tick):
        follower_vector = pygame.math.Vector2(player[0])
        target_vector = pygame.math.Vector2(player[1])

        distance = follower_vector.distance_to(target_vector)

        if distance > minimum_distance:
            try:
                dx, dy = player[0] - self.rect.x, player[1] - self.rect.y
                dist = math.hypot(dx, dy)
                # print(self.checkY)
                # print(self.rect.y)

                if self.checkY > self.rect.y:
                    # Geht hoch
                    self.checkY = self.rect.y
                    self.animate_enemy('up', tick)
                    # print('Geht up')

                else:
                    # geht runter
                    # print(self.checkY)
                    # print(self.rect.y)
                    self.checkY = self.rect.y
                    self.animate_enemy('down', tick)

                # if self.checkX > self.rect.x:
                    # Geht Rechts
                #    self.checkX = self.rect.x
                #    self.animate_enemy('left', tick)
                #    print('geht rechts')
                # else:
                    # Geht links
                #    self.checkX = self.rect.x
                #    self.animate_enemy('right', tick)
                #    print('geht Link')

                if dist > 20.0:
                    dx, dy = dx / dist, dy / dist
                    self.rect.x += dx * self.speed
                    self.rect.y += dy * self.speed
            except ZeroDivisionError:
                dist = 50

    def change_sprite_index(self, tick):
        if tick > (self.last_change_tick + 250):
            if self.animation_index == 1:
                self.animation_index = 0
                self.last_change_tick = tick
            else:
                self.animation_index = 1
                self.last_change_tick = tick

    def animate_enemy(self, w_direction, tick):
        if w_direction == 'down':
            self.change_sprite_index(tick)
            self.image = self.animation_forwards[self.animation_index]
            self.image = pygame.transform.scale(self.image, (80, 80))

        if w_direction == 'up':
            self.change_sprite_index(tick)
            self.image = self.animation_backwards[self.animation_index]
            self.image = pygame.transform.scale(self.image, (80, 80))

    def decrease_health(self):
        self.health -= 1
