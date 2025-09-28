__pragma__ ('skip')
document = window = Math = Date = 0 # Prevent complaints by optional static checker
PIXI = 0
__pragma__ ('noskip')

from com.pixi import PIXI
from com.vkgd.common.scene import Scene
from com.vkgd.common.constants import *
from com.vkgd.Game2048 import Game2048
from com.vkgd.assets import *
from com.howler import PyHowl

cellSize = 128

cellSizeX = 128 + 48
cellSizeY = 128 + 48
gapSize = 5

class GameplayScreen(Scene):
    def __init__(self, rootStage):
        Scene.__init__(self, rootStage)
        self.game = Game2048()
        self.gameOver = False
        self.score = 0

        self.graphics = PIXI.Graphics()
        self.stage.addChild(self.graphics)

        mymap = PIXI.Sprite(PIXI.Texture.js_from("map"))
        mymap.x = (DESIGN_WIDTH/2)
        mymap.y = (DESIGN_HEIGHT/2)
        mymap.anchor.x = 0.5
        mymap.anchor.y = 0.5
        self.stage.addChild(mymap)
        
        self.disableInput = False
        self.textDisplay = []
        self.imgDisplay = []

        self.sounds = {}
        for sfx_files in SFX_FILES:
            name = sfx_files['name']
            url = sfx_files['url']
            self.sounds[name] = PyHowl({"src":url, "preload": True})

        for r in range(self.game.size):
            row = []
            imRow = []
            for c in range(self.game.size):
                spr = PIXI.Sprite()
                spr.visible = False
                imRow.append(spr)
                self.stage.addChild(spr)

                text = PIXI.BitmapText("", FONT_CONFIG)
                text.visible = False
                row.append(text)
                self.stage.addChild(text)

            self.imgDisplay.append(imRow)
            self.textDisplay.append(row)
        self.drawGrid()

    def drawGrid(self):
        # self.graphics.js_clear()
        self.graphics.lineStyle(2, 0x000000)
        offsetX = (DESIGN_WIDTH - self.game.size * cellSizeX) / 2
        offsetY = (DESIGN_HEIGHT - self.game.size * cellSizeY) / 2

        for r in range(self.game.size):
            for c in range(self.game.size):
                x = offsetX + c * cellSizeX
                y = offsetY + r * cellSizeY
                value = self.game.board[r][c]
                color = 0xcccccc if value == 0 else 0xffcc00
                # self.graphics.beginFill(color)
                # self.graphics.drawRect(x, y, cellSizeX - gapSize, cellSizeY - gapSize)
                # self.graphics.endFill()

                if(value != 0):
                    self.textDisplay[r][c].text = str(value)
                    # self.textDisplay[r][c].visible = True
                    #place the text at the right place.
                    self.textDisplay[r][c].x = x + cellSizeX / 2 - self.textDisplay[r][c].width / 2
                    self.textDisplay[r][c].y = y + cellSizeY / 2 - self.textDisplay[r][c].height  + 6

                    tex = PIXI.Texture.js_from(str(value))
                    self.imgDisplay[r][c].texture = tex
                    self.imgDisplay[r][c].visible = True
                    self.imgDisplay[r][c].x = x + (cellSizeX - gapSize)/2
                    self.imgDisplay[r][c].y = y + (cellSizeY - gapSize)/2
                    self.imgDisplay[r][c].anchor.x = 0.5
                    self.imgDisplay[r][c].anchor.y = 1
                    self.imgDisplay[r][c].width = tex.width
                    self.imgDisplay[r][c].height = tex.height
                    print(f"Set image {value} at ({r},{c}) to size {tex.width}x{tex.height}")
                    # self.imgDisplay[r][c].scale = 1
                
                else:
                    self.textDisplay[r][c].visible = False
                    self.imgDisplay[r][c].visible = False

    def update(self, dt):
        PIXI.tweenManager.js_update()
        pass

    def getPosition(self, r, c):
        offsetX = (DESIGN_WIDTH - self.game.size * cellSizeX) / 2
        offsetY = (DESIGN_HEIGHT - self.game.size * cellSizeY) / 2
        x = offsetX + c * cellSizeX
        y = offsetY + r * cellSizeY

        x = x + (cellSizeX - gapSize)/2
        y = y + (cellSizeY - gapSize)/2 
        return (x, y)

    def createBlock(self, r, c, value):
        # Placeholder for creating a new block graphic
        graphics = PIXI.Sprite(PIXI.Texture.js_from(str(value)))
        (x, y) = self.getPosition(r, c)
        graphics.x = x
        graphics.y = y
        print(f"Creating block {value} at ({r},{c}) -> ({x},{y})")

        self.stage.addChild(graphics)
        return graphics
    
    def onAnimationFinished(self):
        self.disableInput = False
        self.drawGrid()

    def onSlideAnimationFinished(self):
        self.drawGrid()

        #if there was no slide anymation, do not add a new tile.
        if not self.anyslide:
            self.onAnimationFinished()
            return

        if self.anymerge:
            self.sounds["merge"].play()

        new_tile_info = self.game.add_random_tile()
        if new_tile_info:
            r, c, value = new_tile_info
            print(f"New tile {value} at ({r},{c})")
            block = self.createBlock(r, c, value)

            def onCompleted(block):
                return lambda: self.stage.removeChild(block)

            (tx, ty) = self.getPosition(r, c)
            block.x = tx
            block.y = ty
            block.scale.x = 0.1
            block.scale.y = 0.1

            blockTween = PIXI.tweenManager.createTween(block.scale)
            blockTween.js_from({'x': 0.1, 'y':0.1}).to({'x':1, 'y': 1})
            blockTween.time = 100
            blockTween.on('end', onCompleted(block))
            blockTween.start()
            window.setTimeout(self.onAnimationFinished, 120)
        elif self.game.game_over:
            self.onGameOver()

        
    def handleMoveAnimation(self, mc):
        sr, sc = mc.source
        er, ec = mc.end
        value = mc.value
        block = self.createBlock(sr, sc, value)
        (tx,ty) = self.getPosition(er, ec)
        (sx, sy) = self.getPosition(sr, sc)

        # print(f"Reset: {sx}, {sy}")
        # #hide the block at current position and animate to new position
        # self.graphics.beginFill(0xcccccc)
        # self.graphics.drawRect(sx, sy, cellSizeX - gapSize, cellSizeY - gapSize)
        # self.graphics.endFill()
        # self.textDisplay[sr][sc].visible = False

        def onCompleted(block):
            return lambda: self.stage.removeChild(block)

        blockTween = PIXI.tweenManager.createTween(block)
        blockTween.js_from({'x':block.x, 'y':block.y}).to({'x':tx, 'y':ty})
        blockTween.time = 100
        blockTween.on('end', onCompleted(block))
        blockTween.start()

    def animateSlide(self, merged_coords):
        self.anyslide = False
        self.disableInput = True
        self.anymerge = False
        for mc in merged_coords:
            print(f"Type: {mc.js_type}, Source: {mc.source}, End: {mc.end}, Value: {mc.value}")
            #create a new graphics object to animate for each merged coordinate
            if(mc.js_type == 'move'):
                sr, sc = mc.source
                er, ec = mc.end
                value = mc.value

                #skip the animationi if source and end are same
                if(sr == er and sc == ec):
                    continue

                self.anyslide = True
                self.handleMoveAnimation(mc)
            elif(mc.js_type == 'merge'):
                #for merge, we will animate both the source and end blocks.
                (sr, sc) = mc.sources[1]
                er, ec = mc.end
                value = mc.value
                if(sr == er and sc == ec):
                    (sr, sc) = mc.sources[0]
                self.anyslide = True
                self.anymerge = True
                new_mc = {"value": value, "source": (sr, sc), "end": (er, ec)}
                self.handleMoveAnimation(new_mc)

        if self.anyslide:
            self.sounds["swish"].play()  
        #redraw the grid after animation
        window.setTimeout(self.onSlideAnimationFinished, 120)

    def onEvent(self, e_name, params):
        if e_name == EVENT_MOUSEDOWN:
            if self.gameOver:
                window.location.reload()
                return
        elif e_name == EVENT_MOVE:
            if self.disableInput:
                return

            if self.game._check_game_over():        
                self.onGameOver()

            direction = params
            if direction in [Game2048.move_left, Game2048.move_right, Game2048.move_up, Game2048.move_down]:
                self.game.display_board()
                (moved, score_added, merged_coords) = self.game.move(direction)

                self.score += score_added
                if moved:
                    self.animateSlide(merged_coords)
                    print(f"Move: {direction}, Moved: {moved}, Score Added: {score_added}, Merged: {merged_coords}")
                    # self.game.add_random_tile()
                    # self.drawGrid()    
                self.game.display_board()

    def onGameOver(self):
        print("Game Over!")
        self.disableInput = True
        window.score = self.score
        self.gameOver = True

        graphics = PIXI.Graphics()
        graphics.beginFill(0x000000, 0.7)
        graphics.drawRect(0, 0, DESIGN_WIDTH, DESIGN_HEIGHT)
        graphics.endFill()


        txt = PIXI.BitmapText("Game Over!", HEADER_FONT_CONFIG)
        txt.x = (DESIGN_WIDTH - txt.width)/2
        txt.y = (DESIGN_HEIGHT - txt.height)/2 - 100
        graphics.addChild(txt)
        
        scoretxt = PIXI.BitmapText(f"Score: {self.score}", FONT_CONFIG)
        scoretxt.x = (DESIGN_WIDTH - scoretxt.width)/2
        scoretxt.y = (DESIGN_HEIGHT - scoretxt.height)/2 + 20
        graphics.addChild(scoretxt)

        restarttxt = PIXI.BitmapText("Click / Tap to Restart", FONT_CONFIG)
        restarttxt.x = (DESIGN_WIDTH - restarttxt.width)/2
        restarttxt.y = (DESIGN_HEIGHT - restarttxt.height)/2 + 250
        graphics.addChild(restarttxt)

        self.stage.addChild(graphics)
        Tween = PIXI.tweenManager.createTween(graphics)
        Tween.js_from({'alpha': 0}).to({'alpha': 0.7})
        Tween.time = 500
        Tween.start()

    def isComplete(self):
        return False #self.gameOver