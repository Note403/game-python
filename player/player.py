import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(
            'assets/player_sprite.png').convert().subsurface(0, 38, 16, 16)
        self.image = pygame.transform.scale(self.image, (36, 36))
        self.rect = self.image.get_rect()

        self.velocity = 3

    def handle_movement(self, keys_pressed):
        if keys_pressed[pygame.K_w]:
            self.rect.y -= self.velocity

        if keys_pressed[pygame.K_s]:
            self.rect.y += self.velocity

        if keys_pressed[pygame.K_a]:
            self.rect.x -= self.velocity

        if keys_pressed[pygame.K_d]:
            self.rect.x += self.velocity

    def get_loc(self):
        player_location = (self.rect.x, self.rect.y)
        return player_location
