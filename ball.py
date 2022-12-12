import pygame
from random import randint

BLACK = (0, 0, 0)


class Ball(pygame.sprite.Sprite):
    # This class represents a ball. It derives from the "Sprite" class in Pygame.
    screenbound = pygame.Rect(0,0,0,0)
    containers = []
    def __init__(self, color, radius):
        # Call the parent class (Sprite) constructor
        super().__init__()
        # Pass in the color of the ball, its width and height.
        # Set the background color and set it to be transparent
        self.image = pygame.Surface([2*radius, 2*radius])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        # Draw the ball (a rectangle!)
        pygame.draw.circle(self.image,color,[self.image.get_width()//2,self.image.get_width()//2],radius)
        self.mask = pygame.mask.from_surface(self.image.convert_alpha())
        self.radius = radius
        self.velocity = [0, 0]
        self.alive = True
        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y -= self.velocity[1]
        
        if self.rect.right >= self.screenbound.width:
            self.velocity[0] = -self.velocity[0]
        if self.rect.left <= 0:
            self.velocity[0] = -self.velocity[0]
        if self.rect.top <= 0:
            self.velocity[1] = -self.velocity[1]
        if self.rect.top >= self.screenbound.height:
            self.alive = False