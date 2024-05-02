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
                self.GAME.instantiate_projectile(self.x + self.SIZE//2,
                                                 self.y,
                                                 0)
                self.cooldown = self.COOLDOWN

    def draw(self):
        pyxel.rect(self.x, self.y, self.SIZE, self.SIZE, 11)


class Projectile:
    def __init__(self, x, y, team):
        self.team = team
        self.x = x
        self.y = y

    def tick(self):
        self.y -= 1

    def draw(self):
        pyxel.rect(self.x, self.y, 1, 3, 11)


class Game:
    def __init__(self):
        pyxel.init(128, 128, title="Obamium Survivor")

        self.player = Player(self)
        self.projectiles = []

        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btn(pyxel.KEY_ESCAPE):
            pyxel.quit()

        self.player.tick()
        for projectile in self.projectiles:
            projectile.tick()

    def draw(self):
        pyxel.cls(0)

        self.player.draw()
        for projectile in self.projectiles:
            projectile.draw()

    def instantiate_projectile(self, x, y, team):
        """Instantiate a projectile at the desired coordinates

        :param x:
        :param y:
        :return:
        """
        projectile = Projectile(x, y, team)
        self.projectiles.append(projectile)


if __name__ == '__main__':
    Game()
