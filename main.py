import math
import random
from typing import List

import pyxel


class Player:
    def __init__(self, game):
        """

        :param game: The "Game" object
        """
        self.GAME = game
        self.SIZE = 10
        self.SPEED = 2
        self.COOLDOWN = 10

        self.x = 30
        self.y = 30

        self.cooldown = 0

    def tick(self):
        self.handle_movement()
        self.handle_attack()

    def handle_movement(self):
        x, y = 0, 0

        if pyxel.btn(pyxel.KEY_Z):
            y -= 1
        elif pyxel.btn(pyxel.KEY_S):
            y += 1
        if pyxel.btn(pyxel.KEY_D):
            x += 1
        elif pyxel.btn(pyxel.KEY_Q):
            x -= 1

        self.x += x * self.SPEED
        self.y += y * self.SPEED

    def handle_attack(self):
        if self.cooldown > 0:
            self.cooldown -= 1

        if pyxel.btnr(pyxel.KEY_SPACE):
            if self.cooldown <= 0:
                self.GAME.instantiate_projectile(self.x,
                                                 self.y,
                                                 0)
                self.cooldown = self.COOLDOWN

    def draw(self):
        pyxel.rect(self.x - self.SIZE // 2,
                   self.y - self.SIZE // 2,
                   self.SIZE,
                   self.SIZE,
                   11)


class Projectile:
    def __init__(self, x, y, team, game):
        """Instantiate a projectile at the desired coordinates

        :param x:
        :param y:
        :param team: The projectile's team: 0 for the player, 1 for the monsters
        :param game: The "Game" object
        """
        self.GAME = game
        self.team = team
        self.x = x
        self.y = y

    def tick(self):
        self.y -= 1

        if self.y <= -10:
            self.GAME.projectiles.remove(self)

    def draw(self):
        pyxel.rect(self.x, self.y, 1, 3, 11)


class Spawner:
    """The monster spawner

    """

    def __init__(self, game):
        """

        :param game: The "Game" object
        """
        self.GAME = game
        self.COOLDOWN_MIN = 50
        self.COOLDOWN_MAX = 100

        self.cooldown = 0

    def tick(self):
        self.cooldown -= 1

        if self.cooldown <= 1:
            self.cooldown = random.randint(self.COOLDOWN_MIN, self.COOLDOWN_MAX)
            self.spawn_ennemy()

    def spawn_ennemy(self):
        x = random.randint(10, 110)
        self.GAME.instantiate_monster(x, 0)


class Monster:
    def __init__(self, x, y, game):
        """Instantiate a projectile at the desired coordinates

        :param x:
        :param y:
        :param game: The "Game" object
        """
        self.GAME = game
        self.SIZE = 16

        self.x = x
        self.y = y

    def tick(self):
        self.y += 1

        if self.y >= 130:
            self.GAME.monsters.remove(self)

        # Collisions
        # Bullets
        for projectile in self.GAME.projectiles:
            if self.check_collision(projectile.x, projectile.y):
                self.GAME.projectiles.remove(projectile)
                self.GAME.monsters.remove(self)
                return
        # Player
        print("Checking collisions")
        if self.check_collision(self.GAME.player.x, self.GAME.player.x):
            self.GAME.game_over()

    def check_collision(self, x, y):
        """Checks the collision with the specified projectile

        :param x:
        :param y:
        :return:
        """
        x_diff = self.x - x
        y_diff = self.y - y
        diff = math.sqrt(x_diff ** 2 + y_diff ** 2)
        return diff < self.SIZE

    def draw(self):
        pyxel.rect(self.x - self.SIZE // 2,
                   self.y - self.SIZE // 2,
                   self.SIZE, self.SIZE,
                   10)


class Game:
    def __init__(self):
        pyxel.init(128, 128, title="Obamium Survivor")

        self.running = True

        self.player = Player(self)
        self.projectiles: List[Projectile] = []

        self.spawner = Spawner(self)
        self.monsters: List[Monster] = []

        pyxel.run(self.update, self.draw)

    def update(self):
        if self.running:
            if pyxel.btn(pyxel.KEY_ESCAPE):
                pyxel.quit()

            self.player.tick()

            for projectile in self.projectiles:
                projectile.tick()

            self.spawner.tick()

            for monster in self.monsters:
                monster.tick()

    def draw(self):
        pyxel.cls(0)

        self.player.draw()

        for projectile in self.projectiles:
            projectile.draw()

        for monster in self.monsters:
            monster.draw()

    def instantiate_projectile(self, x, y, team):
        """Instantiate a projectile at the desired coordinates

        :param x:
        :param y:
        :param team: The projectile's team: 0 for the player, 1 for the monsters
        :return:
        """
        projectile = Projectile(x, y, team, self)
        self.projectiles.append(projectile)

    def instantiate_monster(self, x, y):
        """Instantiate a projectile at the desired coordinates

        :param x:
        :param y:
        :return:
        """
        monster = Monster(x, y, self)
        self.monsters.append(monster)

    def game_over(self):
        """Ends the game

        """
        self.running = False


if __name__ == '__main__':
    Game()
