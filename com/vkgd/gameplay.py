__pragma__ ('skip')
document = window = Math = Date = 0 # Prevent complaints by optional static checker
PIXI = 0
__pragma__ ('noskip')

from com.pixi import PIXI
from com.vkgd.common.scene import Scene
from com.vkgd.common.constants import *
from com.vkgd.Game2048 import Game2048

class GameplayScreen(Scene):
    def __init__(self, rootStage):
        Scene.__init__(self, rootStage)
        self.game = Game2048()
        self.graphics = PIXI.Graphics()
        self.stage.addChild(self.graphics)
        self.drawGrid()

    def drawGrid(self):
        self.graphics.js_clear()
        self.graphics.lineStyle(2, 0x000000)
        cellSize = 128
        offsetX = (DESIGN_WIDTH - self.game.size * cellSize) / 2
        offsetY = (DESIGN_HEIGHT - self.game.size * cellSize) / 2

        for r in range(self.game.size):
            for c in range(self.game.size):
                x = offsetX + c * cellSize
                y = offsetY + r * cellSize
                value = self.game.grid[r][c]
                color = 0xcccccc if value == 0 else 0xffcc00
                self.graphics.beginFill(color)
                self.graphics.drawRect(x, y, cellSize - 5, cellSize - 5)
                self.graphics.endFill()

    def update(self, dt):
        pass

    def onEvent(self, e_name, params):
        if e_name == EVENT_MOVE:
            direction = params
            if direction in [Game2048.move_left, Game2048.move_right, Game2048.move_up, Game2048.move_down]:
                if self.game.move(direction):
                    self.game.add_random_tile()
                    print(f"Moved {direction}")
                    self.game.print_board()

    def isComplete(self):
        return False