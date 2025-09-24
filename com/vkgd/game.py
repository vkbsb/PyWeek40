__pragma__ ('skip')
document = window = Math = Date = 0 # Prevent complaints by optional static checker
PIXI = 0
__pragma__ ('noskip')

from com.pixi import PIXI
from com.vkgd.splash import LoadingScreen
from com.vkgd.common.constants import *

class Game:
    def __init__(self):
        container = document.getElementById("app")
        app = PIXI.Application({
            'antialias': True,
            'autoDensity': True,
            'resizeTo':container,
        })

        self.gameOver = False
        self.app = app
        container.appendChild(app.view)

        #setup root stage with the right scaling.
        self.rootStage = PIXI.Container()
        self.app.stage.addChild(self.rootStage)
        self.onResize()

        #create loading screen for the game.
        self.screen = LoadingScreen(self.rootStage) 
        PIXI.loader.load(self.onAssetsLoaded)

        #schedule update for the game loop.    
        PIXI.Ticker.shared.add(self.update)
        
        # Register once
        window.addEventListener('resize', self.onResize)
        window.addEventListener('touchstart', self.onMouseDown)

    def onMouseDown(self, e):
        touch = e.changedTouches[0]
        x = int((touch.clientX - self.rootStage.x)/self.scale)
        y = int((touch.clientY - self.rootStage.y)/self.scale)
        # print(f"x:{x}, y:{y}, rx:{self.rootStage.x}, ry:{self.rootStage.y}")
        e.preventDefault()

        #send the x,y in the design resolution space with origin at center of screen.
        self.screen.onEvent(EVENT_MOUSEDOWN, (x,y))


    def onResize(self):
        app = self.app
        viewW = app.renderer.width
        viewH = app.renderer.height
        scale = Math.min(viewW/DESIGN_WIDTH, viewH/DESIGN_HEIGHT)
        self.scale = scale
        self.rootStage.scale.set(scale, scale)

        #Center world with letterboxing
        worldWidth = DESIGN_WIDTH * scale
        worldHeight = DESIGN_HEIGHT * scale

        print(scale, viewW, DESIGN_WIDTH, worldWidth, worldHeight)
        self.rootStage.x = (viewW - worldWidth) / 2
        self.rootStage.y = (viewH - worldHeight) / 2


    def onAssetsLoaded(self):
        pass
        # #self.player.addChild()
        # self.screen.cleanup()
        # print("StageChildren: ", self.app.stage.children.length)
        # self.screen = GameOverScreen(self.app.stage)

    def update(self, dt):
        self.screen.update(dt)
        PIXI.tweenManager.js_update()