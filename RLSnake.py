import pygame, math, time, random, copy, multiprocessing, sys, json
import numpy as np
from pygame.locals import *

class Scoreboard:
    def __init__(self, game):
        """
        Create the scoreboard object
        """
        self.game = game

    def render(self, surface: pygame.Surface):
        """
        Print the score at the top of the game.
        """
        text = "Score: "+ str(round(self.game.snake.length, 2)).rjust(3)
        displayFont = pygame.font.Font(pygame.font.match_font("Consolas,Lucida Console,Mono,Monospace,Sans"), 20)
        textImage = displayFont.render(text, True, (255, 255, 255))
        surface.blit(textImage, pygame.Vector2(0, 0))

class Apple:
    def __init__(self,game):
        self.x = random.randint(0, game.dimensionX-1)
        self.y = random.randint(0, game.dimensionY-1)
        self.game = game
        self.color = (255,0,0)

    def isEated(self, Headposition):
        if Headposition[0] == self.x and Headposition[1] == self.y:
            return True

    def update(self,snake):
        if self.isEated(snake.bodyPosition[0]) :
            snake.grow(self)
            self.x = random.randint(0, self.game.dimensionX-1)
            self.y = random.randint(0, self.game.dimensionY-1)
        
    def render(self, surface: pygame.Surface):
        self.drawApple = pygame.draw.rect(surface, self.color,[self.x * self.game.tileSize , self .y * self.game.tileSize , self.game.tileSize , self.game.tileSize])

class Snake:
    def __init__(self,game):
        self.game = game
        self.bodyPosition = [[game.dimensionX/2,game.dimensionY/2]]
        self.lastBodyPosition = None
        self.moveSpeed = 30
        self.color = (0,255,0)
        self.dirX = 1
        self.dirY = 0
        self.length = 0
        
    def changeDir(self, direction):
        if direction == "LEFT":
            self.dirX = -1
            self.dirY = 0
        if direction == "RIGHT":
            self.dirX = 1
            self.dirY = 0
        if direction == "DOWN":
            self.dirX = 0
            self.dirY = 1
        if direction == "UP":
            self.dirX = 0
            self.dirY = -1

    def grow(self, apple):
        self.bodyPosition.append([apple.x,apple.y])
        self.length += 1

    def colide(self):
        if self.bodyPosition[0][0]<0 or self.bodyPosition[0][0] == self.game.dimensionX or self.bodyPosition[0][1]<0 or self.bodyPosition[0][1] == self.game.dimensionY:
            return True
        for position in self.lastBodyPosition:
            if self.bodyPosition[0][0] == position[0] and self.bodyPosition[0][1] == position[1] :
                return True

    def update(self):
        self.lastBodyPosition = copy.deepcopy(self.bodyPosition[1:])
        for i in range(self.length):
            self.bodyPosition[self.length-i][0] = self.bodyPosition[self.length-1-i][0]
            self.bodyPosition[self.length-i][1] = self.bodyPosition[self.length-1-i][1]
        self.bodyPosition[0][0] += self.dirX
        self.bodyPosition[0][1] += self.dirY

    def render(self, surface: pygame.Surface):
        for bodyPart in self.bodyPosition:
            pygame.draw.rect(surface,self.color,[bodyPart[0] * self.game.tileSize , bodyPart[1] * self.game.tileSize , self.game.tileSize-1 , self.game.tileSize-1])

class snakeGame:
    def __init__(self):
        self.color = (0,0,0)
        self.dimensionX = 40
        self.dimensionY = 40
        self.tileSize = 10
        self.specimen = None
        self.doRender = True
        self.isPlaying = True
        self.score = 0
        self.snake = Snake(self)
        self.apple = Apple(self)
        self.scoreboard = Scoreboard(self)

    def check_events(self):
        event = pygame.event.poll()
        while(event.type != NOEVENT):
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.snake.changeDir("LEFT")
                if event.key == pygame.K_RIGHT:
                    self.snake.changeDir("RIGHT")
                if event.key == pygame.K_DOWN:
                    self.snake.changeDir("DOWN")
                if event.key == pygame.K_UP:
                    self.snake.changeDir("UP")
            if(event.type == QUIT):
                exit()
            event = pygame.event.poll()

    def update(self,dt = 0):
        self.snake.update()
        self.apple.update(self.snake)
    
    def render(self, surface: pygame.Surface):
        self.snake.render(surface)
        self.apple.render(surface)
        self.scoreboard.render(surface)

    def check_collisions(self):
        if self.snake.colide():
            self.isPlaying = False
 
    def run(self, specimen=None,doRender=True):
        #self.specimen = specimen
        #self.doRender = doRender

        if doRender:
            renderSurface = pygame.display.get_surface()
        else:
            renderSurface = None
        count = 0

        while (self.isPlaying):
            if doRender:
                self.check_events()

            self.update()
            self.check_collisions()
            
            if self.doRender:
                self.render(renderSurface)
                pygame.display.flip()
                pygame.display.get_surface().fill((0, 0, 0))
                clock.tick(10+(self.snake.length/4))
            count += 1
            

        return self.snake.length
            

if __name__ == "__main__":
    pygame.init()
    args = sys.argv[1:]
    clock = pygame.time.Clock()
    pygame.display.set_mode((400,400))
    game = snakeGame()
    print("Score: ", game.run())