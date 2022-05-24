import pygame
import math
from helper import *
from particles import *
import stats

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class Shell:
    def __init__(self, position, direction):
        self.direction = direction
        self.surf = pygame.Surface((8, 8))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
        self.bullet = pygame.transform.scale(pygame.image.load("assets/shell.png").convert_alpha(), (8, 8))
        self.speed = 20
        self.rect.centerx = position[0]
        self.rect.centery = position[1]
        self.vel = [0, 0]
        ds = directionSpeed(self.direction, self.speed)
        self.vel[0] = ds[0]
        self.vel[1] = -ds[1]
        self.active = True
        self.rect.move_ip(self.vel[0] * 0.2, self.vel[1] * 0.2)
        self.damage = stats.shelldamage
        self.areadamage = stats.shellareadamage
        self.knockback = 20
        self.sound = pygame.mixer.Sound("assets/shell.wav")
        self.aoerect = pygame.Rect(self.rect.centerx - stats.shellaoe, self.rect.centery - stats.shellaoe,
                                   stats.shellaoe * 2,
                                   stats.shellaoe * 2)

    # update object location & state
    def update(self, dt):
        # move the bullet
        self.rect.move_ip(self.vel[0] * dt, self.vel[1] * dt)
        self.aoerect.center = self.rect.center
        # checks if its inside the screen
        if not onScreen(self.rect, SCREEN_WIDTH, SCREEN_HEIGHT, 16, 12):
            self.active = False

    def draw(self, screen):
        # draw the bullet
        rotatedbullet = pygame.transform.rotate(self.bullet, self.direction)
        screen.blit(rotatedbullet, (
            self.rect.centerx - int(rotatedbullet.get_width() / 2),
            self.rect.centery - int(rotatedbullet.get_height() / 2)))


class Bullet:
    def __init__(self, position, direction):
        self.direction = direction
        self.surf = pygame.Surface((4, 4))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
        self.bullet = pygame.transform.scale(pygame.image.load("assets/bullet.png").convert_alpha(), (2, 4))
        self.speed = 25
        self.rect.centerx = position[0]
        self.rect.centery = position[1]
        self.vel = [0, 0]
        ds = directionSpeed(self.direction, self.speed)
        self.vel[0] = ds[0]
        self.vel[1] = -ds[1]
        self.active = True
        self.rect.move_ip(self.vel[0] * 0.1, self.vel[1] * 0.1)
        self.damage = stats.bulletdamage
        self.knockback = 5
        self.sound = pygame.mixer.Sound("assets/bullet.wav")

    # update object location & state
    def update(self, dt):
        # move the bullet
        self.rect.move_ip(self.vel[0] * dt, self.vel[1] * dt)
        # checks if its inside the screen
        if not onScreen(self.rect, SCREEN_WIDTH, SCREEN_HEIGHT, 16, 12):
            self.active = False

    def draw(self, screen):
        # draw the bullet
        rotatedbullet = pygame.transform.rotate(self.bullet, self.direction)
        screen.blit(rotatedbullet, (
            self.rect.centerx - int(rotatedbullet.get_width() / 2),
            self.rect.centery - int(rotatedbullet.get_height() / 2)))


class MinionBullet:
    def __init__(self, position, direction):
        self.direction = direction
        self.surf = pygame.Surface((2, 2))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
        self.bullet = pygame.image.load("assets/minionbullet.png").convert_alpha()
        self.speed = 25
        self.rect.centerx = position[0]
        self.rect.centery = position[1]
        self.vel = [0, 0]
        ds = directionSpeed(self.direction, self.speed)
        self.vel[0] = ds[0]
        self.vel[1] = -ds[1]
        self.active = True
        self.damage = stats.level // 5
        self.knockback = 5
        self.sound = pygame.mixer.Sound("assets/bullet.wav")

    # update object location & state
    def update(self, dt):
        # move the bullet
        self.rect.move_ip(self.vel[0] * dt, self.vel[1] * dt)
        # checks if it's inside the screen
        if not onScreen(self.rect, SCREEN_WIDTH, SCREEN_HEIGHT, 16, 12):
            self.active = False

    def draw(self, screen):
        # draw the bullet
        rotatedbullet = pygame.transform.rotate(self.bullet, self.direction)
        screen.blit(rotatedbullet, (
            self.rect.centerx - int(rotatedbullet.get_width() / 2),
            self.rect.centery - int(rotatedbullet.get_height() / 2)))


class Mine:
    def __init__(self, position):
        self.surf = pygame.Surface((16, 16))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
        self.rect.center = position
        self.mine = pygame.image.load("assets/mine.png").convert_alpha()
        self.active = True
        self.damage = stats.level // 2
        self.sound = pygame.mixer.Sound("assets/shell.wav")
        self.aoerect = pygame.Rect(self.rect.centerx - stats.shellaoe, self.rect.centery - stats.shellaoe,
                                   stats.shellaoe * 2,
                                   stats.shellaoe * 2)

    def update(self, dt):
        pass

    def draw(self, screen):
        # draw the mine
        screen.blit(self.mine, self.rect)
