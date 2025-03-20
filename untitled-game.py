#Credits to Vincent from coding class

import pygame

from pygame.locals import *

import copy

# Import pygame.locals for access to key coordinates
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

pygame.init()

# Width and height of the screen
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

screen.fill((255, 255, 255))


# x = 100
# y = 100

class snake(pygame.sprite.Sprite):
    def __init__(self, position, up_key, down_key, left_key, right_key, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((0, 0, 0))
        self.rect = self.surf.get_rect(topleft=position)
        self.up_key = up_key
        self.down_key = down_key
        self.left_key = left_key
        self.right_key = right_key
        self.x = x
        self.y = y

    def update(self, keys1):
        if keys1[self.up_key]:
            self.rect.move_ip(0, -2)
        if keys1[self.down_key]:
            self.rect.move_ip(0, 2)
        if keys1[self.left_key]:
            self.rect.move_ip(-2, 0)
        if keys1[self.right_key]:
            self.rect.move_ip(2, 0)
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


class raven(pygame.sprite.Sprite):
    def __init__(self, position, up_key, down_key, left_key, right_key, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((0, 0, 255))
        self.rect = self.surf.get_rect(topleft=position)
        self.up_key = up_key
        self.down_key = down_key
        self.left_key = left_key
        self.right_key = right_key
        self.x = x
        self.y = y

    def update(self, keys2):
        if keys2[self.up_key]:
            self.rect.move_ip(0, -2)
        if keys2[self.down_key]:
            self.rect.move_ip(0, 2)
        if keys2[self.left_key]:
            self.rect.move_ip(-2, 0)
        if keys2[self.right_key]:
            self.rect.move_ip(2, 0)
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


def collide(sprite1, sprite2):
    return sprite1.rect.colliderect(sprite2.rect)

class projectile(pygame.sprite.Sprite):
    def __init__ (self, position, up_key, down_key, left_key, right_key, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.surf = pygame.Surface((40, 10))
        self.surf.fill((255, 0, 0))
        self.rect = self.surf.get_rect(topleft=position)
        self.x_speed = 6
        self.y_speed = 0
        #self.p_is_pressed = True

    def shoot(self, x, y, keys1):
        self.x += self.x_speed
        self.y += self.y_speed
        self.rect.topleft = (self.x, self.y)






snake = snake((500, 500), K_UP, K_DOWN, K_LEFT, K_RIGHT, 500, 500)
raven = raven((100, 100), pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, 100, 100)
projectile = projectile((snake.x, snake.y), K_w, K_s, K_p, K_r, snake.x, snake.y)

# Variable to keep the main loop running
running = True

p_is_pressed = False

projectiles = []

# Main loop
while running:
    clock = pygame.time.Clock()
    clock.tick(120)

    # Look at every event in the queue
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop.
            if event.key == K_ESCAPE:
                running = False
            elif event.key == K_p:
                p_is_pressed = True
        # Did the user click the window close button? If so, stop the loop.
        elif event.type == QUIT:
            running = False

    screen.fill((255, 255, 255))

    keys1 = pygame.key.get_pressed()
    keys2 = pygame.key.get_pressed()
    snake.update(keys1)
    raven.update(keys2)



    if collide(snake, raven):
        # we make the inverse of the vector between p1 and p2's centers
        between_centers = pygame.math.Vector2(raven.rect.centerx - snake.rect.centerx,
                                              raven.rect.centery - snake.rect.centery)
        # we scale that vector by half, to make each player be reppelled by the same amount
        between_centers.scale_to_length(between_centers.length() / 2)

        # we move p1 backwards
        snake.rect.move_ip(-between_centers.x, -between_centers.y)

        # we invert the vector, to push p2 in the opposite direction
        between_centers.rotate_ip(180)
        raven.rect.move_ip(-between_centers.x, -between_centers.y)



    screen.blit(snake.surf, snake.rect)
    screen.blit(raven.surf, raven.rect)


    #projectile.shoot(projectile.rect.x, projectile.rect.y, keys1)
    #projectile.shoot(keys1)


    if p_is_pressed:
        screen.blit(projectile.surf, (projectile.x, projectile.y))
        projectile.shoot(projectile.rect.x, projectile.rect.y, keys1)
    if projectile.x > SCREEN_WIDTH:
       # projectile.rect.copy()
        projectile.x = snake.rect.x
        projectile.y = snake.rect.y
        p_is_pressed = False

    if projectile.y > SCREEN_HEIGHT:
        projectile.y_speed = 0
        projectile.rect.x = snake.rect.x
        projectile.rect.y = snake.rect.y




    pygame.display.flip()

pygame.quit()
