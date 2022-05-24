from background import *
from levelcontroller import LevelController
from gui import StartGUI, GameOverGUI
import time
import pygame
import random
import stats


from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
)


def main():
    # Framerate Independent
    pygame.init()
    clock = pygame.time.Clock()
    prev_time = time.time()

    # Define constants for the screen width and height
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600

    # Set up the drawing window and screen shake
    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen = window.copy()
    bordercolor = (0, 0, 0)

    # Set up music
    pygame.mixer.init()
    pygame.mixer.music.load("assets/shellhell.wav")
    pygame.mixer.music.set_volume(0.7)
    pygame.mixer.music.play(-1)

    # Create Instances
    levelcontroller = LevelController()
    background = Background()
    pygame.mouse.set_visible(False)
    cursor = pygame.image.load("assets/cursor.png").convert_alpha()
    state = 0
    offset = [0, 0]
    startmenu = StartGUI()
    gameover = GameOverGUI()
    highscore = 0
    currentscore = 0

    # Run until the user asks to quit
    running = True
    while running:
        # delta time and FPS
        clock.tick(60)
        now = time.time()
        dt = (now - prev_time) * 60
        prev_time = now
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == pygame.QUIT:
                running = False

        # Start Menu
        if not state:
            startmenu.draw(screen)
            if pygame.mouse.get_pressed(3)[0]:
                state = 1
        # Game
        elif state == 1:
            levelcontroller.update(dt)
            if levelcontroller.playerhealth <= 0:
                if highscore < stats.level:
                    highscore = stats.level
                currentscore = stats.level
                levelcontroller.restart()
                gameover.update(highscore, currentscore)
                state = 2
            if levelcontroller.player.shellshake:
                levelcontroller.player.shellshake -= dt
                offset = [random.randint(0, 10) - 5, random.randint(0, 10) - 5]
                if levelcontroller.player.shellshake <= 0:
                    levelcontroller.player.shellshake = 0
            if levelcontroller.player.hurtshake:
                levelcontroller.player.hurtshake -= dt
                offset = [random.randint(0, 16) - 8, random.randint(0, 16) - 8]
                if levelcontroller.player.hurtshake <= 0:
                    levelcontroller.player.hurtshake = 0

            # Draw Background
            background.draw(screen)

            # Draw Content
            levelcontroller.draw(screen)

            # Draw border
            pygame.draw.rect(screen, bordercolor, (0, 0, 16, SCREEN_HEIGHT))
            pygame.draw.rect(screen, bordercolor, (SCREEN_WIDTH - 16, 0, 16, SCREEN_HEIGHT))
            pygame.draw.rect(screen, bordercolor, (0, 0, SCREEN_WIDTH, 12))
            pygame.draw.rect(screen, bordercolor, (0, SCREEN_HEIGHT - 12, SCREEN_WIDTH, 12))

        # Game Over Screen
        elif state == 2:
            gameover.draw(screen)
            if pygame.mouse.get_pressed(3)[0]:
                state = 1

        # Draw screen
        window.blit(screen, offset)
        offset = [0, 0]
        window.blit(cursor, (pygame.mouse.get_pos()[0] - 7.5, pygame.mouse.get_pos()[1] - 7.5))

        # Flip the display
        pygame.display.flip()

    pygame.quit()
