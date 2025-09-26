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
                value = self.game.board[r][c]
                color = 0xcccccc if value == 0 else 0xffcc00
                self.graphics.beginFill(color)
                self.graphics.drawRect(x, y, cellSize - 5, cellSize - 5)
                self.graphics.endFill()

                if(value != 0):
                    self.textDisplay[r][c].text = str(value)
                    self.textDisplay[r][c].visible = True
                    #place the text at the right place.
                    self.textDisplay[r][c].x = x + cellSize / 2 - self.textDisplay[r][c].width / 2
                    self.textDisplay[r][c].y = y + cellSize / 2 - self.textDisplay[r][c].height  + 6
                else:
                    self.textDisplay[r][c].visible = False

    def update(self, dt):
        PIXI.tweenManager.js_update()
        pass

    def getPosition(self, r, c):
        cellSize = 128
        offsetX = (DESIGN_WIDTH - self.game.size * cellSize) / 2
        offsetY = (DESIGN_HEIGHT - self.game.size * cellSize) / 2
        x = offsetX + c * cellSize
        y = offsetY + r * cellSize
        return (x, y)

    def createBlock(self, r, c, value):
        # Placeholder for creating a new block graphic
        graphics = PIXI.Graphics()
        (x, y) = self.getPosition(r, c)
        graphics.x = x
        graphics.y = y
        color = 0xffcc00
        graphics.beginFill(color)
        graphics.drawRect(0, 0, cellSize - 5, cellSize - 5)
        graphics.endFill()

        self.stage.addChild(graphics)
        return graphics
        
    def animateBoard(self, merged_coords):
        # Placeholder for animation logic
        for mc in merged_coords:
            print(f"Merged at: {mc}")
            #create a new graphics object to animate for each merged coordinate
            if(mc.type == 'move'):
                r, c = mc.source
                value = mc.value
                block = self.createBlock(r, c, value)

                r, c = mc.end
                (tx,ty) = self.getPosition(r, c)

                # After animation, remove the block (in real case, you would update the existing block)
                def onComplete():
                    print("Deleting.`")
                    self.stage.removeChild(block)
                blockTween = PIXI.tweenManager.createTween(block)
                blockTween.js_from({'x':block.x, 'y':block.y}).to({'x':tx, 'y':ty})
                blockTween.time = 300
                blockTween.on('end', onComplete)
                blockTween.start()
        # self.drawGrid()
        pass

    def onEvent(self, e_name, params):
        if e_name == EVENT_MOVE:
            direction = params
            if direction in [Game2048.move_left, Game2048.move_right, Game2048.move_up, Game2048.move_down]:
                self.game.display_board()
                (moved, score_added, merged_coords) = self.game.move(direction)
                if moved:
                    self.animateBoard(merged_coords)
                    # print(f"Move: {direction}, Moved: {moved}, Score Added: {score_added}, Merged: {merged_coords}")
                    # self.game.add_random_tile()
                    # self.drawGrid()                
                self.game.display_board()

    def isComplete(self):
        return False