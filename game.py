# Import the pygame module
import pygame
from ball import Ball
from paddle import Paddle
from random import randint
import pickle
# Import pygame.locals for easier access to key coordinates
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_SPACE,
    KEYDOWN,
    QUIT,
    K_RETURN
)

# Initialize pygame
pygame.init()

SCREEN_H = 400
SCREEN_W = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
SCREENRECT = pygame.Rect(0, 0, SCREEN_W, SCREEN_H)

# assigning values to X and Y variable
X = 400
Y = 400

# create the display surface object
# of specific dimension..e(X, Y).
display_surface = pygame.display.set_mode((X, Y))

# set the pygame window name
pygame.display.set_caption('Flatland Wars')

# create a font object.
# 1st parameter is the font file
# which is present in pygame.
# 2nd parameter is size of the font
font = pygame.font.Font('freesansbold.ttf', 32)

score_genned = False

state = 0
"""
0 - Ball on top of paddle
1 - Gameplay
"""

alive = True

# Initialize Class Data
Paddle.screenbound = SCREENRECT
Ball.screenbound = SCREENRECT

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H), pygame.SHOWN)

paddle = Paddle((SCREEN_W//2, SCREEN_H - 12))
ball = Ball(RED, 10)
ball.rect.centerx = paddle.rect.centerx
ball.rect.bottom = paddle.rect.top


# This will be a list that will contain all the sprites we intend to use in our game.
all = pygame.sprite.Group()

# Add the paddles and the ball to the list of objects
all.add(paddle)
all.add(ball)

# The loop will carry on until the user exits the game (e.g. clicks the close button).
carryOn = True

# The clock will be used to control how fast the screen updates
clock = pygame.time.Clock()

# -------- Main Program Loop -----------
while carryOn:
    # --- Main event loop

    while ball.alive:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                carryOn = False
                break
        keys = pygame.key.get_pressed()
        if state == 0:
            ball.rect.centerx = paddle.rect.centerx
            ball.rect.bottom = paddle.rect.top
            if keys[K_SPACE]:
                ball.velocity = [0, 5]
                state = 1
        
        paddle.move(keys)
        all.update()

        if pygame.sprite.collide_rect(ball, paddle):
            ball.velocity = [ball.rect.centerx - paddle.rect.centerx, (paddle.rect.centery - ball.rect.centery) * 0.5]

        # --- Drawing code should go here
        # First, clear the screen to black.

        screen.fill(BLACK)
        # Now let's draw all the sprites in one go. (For now we only have 2 sprites!)
        all.draw(screen)
        pygame.display.update()
        # --- Go ahead and update the screen with what we've drawn.
        clock.tick(30)
        
    paddle.rect.center = (SCREEN_W//2, SCREEN_H - 12)
    ball.rect.centerx = paddle.rect.centerx
    ball.rect.bottom = paddle.rect.top
    ball.alive = True
    ball.velocity = [0, 0]
    state = 0
    