import pyxel


class Player:
    def __init__(self):
        self.SIZE = 10
        self.SPEED = 2

        self.x = 30
        self.y = 30

    def update(self):
        self.handle_movement()

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
        

    def draw(self):
        pyxel.cls(0)
        pyxel.rect(self.x, self.y, self.SIZE, self.SIZE, 11)


class Game:
    def __init__(self):
        pyxel.init(128, 128, title="Obamium Survivor")

        self.player = Player()

        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btn(pyxel.KEY_ESCAPE):
            pyxel.quit()
        self.player.update()

    def draw(self):
        self.player.draw()


if __name__ == '__main__':
    Game()