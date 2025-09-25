__pragma__ ('skip')
document = window = Math = Date = 0 # Prevent complaints by optional static checker
PIXI = 0
__pragma__ ('noskip')

from com.pixi import PIXI
from com.vkgd.common.scene import Scene
from com.vkgd.common.constants import *
from com.vkgd.Game2048 import Game2048
from com.vkgd.assets import FONT_CONFIG

class GameplayScreen(Scene):
    def __init__(self, rootStage):
        Scene.__init__(self, rootStage)
        self.game = Game2048()
        self.graphics = PIXI.Graphics()
        self.stage.addChild(self.graphics)

        self.textDisplay = []
        for r in range(self.game.size):
            row = []
            for c in range(self.game.size):
                text = PIXI.BitmapText("", FONT_CONFIG)
                text.visible = False
                row.append(text)
                self.stage.addChild(text)
            self.textDisplay.append(row)
    

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

                if(value != 0):
                    self.textDisplay[r][c].text = str(value)
                    self.textDisplay[r][c].visible = True
                    self.textDisplay[r][c].x = x + cellSize / 2 - self.textDisplay[r][c].width / 2
                    self.textDisplay[r][c].y = y + cellSize / 2 - self.textDisplay[r][c].height / 2
                else:
                    self.textDisplay[r][c].visible = False

    def update(self, dt):
        pass

    def onEvent(self, e_name, params):
        if e_name == EVENT_MOVE:
            direction = params
            if direction in [Game2048.move_left, Game2048.move_right, Game2048.move_up, Game2048.move_down]:
                if self.game.move(direction):
                    self.game.spawn_block()
                    print(f"Moved {direction}")
                    # self.game.print_board()
                    self.drawGrid()

    def isComplete(self):
        return False