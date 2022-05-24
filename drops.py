import pygame


class Health(pygame.sprite.Sprite):
    def __init__(self, position):
        super(Health, self).__init__()
        self.surf = pygame.Surface((16, 16))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
        self.rect.center = position
        self.health = []
        self.time = 15 * 60
        for i in range(10):
            self.health.append(pygame.image.load(f"assets/healthanimation/health{i}.png").convert_alpha())
        self.frame = 0
        self.sound = pygame.mixer.Sound("assets/heal.wav")

    def update(self, dt):
        self.time -= dt
        if self.frame == 9:
            self.frame = 0
        else:
            self.frame += 1

    def draw(self, screen):
        screen.blit(self.health[self.frame], self.rect)
