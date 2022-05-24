import pygame
import math
from helper import *
from bullets import *

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class Enemy1(pygame.sprite.Sprite):
    def __init__(self, pos):
        super(Enemy1, self).__init__()
        self.direction = 0
        self.speed = 2
        self.rect = pygame.Rect(pos[0], pos[1], 16, 16)
        self.enemy = pygame.transform.scale(pygame.image.load("assets/enemies/1.png").convert_alpha(), (16, 16))
        self.maxhealth = 6
        self.health = self.maxhealth
        self.alive = True

    # inflict damage to enemy
    def hurt(self, obj, dt):
        damage = obj.damage
        if hasattr(obj, 'areadamage'):
            damage += obj.areadamage
        if hasattr(obj, 'knockback'):
            vel = directionSpeed((obj.direction + 180), -obj.knockback)
            self.rect.move_ip(vel[0] * dt, -vel[1] * dt)
        self.health -= damage

    # update object location
    def update(self, dt, prect):
        self.direction = getAngle(prect.centerx, prect.centery, self.rect.centerx, self.rect.centery)
        vel = directionSpeed(self.direction, self.speed)
        self.rect.move_ip(vel[0] * dt, -vel[1] * dt)
        if self.health <= 0:
            self.alive = False

    def draw(self, screen, invincibility=False):
        if invincibility:
            self.enemy.set_alpha(128)
            screen.blit(self.enemy, self.rect)
        else:
            self.enemy.set_alpha(255)
            screen.blit(self.enemy, self.rect)
            pygame.draw.rect(screen, (255, 0, 0), (self.rect.x, self.rect.y - 7, self.rect.width, self.rect.width / 6))
            pygame.draw.rect(screen, (0, 255, 0), (
                self.rect.x, self.rect.y - 7, self.rect.width * (self.health / self.maxhealth), self.rect.width / 6))


class Enemy2(pygame.sprite.Sprite):
    def __init__(self, pos):
        super(Enemy2, self).__init__()
        self.direction = 0
        self.speed = 1.5
        self.rect = pygame.Rect(pos[0], pos[1], 16, 16)
        self.enemy = pygame.transform.scale(pygame.image.load("assets/enemies/2.png").convert_alpha(), (16, 16))
        self.maxhealth = 24
        self.health = self.maxhealth
        self.alive = True

    # inflict damage to enemy
    def hurt(self, obj, dt):
        damage = obj.damage
        if hasattr(obj, 'areadamage'):
            damage += obj.areadamage
        if hasattr(obj, 'knockback'):
            vel = directionSpeed((obj.direction + 180), -obj.knockback)
            self.rect.move_ip(vel[0] * dt, -vel[1] * dt)
        self.health -= damage

    # update object location
    def update(self, dt, prect):
        self.direction = getAngle(prect.centerx, prect.centery, self.rect.centerx, self.rect.centery)
        vel = directionSpeed(self.direction, self.speed)
        self.rect.move_ip(vel[0] * dt, -vel[1] * dt)
        if self.health <= 0:
            self.alive = False

    def draw(self, screen, invincibility=False):
        if invincibility:
            self.enemy.set_alpha(128)
            screen.blit(self.enemy, self.rect)
        else:
            self.enemy.set_alpha(255)
            screen.blit(self.enemy, self.rect)
            pygame.draw.rect(screen, (255, 0, 0), (self.rect.x, self.rect.y - 7, self.rect.width, self.rect.width / 6))
            pygame.draw.rect(screen, (0, 255, 0), (
                self.rect.x, self.rect.y - 7, self.rect.width * (self.health / self.maxhealth), self.rect.width / 6))


class Enemy3(pygame.sprite.Sprite):
    def __init__(self, pos):
        super(Enemy3, self).__init__()
        self.direction = 0
        self.speed = 1.5
        self.rect = pygame.Rect(pos[0], pos[1], 16, 16)
        self.enemy = pygame.transform.scale(pygame.image.load("assets/enemies/3.png").convert_alpha(), (16, 16))
        self.maxhealth = 24
        self.health = self.maxhealth
        self.alive = True

    # inflict damage to enemy
    def hurt(self, obj, dt):
        damage = obj.damage
        if hasattr(obj, 'areadamage'):
            damage += obj.areadamage
        if hasattr(obj, 'knockback'):
            vel = directionSpeed((obj.direction + 180), -obj.knockback)
            self.rect.move_ip(vel[0] * dt, -vel[1] * dt)
        self.health -= damage

    # update object location
    def update(self, dt, prect):
        self.direction = getAngle(prect.centerx, prect.centery, self.rect.centerx, self.rect.centery)
        vel = directionSpeed(self.direction, self.speed)
        self.rect.move_ip(vel[0] * dt, -vel[1] * dt)
        if self.health <= 0:
            self.alive = False

    def draw(self, screen, invincibility=False):
        if invincibility:
            self.enemy.set_alpha(128)
            screen.blit(self.enemy, self.rect)
        else:
            self.enemy.set_alpha(255)
            screen.blit(self.enemy, self.rect)
            pygame.draw.rect(screen, (255, 0, 0), (self.rect.x, self.rect.y - 7, self.rect.width, self.rect.width / 6))
            pygame.draw.rect(screen, (0, 255, 0), (
                self.rect.x, self.rect.y - 7, self.rect.width * (self.health / self.maxhealth), self.rect.width / 6))
