import pygame
import random

from pygame.locals import (
    K_LEFT,
    K_RIGHT,
    K_RETURN,
)


class LevelGUI:
    def __init__(self):
        # Set up fonts
        self.levelfont = pygame.font.Font("assets/Cave-Story.ttf", 200)
        self.healthicon = pygame.transform.scale(pygame.image.load("assets/healthicon.png").convert_alpha(), (64, 64))
        self.nohealthicon = pygame.transform.scale(pygame.image.load("assets/nohealthicon.png").convert_alpha(),
                                                   (64, 64))
        self.healthicon.set_alpha(128)
        self.nohealthicon.set_alpha(128)

    def draw(self, screen, level, health):
        leveltext = self.levelfont.render(str(level), True, (0, 0, 0))
        leveltext.set_alpha(128)
        screen.blit(leveltext, (
            800 / 2 - leveltext.get_rect().width / 2, 600 / 2 - leveltext.get_rect().height / 2))
        for i in range(4):
            if i in range(health):
                screen.blit(self.healthicon, (32 + i * 64, 450))
            else:
                screen.blit(self.nohealthicon, (32 + i * 64, 450))


class UpgradeGUI:
    def __init__(self):
        self.active = False
        self.allupgrades = {
            "None": pygame.transform.scale(
                pygame.image.load("assets/upgrades/None.png").convert_alpha(), (128, 128)),
            "+ Bullet Firerate": pygame.transform.scale(
                pygame.image.load("assets/upgrades/+bulletfirerate.png").convert_alpha(), (128, 128)),
            "+ Shell Firerate": pygame.transform.scale(
                pygame.image.load("assets/upgrades/+shellfirerate.png").convert_alpha(), (128, 128)),
            "+ Movement Speed": pygame.transform.scale(
                pygame.image.load("assets/upgrades/+movementspeed.png").convert_alpha(), (128, 128)),
            "+ Rotation Speed": pygame.transform.scale(
                pygame.image.load("assets/upgrades/+rotationspeed.png").convert_alpha(), (128, 128)),
            "+ Bullet Damage": pygame.transform.scale(
                pygame.image.load("assets/upgrades/+bulletdamage.png").convert_alpha(), (128, 128)),
            "+ Shell Damage": pygame.transform.scale(
                pygame.image.load("assets/upgrades/+shelldamage.png").convert_alpha(), (128, 128)),
            "+ Bullet Accuracy": pygame.transform.scale(
                pygame.image.load("assets/upgrades/+bulletaccuracy.png").convert_alpha(), (128, 128)),
            "+ Shell AOE": pygame.transform.scale(
                pygame.image.load("assets/upgrades/+shellaoe.png").convert_alpha(), (128, 128)),
            "+ Shell AOE Damage": pygame.transform.scale(
                pygame.image.load("assets/upgrades/+shellaoedamage.png").convert_alpha(), (128, 128)),
            "+ Health Drop Rate": pygame.transform.scale(
                pygame.image.load("assets/upgrades/+healthdroprate.png").convert_alpha(), (128, 128)),
            "+ Minion": pygame.transform.scale(
                pygame.image.load("assets/upgrades/+minion.png").convert_alpha(), (128, 128)),
            "+ Mine": pygame.transform.scale(
                pygame.image.load("assets/upgrades/+mine.png").convert_alpha(), (128, 128)),
        }
        self.upgradefont = pygame.font.Font("assets/Cave-Story.ttf", 15)
        self.titlefont = pygame.font.Font("assets/Cave-Story.ttf", 50)
        self.select = pygame.transform.scale(pygame.image.load("assets/selectupgrade.png").convert_alpha(), (128, 128))
        self.upgradesname = [name for name in self.allupgrades.keys()][1:]
        self.upgrades = []
        self.upgradesrect = [
            pygame.Rect(178, 236, 128, 128),
            pygame.Rect(336, 236, 128, 128),
            pygame.Rect(494, 236, 128, 128)
        ]
        self.background = pygame.image.load("assets/upgrademenu.png").convert_alpha()
        self.background.set_alpha(200)
        self.upgradeselected = ""
        self.selection = 1
        self.selectioncd = 0
        self.selectsfx = pygame.mixer.Sound("assets/select.wav")
        self.upgradesfx = pygame.mixer.Sound("assets/upgrade.wav")

    def refresh(self):
        self.active = True
        self.upgrades = []
        if len(self.upgradesname) >= 3:
            for _ in range(3):
                tempupgrade = self.upgradesname[random.randint(0, len(self.upgradesname) - 1)]
                while tempupgrade in self.upgrades:
                    tempupgrade = self.upgradesname[random.randint(0, len(self.upgradesname) - 1)]
                self.upgrades.append(tempupgrade)
            self.upgradeselected = self.upgrades[1]
            self.selection = 1
        elif len(self.upgradesname) == 2:
            self.upgrades.append(self.upgradesname[0])
            self.upgrades.append("None")
            self.upgrades.append(self.upgradesname[1])
            self.selection = 0
        elif len(self.upgradesname) == 1:
            self.upgrades.append("None")
            self.upgrades.append(self.upgradesname[0])
            self.upgrades.append("None")
            self.selection = 1
        else:
            self.active = False

    def update(self, level, dt):
        if self.active:
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[K_RIGHT] and self.selection < 2 and self.selectioncd <= 0:
                if len(self.upgradesname) >= 3:
                    self.selection += 1
                    self.selectsfx.play()
                elif len(self.upgradesname) == 2:
                    self.selection += 2
                    self.selectsfx.play()
                self.selectioncd += 10
            if pressed_keys[K_LEFT] and self.selection > 0 and self.selectioncd <= 0:
                if len(self.upgradesname) >= 3:
                    self.selection -= 1
                    self.selectsfx.play()
                elif len(self.upgradesname) == 2:
                    self.selection -= 2
                    self.selectsfx.play()
                self.selectioncd += 10
            if self.selectioncd > 0:
                self.selectioncd -= dt
            self.upgradeselected = self.upgrades[self.selection]
            if pressed_keys[K_RETURN]:
                self.active = False
                self.upgradesfx.play()

    def draw(self, screen):
        if self.active:
            screen.blit(self.background, (0, 0))
            titletext = self.titlefont.render("Upgrades", True, (255, 255, 255))
            screen.blit(titletext, (
                400 - titletext.get_rect().width / 2,
                200 - titletext.get_rect().height / 2))
            for i in range(3):
                screen.blit(self.allupgrades[self.upgrades[i]], self.upgradesrect[i])
                if i == self.selection:
                    upgradetext = self.upgradefont.render(str(self.upgrades[i]), True, (255, 255, 255))
                    screen.blit(upgradetext, (
                        self.upgradesrect[i].x + 64 - upgradetext.get_rect().width / 2,
                        384 - upgradetext.get_rect().height / 2))
                    screen.blit(self.select, self.upgradesrect[i])
                else:
                    upgradetext = self.upgradefont.render(str(self.upgrades[i]), True, (0, 0, 0))
                    screen.blit(upgradetext, (
                        self.upgradesrect[i].x + 64 - upgradetext.get_rect().width / 2,
                        384 - upgradetext.get_rect().height / 2))


class StartGUI:
    def __init__(self):
        self.titlefont = pygame.font.Font("assets/Cave-Story.ttf", 200)
        self.startfont = pygame.font.Font("assets/Cave-Story.ttf", 50)
        self.background = pygame.image.load("assets/startmenubackground.png")

    def draw(self, screen):
        titletext = self.titlefont.render("Shell Hell", True, (255, 255, 255))
        starttext = self.startfont.render("Click to Start", True, (255, 255, 255))
        screen.blit(self.background, (0, 0))
        screen.blit(titletext, (100, 150))
        screen.blit(starttext, (287, 400))


class GameOverGUI:
    def __init__(self):
        self.titlefont = pygame.font.Font("assets/Cave-Story.ttf", 200)
        self.continuefont = pygame.font.Font("assets/Cave-Story.ttf", 50)
        self.scorefont = pygame.font.Font("assets/Cave-Story.ttf", 50)
        self.background = pygame.image.load("assets/startmenubackground.png")
        self.hs = 0
        self.cs = 0

    def update(self, hs, cs):
        self.hs = hs
        self.cs = cs

    def draw(self, screen):
        titletext = self.titlefont.render("Game Over", True, (255, 255, 255))
        highscoretext = self.scorefont.render(f"High Score: {self.hs}", True, (255, 255, 255))
        currentscoretext = self.scorefont.render(f"Score: {self.cs}", True, (255, 255, 255))
        continuetext = self.continuefont.render("Click to Retry", True, (255, 255, 255))
        screen.blit(self.background, (0, 0))
        screen.blit(titletext, (800 / 2 - titletext.get_rect().width / 2, 150))
        screen.blit(highscoretext, (800 / 2 - highscoretext.get_rect().width / 2, 300))
        screen.blit(currentscoretext, (800 / 2 - currentscoretext.get_rect().width / 2, 350))
        screen.blit(continuetext, (800 / 2 - continuetext.get_rect().width / 2, 450))
