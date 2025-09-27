__pragma__ ('skip')
document = window = Math = Date = 0 # Prevent complaints by optional static checker
PIXI = 0
__pragma__ ('noskip')

from com.pixi import PIXI
from com.vkgd.splash import LoadingScreen
from com.vkgd.gameplay import GameplayScreen
from com.vkgd.common.constants import *
from com.vkgd.Game2048 import Game2048
from com.vkgd.assets import ASSETS

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

        #load assets
        PIXI.loader.add(ASSETS)

        PIXI.loader.load(self.onAssetsLoaded)

        #schedule update for the game loop.    
        PIXI.Ticker.shared.add(self.update)
        
        # Register once
        window.addEventListener('resize', self.onResize)
        window.addEventListener('touchstart', self.onTouchStart)
        window.addEventListener('mousedown', self.onMouseDown)
        window.addEventListener('keydown', self.onKeyDown)

    def onKeyDown(self, e):
        if self.screen != None and hasattr(self.screen, 'game'):
            direction = None
            if e.key == 'ArrowLeft':
                direction = Game2048.move_left
            elif e.key == 'ArrowRight':
                direction = Game2048.move_right
            elif e.key == 'ArrowUp':
                direction = Game2048.move_up
            elif e.key == 'ArrowDown':
                direction = Game2048.move_down
            if direction != None:
                self.screen.onEvent(EVENT_MOVE, direction)
            e.preventDefault()


    def onMouseDown(self, e):
        x = int((e.clientX - self.rootStage.x)/self.scale)
        y = int((e.clientY - self.rootStage.y)/self.scale)
        # print(f"x:{x}, y:{y}, rx:{self.rootStage.x}, ry:{self.rootStage.y}")
        e.preventDefault()

        #send the x,y in the design resolution space with origin at center of screen.
        self.screen.onEvent(EVENT_MOUSEDOWN, (x,y))

    def onTouchStart(self, e):
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


    def onAssetsLoaded(self, resources):
        #create gameplay screen for the game.
        self.screen.cleanup()
        print("StageChildren: ", self.rootStage.children.length)
        self.screen = GameplayScreen(self.rootStage)

    def update(self, dt):
        self.screen.update(dt)
        if isinstance(self.screen, GameplayScreen):
            if self.screen.isComplete():
                self.screen.cleanup()
                self.screen = GameOverScreen(self.rootStage)
        PIXI.tweenManager.js_update()