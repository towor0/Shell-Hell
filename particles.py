import pygame
import random
from helper import *


class ShellParticle:
    def __init__(self, position, size):
        self.vel = [random.randint(0, 200) / 20 - 5, random.randint(0, 200) / 20 - 5]
        self.time = random.randint(10, 20)
        self.surf = pygame.Surface((self.time, self.time))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
        self.rect.center = position
        self.size = size

    def update(self, dt):
        self.rect.move_ip(self.vel[0] * dt * self.size, self.vel[1] * dt * self.size)
        self.time -= dt

    def draw(self, screen):
        pygame.draw.circle(screen, (255, random.randint(0, 255), 0), self.rect.topleft, self.time * self.size)


class BulletParticle:
    def __init__(self, position, angle):
        self.vel = directionSpeed((angle + 180) + (random.randint(0, 90) - 45), random.randint(2, 5))
        self.time = random.randint(2, 5)
        self.surf = pygame.Surface((self.time, self.time))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
        self.rect.center = position
        self.angle = angle

    def update(self, dt):
        self.rect.move_ip(self.vel[0] * dt, -self.vel[1] * dt)
        self.time -= dt

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 0), self.rect.topleft, self.time)


class MinionBulletParticle:
    def __init__(self, position):
        self.vel = [random.randint(0, 200) / 20 - 5, random.randint(0, 200) / 20 - 5]
        self.time = random.randint(10, 20)
        self.surf = pygame.Surface((self.time, self.time))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
        self.rect.center = position

    def update(self, dt):
        self.rect.move_ip(self.vel[0] * dt, self.vel[1] * dt)
        self.time -= dt

    def draw(self, screen):
        pygame.draw.circle(screen, (0, 255, 0), self.rect.topleft, self.time//4)


class EnemyDeathParticle(pygame.sprite.Sprite):
    def __init__(self, position):
        super(EnemyDeathParticle, self).__init__()
        self.vel = [random.randint(0, 200) / 20 - 5, random.randint(0, 200) / 20 - 5]
        self.time = random.randint(5, 8)
        self.surf = pygame.Surface((self.time, self.time))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
        self.rect.center = position

    def update(self, dt):
        self.rect.move_ip(self.vel[0] * dt, self.vel[1] * dt)
        self.time -= dt

    def draw(self, screen):
        pygame.draw.circle(screen, (0, 0, 0), self.rect.topleft, self.time * 2)


class PlayerTrailParticle:
    def __init__(self, position):
        self.pos = [int(position[0]), int(position[1])]
        self.time = 8
        self.surf = pygame.Surface((self.time, self.time))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
        self.rect.center = self.pos

    def update(self, dt):
        self.time -= dt * 0.1
        self.rect.width = self.time
        self.rect.height = self.time
        self.rect.center = self.pos

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 100, 0), self.rect, int(self.time))


class DamageCounter:
    def __init__(self, position, damage, color):
        self.time = 8
        self.surf = pygame.Surface((self.time, self.time))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
        self.rect.center = position
        self.font = pygame.font.Font("assets/Cave-Story.ttf", 15)
        self.text = self.font.render(str(damage), True, color)
        self.color = color

    def update(self, dt):
        self.time -= dt * 0.2
        self.rect.y -= dt

    def draw(self, screen):
        screen.blit(self.text, (self.rect.x, self.rect.y))
