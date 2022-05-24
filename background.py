import pygame
import random


class Background:
    def __init__(self):
        self.rect = pygame.rect.Rect(16, 12, 768, 576)
        self.grounds = []
        self.groundimages = [
            pygame.image.load("assets/ground1.png").convert_alpha(),
            pygame.image.load("assets/ground2.png").convert_alpha(),
        ]
        for x in range(48):
            for y in range(36):
                self.grounds.append(random.randint(0, 1))

    def draw(self, screen):
        for x in range(48):
            for y in range(36):
                screen.blit(self.groundimages[self.grounds[x * y]], (x * 16 + 16, y * 16 + 12))
