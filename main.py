import pyxel


class Player:
    def __init__(self):
        self.SIZE = 10
        self.x = 30
        self.y = 30

    def update(self):
        self.x+=1

    def draw(self):
        pyxel.cls(0)
        pyxel.rect(self.x, self.y, self.SIZE, self.SIZE, 11)


class Game:
    def __init__(self):
        pyxel.init(128, 128, title="Obamium Survivor")

        self.player = Player()

        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btn(pyxel.KEY_Q):
            pyxel.quit()
        self.player.update()

    def draw(self):
        self.player.draw()


if __name__ == '__main__':
    Game()