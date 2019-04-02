import pygame

class Pipe(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.WIDTH = 48
        self.HEIGHT = 500
        self.SPEED = -4

        self.x = 0
        self.y = 0

        self.image = pygame.Surface((self.WIDTH,self.HEIGHT))
        self.image.fill((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.center = (0,0)

    def update(self):
        self.x += self.SPEED
        self.rect = (self.x,self.y)
