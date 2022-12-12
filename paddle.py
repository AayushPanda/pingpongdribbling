import pygame
from pygame.locals import *
from random import randint

WHITE = (255, 255, 255)


class Paddle(pygame.sprite.Sprite):
    screenbound = pygame.Rect(0,0,0,0)
    def __init__(self, origin):
        # Call the parent class (Sprite) constructor
        super().__init__()
        self.image = pygame.Surface([80,8])
        self.image.fill(WHITE)
        self.mask = pygame.mask.from_surface(self.image)

        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect(center=origin)

    def move(self, keystate):
        direction = -int(keystate[K_LEFT]) + int(keystate[K_RIGHT])
        if keystate[K_LSHIFT]: direction *= 2
        self.rect.x += direction * 3
        self.rect.clamp_ip(self.screenbound)
        
