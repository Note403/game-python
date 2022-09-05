import pygame


class Player(pygame.sprite.Sprite):
    def __init(self, width, height):
        pygame.sprite.Sprite.__init__(self)
# test
        # self.image = pygame.Surface()
        self.position = self.image.get_rect([20, 20])

        self.velocity = 3

    def handle_movement(self, keys_pressed):
        if keys_pressed[pygame.K_w]:
            self.position.y -= self.velocity

        if keys_pressed[pygame.K_s]:
            self.position.y += self.velocity

        if keys_pressed[pygame.K_a]:
            self.position.x -= self.velocity

        if keys_pressed[pygame.K_d]:
            self.position.x += self.velocity
