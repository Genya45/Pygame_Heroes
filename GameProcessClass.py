import pygame
import random
import os
from EnemyAsteroidClass import EnemyAsteroid
from UserClass import User

class MainGame():
    

    def __init__(self, win, imageBackgroundSpace):        
        self.win = win        
        self.imageBackgroundSpace = imageBackgroundSpace
        self.isRunMainLoop = True

        
        self.__FONT_PATH__ = 'assets/fonts/solid.ttf'
        self.font = None

        
        self.__IMG_PATH_ASTEROIDS__ = "assets/images/asteroids/" 
        self.enemyAsteroidTicks = 0
        self.enemyAsteroidTicksMax = 100
        self.enemyAsteroidList = []
        self.asteroidsListImages = []

        self.isStartGame = False
        self.isCloseGame = False


        self.bitWinX = self.win.get_size()[0]/20

        self.user1 = User(self.bitWinX * 5 - 5, self.win.get_size()[1]/2, self.win.get_size()[0],
        self.win.get_size()[1], 0)
        self.user2 = User(self.bitWinX * 15 + 5, self.win.get_size()[1]/2, self.win.get_size()[0],
        self.win.get_size()[1], 0)

        self.score = 0
        
        self.imageLoader()
        self.fontLoader()     


    def imageLoader(self):        
        for imageAsteroid in os.listdir(self.__IMG_PATH_ASTEROIDS__):       
            asteroidImage = pygame.image.load(self.__IMG_PATH_ASTEROIDS__ + imageAsteroid)
            self.asteroidsListImages.append(asteroidImage)

    def fontLoader(self):
        self.font = pygame.font.Font(self.__FONT_PATH__, 50)


    
    def enemyAsteroidUpdated(self):
        self.enemyAsteroidTicks += 1

        

        if self.enemyAsteroidTicks >= self.enemyAsteroidTicksMax:
            self.enemyAsteroidTicks = 0
            numberImage = random.randint(1, len(self.asteroidsListImages)-1)
            self.enemyAsteroidList.append(EnemyAsteroid(self.win.get_size()[0], self.win.get_size()[1], self.asteroidsListImages[numberImage], self.asteroidsListImages[numberImage]) )
            self.enemyAsteroidList[-1].image = pygame.transform.scale(self.enemyAsteroidList[-1].image, (self.enemyAsteroidList[-1].radius*2, self.enemyAsteroidList[-1].radius*2))
            
        for indexAsteroid, enemyAsteroid in enumerate(self.enemyAsteroidList):
            enemyAsteroid.update_position()       
            self.win.blit(enemyAsteroid.image, (enemyAsteroid.posX - enemyAsteroid.radius, enemyAsteroid.posY - enemyAsteroid.radius))

            if enemyAsteroid.isBorderOut() and len(self.enemyAsteroidList):
                self.enemyAsteroidList.pop(indexAsteroid)
                continue


        

    def eventTest(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.isRunMainLoop = False
                self.isCloseGame = True
                pygame.mixer.music.stop()
                break
            if event.type == pygame.KEYDOWN:                        
                if event.key == pygame.K_ESCAPE:
                    self.isRunMainLoop = False
                    self.isCloseGame = True
                    pygame.mixer.music.stop()
                    break
                if event.key == pygame.K_RETURN:
                    self.isRunMainLoop = False
                    self.isStartGame = True
                    pygame.mixer.music.stop()
                    break


    def updateBackgroundImage(self):
        self.win.blit(self.imageBackgroundSpace, (0, 0))

    def selectMenu(self):
        text = 'USER 1 20'
        fontScoreDisplay = self.font.render(text , False, (0, 255, 0))
        position = []
        position.append(self.win.get_size()[0]*0.25 - self.font.size(text)[0]/2)
        position.append(self.win.get_size()[1]*0.1)        
        pygame.draw.rect(self.win, (2, 2, 2), (position[0]-5, position[1]-5, self.font.size(text)[0]+10, self.font.size(text)[1]+5)) 
        self.win.blit(fontScoreDisplay, position) 
        
        text = 'USER 2 175'
        fontScoreDisplay = self.font.render(text , False, (0, 255, 0))
        position = []
        position.append(self.win.get_size()[0]*0.75 - self.font.size(text)[0]/2)
        position.append(self.win.get_size()[1]*0.1) 
        pygame.draw.rect(self.win, (2, 2, 2), (position[0]-5, position[1]-5, self.font.size(text)[0]+10, self.font.size(text)[1]+5)) 
        self.win.blit(fontScoreDisplay, position) 






    def updateDisplay(self):
        self.updateBackgroundImage()
        self.selectMenu()   
        self.enemyAsteroidUpdated()
        pygame.display.update()
        
    def main_process_update(self):
        self.eventTest()
        self.updateDisplay()


if __name__ == "__main__":
    print("It is not a main module")