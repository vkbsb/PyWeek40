__pragma__ ('skip')
document = window = Math = Date = 0 # Prevent complaints by optional static checker
PIXI = 0
__pragma__ ('noskip')

from com.pixi import PIXI
from com.vkgd.common.scene import Scene
from com.vkgd.common.constants import *

class GameOverScreen(Scene):
    def __init__(self, rootStage):        
        Scene.__init__(self, rootStage)
        self.graphics = PIXI.Graphics()
        self.stage.addChild(self.graphics)
        self.time = 0

    def drawScene(self, dt):
        self.graphics.js_clear()
        # TODO: Add game over screen graphics here
        pass

    def update(self, dt):
        self.drawScene(dt)
    
    def onEvent(self, e_name, params):
        print(f"GameOver event: {e_name}: {params}")

    def showScore(self, score):
        # TODO: Add method to display final score
        pass

    def showRestartButton(self):
        # TODO: Add method to show restart button
        pass