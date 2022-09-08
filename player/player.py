import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        pygame.sprite.Sprite.__init__(self)
        self.width = 36
        self.height = 36
        self.sprite_img = pygame.image.load(
            'assets/player_sprite.png').convert()
        self.image = self.sprite_img.subsurface(0, 38, 16, 16)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.heart_sprite = pygame.image.load('assets/heart.png').convert_alpha()
        self.heart_sprite = pygame.transform.scale(self.heart_sprite, (24, 24))
        self.rect = self.image.get_rect()

        self.health = 4
        self.range = 50

        self.f_x = (screen_width / 2) - (self.width / 2)
        self.f_y = (screen_height / 2) - (self.height / 2)

        self.velocity = 0.3

        # ANIMATIONS

        self.animation_index = 0
        self.last_change_tick = 0
        self.last_direction = 's'

        self.last_attack = 0
        self.last_hit = 0
        self.in_attack = False

        self.attack_sprites = {
            'w': self.sprite_img.subsurface(50, 0, 16, 16),
            'a': self.sprite_img.subsurface(48, 55, 16, 16),
            's': self.sprite_img.subsurface(50, 39, 16, 16),
            'd': self.sprite_img.subsurface(50, 20, 16, 16)
        }

        self.image = self.attack_sprites['d']
        self.image = pygame.transform.scale(self.image, (36, 36))

        self.animation_left = [
            self.sprite_img.subsurface(0, 56, 16, 16),
            self.sprite_img.subsurface(32, 56, 16, 16),
        ]

        self.animation_right = [
            self.sprite_img.subsurface(0, 20, 16, 16),
            self.sprite_img.subsurface(32, 20, 16, 16),
        ]

        self.animation_forwards = [
            self.sprite_img.subsurface(0, 2, 16, 16),
            self.sprite_img.subsurface(32, 2, 16, 16),
        ]

        self.animation_backwards = [
            self.sprite_img.subsurface(0, 38, 16, 16),
            self.sprite_img.subsurface(32, 38, 16, 16),
        ]

    def handle_movement(self, keys_pressed, tick, room, display):
        self.handle_attack(keys_pressed, tick, room)

        if self.in_attack:
            return

        room_rect = pygame.rect.Rect(
            (display.get_width() / 2) - (room.floor.get_width() / 2) + 30,
            (display.get_height() / 2) - (room.floor.get_height() / 2) + 30,
            room.floor.get_width() - 60,
            room.floor.get_height() - 100
        )

        if keys_pressed[pygame.K_w]:
            player_rect = pygame.rect.Rect(self.f_x, self.f_y - self.velocity, self.width, self.height)

            if not room_rect.colliderect(player_rect):
                return

            self.f_y -= self.velocity

            self.last_direction = 'w'
            self.animate('w', tick)

        if keys_pressed[pygame.K_s]:
            player_rect = pygame.rect.Rect(self.f_x, self.f_y + self.velocity, self.width, self.height)

            if not room_rect.colliderect(player_rect):
                return

            self.f_y += self.velocity

            self.last_direction = 's'
            self.animate('s', tick)

        if keys_pressed[pygame.K_a]:
            player_rect = pygame.rect.Rect(self.f_x - self.velocity, self.f_y, self.width, self.height)

            if not room_rect.colliderect(player_rect):
                return

            self.f_x -= self.velocity

            self.last_direction = 'a'
            self.animate('a', tick)

        if keys_pressed[pygame.K_d]:
            player_rect = pygame.rect.Rect(self.f_x + self.velocity, self.f_y, self.width, self.height)

            if not room_rect.colliderect(player_rect):
                return

            self.f_x += self.velocity

            self.last_direction = 'd'
            self.animate('d', tick)

    def animate(self, w_direction, tick):
        if w_direction == 'w':
            self.change_sprite_index(tick)

            self.image = self.animation_forwards[self.animation_index]
            self.image = pygame.transform.scale(self.image, (36, 36))

        if w_direction == 's':
            self.change_sprite_index(tick)

            self.image = self.animation_backwards[self.animation_index]
            self.image = pygame.transform.scale(self.image, (36, 36))

        if w_direction == 'a':
            self.change_sprite_index(tick)

            self.image = self.animation_left[self.animation_index]
            self.image = pygame.transform.scale(self.image, (36, 36))

        if w_direction == 'd':
            self.change_sprite_index(tick)

            self.image = self.animation_right[self.animation_index]
            self.image = pygame.transform.scale(self.image, (36, 36))

    def change_sprite_index(self, tick):
        if tick > (self.last_change_tick + 250):
            if self.animation_index == 1:
                self.animation_index = 0
                self.last_change_tick = tick
            else:
                self.animation_index = 1
                self.last_change_tick = tick

    def handle_attack(self, keys_pressed, tick, room):
        if self.in_attack:
            if self.last_attack + 55 < tick:
                self.in_attack = False
                self.load_old_sprite()

            return

        if self.last_attack + 200 > tick:
            return

        if keys_pressed[pygame.K_SPACE]:
            self.image = self.attack_sprites[self.last_direction]
            self.image = pygame.transform.scale(self.image, (36, 36))
            self.in_attack = True
            self.last_attack = tick

            hitbox_y = self.f_y
            hitbox_x = self.f_x

            if self.last_direction == 'w':
                hitbox_y -= self.range
            elif self.last_direction == 's':
                hitbox_y += self.height
            elif self.last_direction == 'd':
                hitbox_x += self.width
            elif self.last_direction == 'a':
                hitbox_x -= self.width

            hit_rect = pygame.rect.Rect(hitbox_x, hitbox_y, self.range, self.range)

            for enemy in room.enemies:
                if hit_rect.colliderect(enemy.rect):
                    enemy.health -= 1

                    if enemy.health <= 0:
                        room.remove_enemy(enemy)

    def load_old_sprite(self):
        self.animation_index = 0

        if self.last_direction == 'w':
            self.image = self.animation_forwards[self.animation_index]
        elif self.last_direction == 'a':
            self.image = self.animation_left[self.animation_index]
        elif self.last_direction == 's':
            self.image = self.animation_backwards[self.animation_index]
        elif self.last_direction == 'd':
            self.image = self.animation_right[self.animation_index]

        self.image = pygame.transform.scale(self.image, (36, 36))

    def get_loc(self):
        player_location = (self.f_x, self.f_y)
        return player_location

    def decrease_health(self):
        self.health -= 1

    def increase_health(self):
        self.health += 1

    def got_hit(self, room, tick):
        if self.last_hit + 1000 > tick:
            return

        player_rect = pygame.rect.Rect(self.f_x, self.f_y, self.width, self.height)

        for enemy in room.enemies:
            if player_rect.colliderect(enemy):
                self.last_hit = tick
                self.decrease_health()



