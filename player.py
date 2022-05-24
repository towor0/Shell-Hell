from particles import ShellParticle, BulletParticle, PlayerTrailParticle, DamageCounter
from minions import Minion
from bullets import *
import stats

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

from pygame.locals import (
    K_w,
    K_a,
    K_s,
    K_d,
)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.direction = 0
        self.pointerdirection = 0
        self.surf = pygame.Surface((32, 32))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
        self.rect.topleft = [368, 268]
        self.pos = [368, 268]
        self.base = pygame.transform.scale(pygame.image.load("assets/playerbase.png").convert_alpha(), (20, 28))
        self.pointer = pygame.transform.scale(pygame.image.load("assets/playerpointer.png").convert_alpha(), (32, 32))
        self.bullets = []
        self.bulletParticles = []
        self.trailParticles = []
        self.currentshellcd = 0
        self.currentbulletcd = 0
        self.shellshake = 0
        self.hurtshake = 0
        self.shoot = pygame.mixer.Sound("assets/shoot.wav")
        self.hurtsound = pygame.mixer.Sound("assets/hurt.wav")
        self.invincibletime = 0
        self.trailcd = 0
        self.minions = []
        self.counters = []
        self.minecd = 300

    def reset(self):
        self.rect.topleft = [368, 268]
        self.pos = [368, 268]
        self.minions = []
        self.bullets = []

    # hurt player
    def hurt(self):
        self.invincibletime = 120
        self.hurtshake = 5
        self.hurtsound.play()

    # update object location
    def update(self, dt, enemies):
        vel = [0, 0]
        # move player if key pressed
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_a]:
            self.direction += stats.rotationspeed * dt
            if self.direction > 360:
                self.direction = self.direction % 360
        if pressed_keys[K_d]:
            self.direction += -stats.rotationspeed * dt
            if self.direction < 0:
                self.direction = self.direction + 360
        if pressed_keys[K_w]:
            ds = directionSpeed(self.direction, stats.speed)
            vel[0] = (ds[0])
            vel[1] = (-ds[1])
            if self.trailcd <= 0:
                self.trailParticles.append(PlayerTrailParticle(self.rect.center))
                self.trailcd = 10/stats.speed
                self.trailcd = 10/stats.speed
        if pressed_keys[K_s]:
            ds = directionSpeed(self.direction, stats.speed)
            vel[0] = -ds[0]
            vel[1] = ds[1]
            if self.trailcd <= 0:
                self.trailParticles.append(PlayerTrailParticle(self.rect.center))
                self.trailcd = 10/stats.speed
        self.base.get_rect(center=self.rect.center)
        # add velocity
        self.pos[0] += vel[0] * dt
        self.pos[1] += vel[1] * dt
        # Keep player on the screen
        if self.pos[0] < 16:
            self.pos[0] = 16
        if self.pos[0] + 32 > SCREEN_WIDTH - 16:
            self.pos[0] = SCREEN_WIDTH - 48
        if self.pos[1] < 12:
            self.pos[1] = 12
        if self.pos[1] + 32 > SCREEN_HEIGHT - 12:
            self.pos[1] = SCREEN_HEIGHT - 44
        # commit velocity
        self.rect.x = int(self.pos[0])
        self.rect.y = int(self.pos[1])
        # turns the pointer
        self.pointerdirection = getAngle(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], self.rect.centerx,
                                         self.rect.centery)
        # spawn shell & bullet
        if pygame.mouse.get_pressed(3)[0]:
            if self.currentshellcd <= 0:
                self.shoot.play()
                self.bullets.append(Shell(self.rect.center, self.pointerdirection))
                self.currentshellcd = stats.shellcd
        if pygame.mouse.get_pressed(3)[2]:
            if self.currentbulletcd <= 0:
                self.bullets.append(Bullet(self.rect.center, self.pointerdirection + (random.randint(0, stats.accuracy*10)/10
                                                                                      - (stats.accuracy / 2))))
                self.currentbulletcd = stats.bulletcd
        # checks shells & bullets
        if self.minecd <= 0 and stats.mine:
            self.minecd = 90
            self.bullets.append(Mine(self.rect.center))
        for bullet in self.bullets:
            bullet.update(dt)
            for enemy in enemies:
                if enemy.rect.colliderect(bullet.rect):
                    if isinstance(bullet, MinionBullet):
                        self.counters.append(DamageCounter(enemy.rect.center, bullet.damage, (0, 255, 0)))
                        enemy.hurt(bullet, dt)
                    elif isinstance(bullet, Mine):
                        pass
                    else:
                        self.counters.append(DamageCounter(enemy.rect.center, bullet.damage, (255, 255, 0)))
                        enemy.hurt(bullet, dt)
                    bullet.active = False

        # check counters
        for counter in self.counters:
            counter.update(dt)
        for counter in self.counters:
            if counter.time <= 0:
                self.counters.remove(counter)
        # creates particle for shells & bullets + area damage for some bullets
        for bullet in self.bullets:
            if not bullet.active:
                temp = bullet
                self.bullets.remove(bullet)
                temp.sound.play()
                if isinstance(temp, Bullet):
                    for _ in range(10):
                        self.bulletParticles.append(BulletParticle(temp.rect.center, temp.direction))
                elif isinstance(temp, Shell):
                    self.shellshake = 15
                    # area damage to enemy
                    for enemy in enemies:
                        if enemy.rect.colliderect(temp.aoerect):
                            self.counters.append(DamageCounter(enemy.rect.center, stats.shellareadamage, (255, 100, 0)))
                            enemy.hurt(temp, dt)
                    for _ in range(50):
                        self.bulletParticles.append(ShellParticle(temp.rect.center, stats.shellaoe / 32))
                elif isinstance(temp, MinionBullet):
                    for _ in range(10):
                        self.bulletParticles.append(MinionBulletParticle(temp.rect.center))
                elif isinstance(temp, Mine):
                    for enemy in enemies:
                        if enemy.rect.colliderect(temp.aoerect):
                            self.counters.append(DamageCounter(enemy.rect.center, bullet.damage, (255, 100, 0)))
                            enemy.hurt(temp, dt)
                    for _ in range(50):
                        self.bulletParticles.append(ShellParticle(temp.rect.center, stats.shellaoe / 32))
        # check particles
        for particle in self.bulletParticles:
            particle.update(dt)
        for particle in self.bulletParticles:
            if particle.time < 0:
                self.bulletParticles.remove(particle)
        for particle in self.trailParticles:
            particle.update(dt)
        for particle in self.trailParticles:
            if particle.time < 0:
                self.trailParticles.remove(particle)
        # check minions
        if len(self.minions) < stats.minion:
            self.minions.append(Minion(len(self.minions)))
        for minion in self.minions:
            minion.update(dt, self.rect)
            if minion.cd <= 0:
                minion.cd += 15
                if enemies:
                    closest = enemies[0]
                    for enemy in enemies:
                        if getDistance(closest.rect.center, minion.rect.center) > getDistance(enemy.rect.center, minion.rect.center):
                            closest = enemy
                    self.bullets.append(MinionBullet(minion.rect.center, getAngle(closest.rect.x, closest.rect.y, minion.rect.x, minion.rect.y)))
        # manage cooldown
        if self.currentshellcd > 0:
            self.currentshellcd -= dt
        if self.currentbulletcd > 0:
            self.currentbulletcd -= dt
        if self.invincibletime > 0:
            self.invincibletime -= dt
        if self.trailcd > 0:
            self.trailcd -= dt
        if self.minecd > 0:
            self.minecd -= dt

    def draw(self, screen):
        # draw the trail particle
        for particle in self.trailParticles:
            particle.draw(screen)
        # draw the bullets sent by the tank
        for bullet in self.bullets:
                bullet.draw(screen)
        # draw the base of the tank
        rotatedbase = pygame.transform.rotate(self.base, self.direction)
        rotatedptr = pygame.transform.rotate(self.pointer, self.pointerdirection)
        if self.invincibletime > 0:
            rotatedbase.set_alpha(128)
            rotatedptr.set_alpha(128)
        screen.blit(rotatedbase, (
            self.rect.centerx - int(rotatedbase.get_width() / 2),
            self.rect.centery - int(rotatedbase.get_height() / 2)))
        # draw minions
        for minion in self.minions:
            minion.draw(screen)
        # draw the cannon of the tank
        screen.blit(rotatedptr, (
            self.rect.centerx - int(rotatedptr.get_width() / 2), self.rect.centery - int(rotatedptr.get_height() / 2)))
        # draw the bullet particle
        for particle in self.bulletParticles:
            particle.draw(screen)
        # draw counters
        for counter in self.counters:
            counter.draw(screen)
