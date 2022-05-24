from enemies import *
from particles import *
from drops import *
from player import Player
from gui import *
import stats


class LevelController:
    def __init__(self):
        self.invincible = []
        self.enemies = []
        self.enemyParticles = []
        self.drops = []
        self.levelcd = 120
        self.currentlevelcd = 0
        self.levelgui = LevelGUI()
        self.upgradegui = UpgradeGUI()
        self.playermaxhealth = 4
        self.playerhealth = self.playermaxhealth
        self.player = Player()

    def restart(self):
        self.levelgui = LevelGUI()
        self.upgradegui = UpgradeGUI()
        stats.reset()
        self.player.reset()
        self.playerhealth = self.playermaxhealth
        self.enemies = []
        self.drops = []

    def upgrade(self, upgrade):
        def removeupgrade():
            self.upgradegui.upgradesname.remove(upgrade)

        match upgrade:
            case "+ Bullet Firerate":
                stats.bulletcd -= 3.5
                if stats.bulletcd <= 1:
                    removeupgrade()
            case "+ Shell Firerate":
                stats.shellcd -= 25
                if stats.shellcd <= 20:
                    removeupgrade()
            case "+ Movement Speed":
                stats.speed += 1.5
                if stats.speed >= 8:
                    removeupgrade()
            case "+ Rotation Speed":
                stats.rotationspeed += 1
                if stats.rotationspeed >= 5:
                    removeupgrade()
            case "+ Bullet Damage":
                stats.bulletdamage += 3
                if stats.bulletdamage >= 13:
                    removeupgrade()
            case "+ Shell Damage":
                stats.shelldamage += 5
                if stats.shelldamage >= 25:
                    removeupgrade()
            case "+ Bullet Accuracy":
                stats.accuracy -= 2.5
                if stats.accuracy <= 0:
                    removeupgrade()
            case "+ Shell AOE":
                stats.shellaoe += 12
                if stats.shellaoe >= 80:
                    removeupgrade()
            case "+ Shell AOE Damage":
                stats.shellareadamage += 4
                if stats.shellareadamage >= 18:
                    removeupgrade()
            case "+ Health Drop Rate":
                stats.healthdroprate -= 3
                if stats.healthdroprate <= 8:
                    removeupgrade()
            case "+ Minion":
                stats.minion += 1
                if stats.minion >= 2:
                    removeupgrade()
            case "+ Mine":
                stats.mine = True
                removeupgrade()

    # set game level to the next one
    def nextLevel(self, prect):
        stats.level += 1
        count = stats.level
        if stats.level % 5 == 0:
            self.upgradegui.refresh()
        e3 = random.randint(0, count // 10)
        count -= e3 * 10
        e2 = random.randint(0, count // 5)
        count -= e2 * 5
        for _ in range(e3):
            self.invincible.append(Enemy3(enemySpawn(prect)))
        for _ in range(e2):
            self.invincible.append(Enemy2(enemySpawn(prect)))
        for _ in range(count):
            self.invincible.append(Enemy1(enemySpawn(prect)))
        self.currentlevelcd = self.levelcd

    def update(self, dt):
        if not self.upgradegui.active:
            if self.upgradegui.upgradeselected != "":
                self.upgrade(self.upgradegui.upgradeselected)
                self.upgradegui.upgradeselected = ""
            if self.currentlevelcd <= 0:
                # put take enemies out of self.invincible
                if self.invincible:
                    self.enemies = self.invincible
                    self.invincible = []
                # checks each enemy + enemy particle
                for enemy in self.enemies:
                    enemy.update(dt, self.player.rect)
                    if enemy.rect.colliderect(self.player.rect) and self.player.invincibletime <= 0:
                        self.player.hurt()
                        self.playerhealth -= 1
                    if not enemy.alive:
                        temp = enemy
                        self.enemies.remove(enemy)
                        if random.randint(1, stats.healthdroprate) == stats.healthdroprate:
                            self.drops.append(Health(temp.rect.center))
                        match type(enemy).__name__:
                            case "Enemy1":
                                for _ in range(10):
                                    self.enemyParticles.append(EnemyDeathParticle(temp.rect.center))
                            case "Enemy2":
                                for _ in range(10):
                                    self.enemyParticles.append(EnemyDeathParticle(temp.rect.center))
                # check particles
                for particle in self.enemyParticles:
                    particle.update(dt)
                for particle in self.enemyParticles:
                    if particle.time < 0:
                        self.enemyParticles.remove(particle)
                # set next level if there's no more enemy and particle
                if not self.enemies and not self.enemyParticles and not self.invincible:
                    self.nextLevel(self.player.rect)
            else:
                self.currentlevelcd -= dt
            # update drop
            for drop in self.drops:
                drop.update(dt)
                if drop.time <= 0:
                    self.drops.remove(drop)
            # checks if player is on drop
            for drop in self.drops:
                if self.player.rect.colliderect(drop.rect):
                    if type(drop).__name__ == "Health":
                        if self.playermaxhealth > self.playerhealth:
                            self.playerhealth += 1
                            drop.sound.play()
                            self.drops.remove(drop)

        # update upgrade gui
        self.upgradegui.update(stats.level, dt)
        # update player
        self.player.update(dt, self.enemies)

    def draw(self, screen):
        # draw guis
        self.levelgui.draw(screen, stats.level, self.playerhealth)
        # draw enemies and particles
        for enemy in self.enemies:
            enemy.draw(screen)
        for particle in self.enemyParticles:
            particle.draw(screen)
        for invincible in self.invincible:
            invincible.draw(screen, True)
        # draw drops
        for drop in self.drops:
            drop.draw(screen)
        # draw player
        self.player.draw(screen)
        # draw upgrade gui
        self.upgradegui.draw(screen)
