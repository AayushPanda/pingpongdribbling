# Import the pygame module
import pygame
from ball import Ball
from paddle import Paddle
from block import Block
from random import randint
# Import pygame.locals for easier access to key coordinates
from pygame.locals import (
    K_ESCAPE,
    K_SPACE,
    KEYDOWN,
    QUIT,
    K_r
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
pygame.display.set_caption('Ping Pong')

# create a font object.
# 1st parameter is the font file
# which is present in pygame.
# 2nd parameter is size of the font
font = pygame.font.Font('freesansbold.ttf', 32)

score = 0

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
ball = Ball(RED, 5)
ball.rect.centerx = paddle.rect.centerx
ball.rect.bottom = paddle.rect.top


# This will be a list that will contain all the sprites we intend to use in our game.
all = pygame.sprite.Group()
blocks = pygame.sprite.Group()

# Add the paddles and the ball to the list of objects
all.add(paddle)
all.add(ball)
for x in range(24):
    for y in range(12):
        blocks.add(Block((20*(x+3), 20*(y+3))))

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
                print("Ending game!")
                break
        if not carryOn: break
        keys = pygame.key.get_pressed()
        if state == 0:
            ball.rect.centerx = paddle.rect.centerx
            ball.rect.bottom = paddle.rect.top
            if keys[K_SPACE]:
                ball.velocity = [0, 5]
                state = 1
        
        if keys[K_r]:
            break
        paddle.move(keys)
        all.update()
        blocks.update()

        if pygame.sprite.collide_rect(ball, paddle):
            ball.velocity = [(ball.rect.centerx - paddle.rect.centerx) * 0.25, (paddle.rect.centery - ball.rect.centery) * 0.25]
        
        for block in pygame.sprite.spritecollide(ball, blocks, False):
            prevctr = [ball.rect.centerx - ball.velocity[0], ball.rect.centery - ball.velocity[1]]
            if abs(prevctr[0] - block.rect.centerx) > abs(prevctr[1] - block.rect.centery): # Collision from left or right
                ball.velocity[0] = -ball.velocity[0]
                if ball.velocity[0] == 0: ball.velocity[1] = -ball.velocity[1]
            else: ball.velocity[1] = -ball.velocity[1]
            block.kill()
            break


        # --- Drawing code should go here
        # First, clear the screen to black.

        screen.fill(BLACK)
        # Now let's draw all the sprites in one go. (For now we only have 2 sprites!)
        all.draw(screen)
        blocks.draw(screen)
        pygame.display.update()
        # --- Go ahead and update the screen with what we've drawn.
        clock.tick(60)
        
    paddle.rect.center = (SCREEN_W//2, SCREEN_H - 12)
    ball.rect.centerx = paddle.rect.centerx
    ball.rect.bottom = paddle.rect.top
    ball.alive = True
    ball.velocity = [0, 0]
    state = 0
    