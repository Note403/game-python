import pygame


class Enemy(pygame.sprite.Sprite):
    def __init(self, width, height):
        pygame.sprite.Sprite.__init__(self)

        # self.image = pygame.Surface()
        self.position = self.image.get_rect([20, 20])

        self.velocity = 3
