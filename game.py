# Import the pygame module
import pygame as pg
from ball import Ball
from dart import Dart
from random import randint
import pickle
from multiLineSurface import multiLineSurface
import numpy as np
from numpy.linalg import norm
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
pg.init()

SCREEN_H = 1080
SCREEN_W = 1920
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

streak = 0

# assigning values to X and Y variable
X = 400
Y = 400

# create the display surface object
# of specific dimension..e(X, Y).
display_surface = pg.display.set_mode((X, Y))

# set the pygame window name
pg.display.set_caption('Flatland Wars')

# create a font object.
# 1st parameter is the font file
# which is present in pygame.
# 2nd parameter is size of the font
font = pg.font.Font('freesansbold.ttf', 32)

# create a text surface object,
# on which text is drawn on it.
text = font.render(f'Streak: {streak}', True, WHITE, BLACK)

# create a rectangular object for the
# text surface object
textRect = text.get_rect()

score_genned = False

alive = True

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pg.display.set_mode((SCREEN_W, SCREEN_H), pg.FULLSCREEN)

ball = Ball(RED, 20)
ball.rect.x = randint(ball.image.get_width() // 2, 1920)
ball.rect.y = randint(ball.image.get_width() // 2, 1080)

# This will be a list that will contain all the sprites we intend to use in our game.
all_sprites_list = pg.sprite.Group()

# Add the paddles and the ball to the list of objects
all_sprites_list.add(ball)

# The loop will carry on until the user exits the game (e.g. clicks the close button).
carryOn = True

# The clock will be used to control how fast the screen updates
clock = pg.time.Clock()

# -------- Main Program Loop -----------
while carryOn:
    # --- Main event loop

    if alive:

        keys = pg.key.get_pressed()

            # --- Game logic should go here
        all_sprites_list.update()

        # Check if the ball is bouncing against any of the 4 walls:
        if ball.rect.x >= SCREEN_W - ball.radius * 2:
            ball.velocity[0] = -ball.velocity[0]*0.9
        if ball.rect.x <= 0:
            ball.velocity[0] = -ball.velocity[0]*0.9
        if ball.rect.y > SCREEN_H - ball.radius * 2:
            ball.velocity[1] = -ball.velocity[1]*0.4
        if ball.rect.y < 0:
            alive = False

            # --- Drawing code should go here
        # First, clear the screen to black.
        screen.fill(BLACK)

        # Now let's draw all the sprites in one go. (For now we only have 2 sprites!)
        all_sprites_list.draw(screen)

        text = font.render(f'Streak: {streak}', True, WHITE, BLACK)
        display_surface.blit(text, textRect)

        # --- Go ahead and update the screen with what we've drawn.
        pg.display.update()

    elif not gotName:

        display_surface.fill(BLACK)

        text = font.render("Enter initials:", True, WHITE, BLACK)
        textRect.centerx = 1920//2
        textRect.y = (1080//2) - 170
        display_surface.blit(text, textRect)

        for event in pg.event.get():  # User did something
            if event.type == K_ESCAPE:  # If user clicked close
                carryOn = False  # Flag that we are done so we exit this loop
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    name = name[-3:]
                    gotName = True
                else:
                    name = name[1:] + event.unicode

        text = font.render(name[-3:], True, WHITE, BLACK)
        textRect.center = (1920//2, 1080//2)
        display_surface.blit(text, textRect)

        pg.display.update()


    elif not score_genned and gotName:

        scores_vals = list(scores.values())
        scores_keys = list(scores.keys())

        scores_vals.append(streak)
        scores_keys.append(name)

        scores_vals, scores_keys = zip(*sorted(zip(scores_vals, scores_keys)))

        scores_keys = scores_keys[::-1][:min(5, len(scores_keys))]
        scores_vals = scores_vals[::-1][:min(5, len(scores_vals))]

        scores = {}

        score_disp_text = "TOP SCORES\n"

        for idx in range(len(scores_vals)):
            score_disp_text += f"{scores_keys[idx]}: {scores_vals[idx]}\n"
            scores[scores_keys[idx]] = scores_vals[idx]

        with open("scores.pickle", "wb") as f:
            pickle.dump(scores, f)

        display_surface.fill(BLACK)

        message_box(score_disp_text.splitlines())

        score_genned = True

    else:
        # --- Go ahead and update the screen with what we've drawn.
        pg.display.update()

    # --- Limit to 60 frames per second
    clock.tick(59)
