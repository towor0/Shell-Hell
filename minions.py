import pygame


class Minion(pygame.sprite.Sprite):
    def __init__(self, enid):
        super(Minion, self).__init__()
        self.surf = pygame.Surface((16, 16))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
        self.minion = pygame.image.load("assets/minion.png").convert_alpha()
        self.id = enid
        self.cd = 0

    def update(self, dt, prect):
        match self.id:
            case 0:
                self.rect.centerx = prect.centerx + 32
            case 1:
                self.rect.centerx = prect.centerx - 32
        self.rect.centery = prect.centery
        self.cd -= dt

    def draw(self, screen):
        screen.blit(self.minion, self.rect)
