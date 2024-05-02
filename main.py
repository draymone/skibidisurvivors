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
        self.COOLDOWN = 24
        self.health = 3

        # The number of canons
        self.canon_count = 1
        # The number of bullet fired per canon
        self.bullet_count = 1

        self.x = 60
        self.y = 90

        self.level = 0
        self.skillpoints = 0
        self.xp = 1

        self.cooldown = 0

        # load images
        pyxel.load("PYXEL_RESOURCE_FILE.pyxres")

    def tick(self):
        self.handle_movement()
        self.handle_attack()
        self.handle_levelup()

    def handle_movement(self):
        if pyxel.btn(pyxel.KEY_Z):
            if self.y > 5:
                self.y -= 1
        elif pyxel.btn(pyxel.KEY_S):
            if self.y < 100:
                self.y += 1
        if pyxel.btn(pyxel.KEY_D):
            if self.x < 125:
                self.x += 1
        elif pyxel.btn(pyxel.KEY_Q):
            if self.x > 5:
                self.x -= 1

    def handle_attack(self):
        if self.cooldown > 0:
            self.cooldown -= 1

        if pyxel.btnr(pyxel.KEY_SPACE):
            if self.cooldown <= 0:
                self.cooldown = self.COOLDOWN

                for x in range(-self.canon_count//2, self.canon_count//2):
                    for y in range(0, self.bullet_count):
                        self.GAME.instantiate_projectile(self.x + 3*x,
                                                         self.y + 4*y,
                                                         0)

    def handle_levelup(self):
        if pyxel.btnr(pyxel.KEY_1):
            self.levelup_skill(0)
        elif pyxel.btnr(pyxel.KEY_2):
            self.levelup_skill(1)
        elif pyxel.btnr(pyxel.KEY_3):
            self.levelup_skill(2)
        elif pyxel.btnr(pyxel.KEY_4):
            self.levelup_skill(3)

    def levelup_skill(self, i):
        if self.skillpoints >= 1:
            self.skillpoints -= 1

        if i == 0:
            self.canon_count += 1
        elif i == 1:
            self.bullet_count += 1
        elif i == 2:
            pass
            #TODO: explosive boulets
        elif i == 3:
            self.COOLDOWN *= 0.8

    def draw(self):

        pyxel.blt(self.x - self.SIZE // 2,
                  self.y - self.SIZE // 2,
                  0,
                  48,
                  160,
                  8,
                  8,
                  5)

    def draw_ui(self):
        # Bar
        pyxel.rect(0, 113, 128, 15, 1)

        # Life bar
        pyxel.rect(10, 117, 24, 8, 0)
        pyxel.rect(10, 117, self.health*8, 8, 7)

        # Skill points
        pyxel.text(80, 118, str(self.skillpoints), 3)

    def damage(self):
        """Reduces the health by 1

        :return:
        """
        self.health -= 1
        if self.health <= 0:
            self.GAME.game_over()

    def xp_up(self, amount=1):
        self.xp -= amount
        if self.xp <= 0:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.skillpoints += 1
        self.xp += 3*self.level


class Projectile:
    def __init__(self, x, y, team, game):
        """Instantiate a projectile at the desired coordinates

        :param x:
        :param y:
        :param team: The projectile's team: 0 for the player, 1 for the monsters
        :param game: The "Game" object
        """
        self.GAME = game

        self.SPEED = 2

        self.team = team
        self.x = x
        self.y = y

    def tick(self):
        self.y -= self.SPEED

        if self.y <= -10:
            self.GAME.projectiles.remove(self)

    def draw(self):
        pyxel.rect(self.x, self.y, 1, 3, 11)


def pick_number(weights):
    """Pick a random element from the list, they are weighted

    :param weights:
    :return:
    """
    total = sum(weights)

    roll = random.randint(0, total)
    for i in range(len(weights)):
        if roll <= weights[i]:
            return i
        roll -= weights[i]
    return 0


class Spawner:
    """The monster spawner

    """

    def __init__(self, game):
        """

        :param game: The "Game" object
        """
        self.GAME = game
        self.COOLDOWN_MIN = 3
        self.COOLDOWN_MAX = 5
        self.EVOLUTION_COOLDOWN = 150
        self.EVOLUTION_STRENGHT = 0.8

        self.spawn_weights = [100, 0, 0, 0, 0, 0, 0]
        self.cooldown = 0
        self.evolution_cooldown = self.EVOLUTION_COOLDOWN
        self.evolution_stage = 0

    def tick(self):
        self.cooldown -= 1
        self.evolution_cooldown -= 1

        if self.cooldown <= 0:
            self.cooldown = random.randint(self.COOLDOWN_MIN, self.COOLDOWN_MAX)
            self.spawn_ennemy()
        if self.evolution_cooldown <= 0:
            self.evolution_cooldown = self.EVOLUTION_COOLDOWN
            self.evolve()

    def spawn_ennemy(self):
        x = random.randint(0, 128)

        roll = pick_number(self.spawn_weights)

        # Mini skibidi
        if roll == 0:
            self.GAME.instantiate_monster(x,
                                          0)
        # Purple skibidi
        elif roll == 1:
            self.GAME.instantiate_monster(x,
                                          0,
                                          sprite_x=40,
                                          sprite_y=160,
                                          health=7)
        # Big skibidi
        elif roll == 2:
            self.GAME.instantiate_monster(x,
                                          0,
                                          size=16,
                                          sprite_x=0,
                                          sprite_y=152,
                                          speed=0.8,
                                          health=3)
        # Golden skibidi
        elif roll == 3:
            self.GAME.instantiate_monster(x,
                                          0,
                                          size=16,
                                          sprite_x=16,
                                          sprite_y=152,
                                          speed=0.8,
                                          health=3)
        # Farfadet skibidi
        elif roll == 4:
            self.GAME.instantiate_monster(x,
                                          0,
                                          size=16,
                                          sprite_x=0,
                                          sprite_y=168,
                                          health=3)
        # Priest skibidi
        elif roll == 5:
            self.GAME.instantiate_monster(x,
                                          0,
                                          size=16,
                                          sprite_x=16,
                                          sprite_y=168,
                                          health=15)
        # Mao skibidi
        elif roll == 6:
            self.GAME.instantiate_monster(x,
                                          0,
                                          size=16,
                                          sprite_x=32,
                                          sprite_y=168,
                                          speed=0.5,
                                          health=100)

    def evolve(self):
        self.evolution_stage += 1
        self.COOLDOWN_MIN = math.ceil(self.COOLDOWN_MIN * self.EVOLUTION_STRENGHT)
        self.COOLDOWN_MAX = math.ceil(self.COOLDOWN_MAX * self.EVOLUTION_STRENGHT)

        if self.evolution_stage == 10/5:
            self.spawn_weights[2] = 20
            self.spawn_weights[3] = 1
        elif self.evolution_stage == 30/5:
            self.spawn_weights[0] = 20
            self.spawn_weights[4] = 30
        elif self.evolution_stage == 45/5:
            self.spawn_weights[0] = 0
            self.spawn_weights[1] = 35
        elif self.evolution_stage == 60/5:
            self.spawn_weights[5] = 20
        elif self.evolution_stage == 90/5:
            self.spawn_weights = [0, 0, 0, 0, 0, 0, 100]

            # Stop future evolutions


            self.EVOLUTION_STRENGHT = 0


class Monster:
    def __init__(self, x, y, game, size=8, speed=1, health=1, sprite_x=32, sprite_y=160):
        """Instantiate a projectile at the desired coordinates

        :param x:
        :param y:
        :param game: The "Game" object
        """
        self.GAME = game

        self.size = size
        self.sx = sprite_x
        self.sy = sprite_y
        self.speed = speed
        self.health = health

        self.x = x
        self.y = y

    def tick(self):
        self.y += self.speed

        if self.y >= 130:
            self.GAME.monsters.remove(self)

        # Collisions
        # Bullets
        for projectile in self.GAME.projectiles:
            if self.check_collision(projectile.x, projectile.y):
                self.GAME.player.xp_up()
                self.GAME.projectiles.remove(projectile)
                self.damage()
                return
        # Player
        if self.check_collision(self.GAME.player.x, self.GAME.player.y):
            self.GAME.player.damage()
            self.damage()

    def damage(self):
        """Reduces the health by 1

        :return:
        """
        self.health -= 1
        if self.health <= 0:
            self.GAME.monsters.remove(self)

    def check_collision(self, x, y):
        """Checks the collision with the specified projectile

        :param x:
        :param y:
        :return:
        """
        x_diff = self.x - x
        y_diff = self.y - y
        diff = math.sqrt(x_diff ** 2 + y_diff ** 2)
        return diff < self.size

    def draw(self):
        pyxel.blt(self.x - self.size // 2,
                  self.y - self.size // 2,
                  0,
                  self.sx,
                  self.sy,
                  self.size,
                  self.size,
                  5)


class Game:
    def __init__(self):
        pyxel.init(128, 128, title="Obamium Survivor")

        self.running = True
        self.pause_text = "PAUSE"

        self.player = Player(self)
        self.projectiles: List[Projectile] = []

        self.spawner = Spawner(self)
        self.monsters: List[Monster] = []

        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnr(pyxel.KEY_P):
            self.running = not self.running

        if self.running:
            self.player.tick()

            for projectile in self.projectiles:
                projectile.tick()

            self.spawner.tick()

            for monster in self.monsters:
                monster.tick()

    def draw(self):
        pyxel.cls(5)

        self.player.draw()

        for projectile in self.projectiles:
            projectile.draw()

        for monster in self.monsters:
            monster.draw()

        self.player.draw_ui()

        self.draw_pause()

    def draw_pause(self):
        if not self.running:
            pyxel.text(55, 55, self.pause_text, 4)

    def instantiate_projectile(self, x, y, team):
        """Instantiate a projectile at the desired coordinates

        :param x:
        :param y:
        :param team: The projectile's team: 0 for the player, 1 for the monsters
        :return:
        """
        projectile = Projectile(x, y, team, self)
        self.projectiles.append(projectile)

    def instantiate_monster(self, x, y, *, size=8, speed=1, health=1, sprite_x=32, sprite_y=160):
        """Instantiate a projectile at the desired coordinates

        :param x:
        :param y:
        :param size: the monster's size
        :param health:
        :param speed:
        :param sprite_x: The sprite's x coordinate
        :param sprite_y: The sprite's y coordinate
        :return:
        """
        monster = Monster(x, y, self, size, speed, health, sprite_x, sprite_y)
        self.monsters.append(monster)

    def game_over(self):
        """Ends the game

        """
        self.running = False
        self.pause_text = "GAME OVER"


if __name__ == '__main__':
    Game()
