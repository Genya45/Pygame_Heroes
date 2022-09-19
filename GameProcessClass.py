import pygame
import random
import os
from EnemyAsteroidClass import EnemyAsteroid
from UserClass import User
from math import sin

class MainGame():
    

    def __init__(self, win, imageBackgroundSpace, isPrintUsersScore, username1, username2):        
        self.win = win        
        self.imageBackgroundSpace = imageBackgroundSpace
        self.isRunMainLoop = True
        
        self.isPrintUsersScore = isPrintUsersScore
        
        #self.__FONT_PATH__ = 'assets/fonts/solid.ttf'
        self.__FONT_PATH__ = 'assets/fonts/Lato-Black.ttf'
        self.__FONT_PATH_GAME_OVER__ = 'assets/fonts/Lato-Black.ttf'
        self.__FONT_PATH_PRESS_KEY__ = 'assets/fonts/Lato-Black.ttf'
        self.font = None
        self.username1 = username1
        self.username2 = username2     
        self.__TEXT_PRESS_ESC_TO_EXIT__ = 'НАЖМИТЕ ESC ЧТОБЫ ВЫЙТИ'
        self.__TEXT_USER_WIN__ = 'ПОБЕДИЛ '

        

        self.__SONG_SHOT_PATH__ = 'assets/sounds/Shot.mp3'
        self.songBoom = None
        self.__SONG_BOOM_PATH__ = 'assets/sounds/Crash.mp3'
        self.songGameOver = None
        self.__S0NG_GAME_OVER_PATH__ = 'assets/sounds/GameOver.mp3'

        
        self.__IMG_PATH_ASTEROIDS__ = "assets/images/asteroids/" 
        self.enemyAsteroidTicks = 0
        self.enemyAsteroidTicksMax = 100
        self.enemyAsteroidList = []
        self.asteroidsListImages = []

        self.isStartGame = False
        self.isCloseGame = False

        self.flagGameOverSong = False

        self.sinValueY = 0
        self.sinValue = 0
        self.sinValueMax = 62

        self.bitWinX = self.win.get_size()[0]/20


        self.__IMG_PATH_USER1__ = "assets/images/heroes/Hero1.png" 
        self.__IMG_PATH_USER2__ = "assets/images/heroes/Hero2.png" 
        self.__IMG_PATH_BOOM__ = "assets/images/asteroidsBoom/" 
        self.listBoomImages = []
        self.curImgBoom = 0
        self.curImgBoomIndex = 0

        #sizeUserX = self.win.get_size()[1]/7.68
        #sizeUserY = self.win.get_size()[1]/7.68
        sizeUserX = self.win.get_size()[1]/4
        sizeUserY = self.win.get_size()[1]/4

        self.user1 = User(self.bitWinX * 5 - 5 - sizeUserX, self.win.get_size()[1]/2 - sizeUserY/2,
            self.win.get_size()[0], self.win.get_size()[1], 0, sizeUserY, sizeUserX)
        self.user2 = User(self.bitWinX * 15 + 5, self.win.get_size()[1]/2 - sizeUserY/2,
            self.win.get_size()[0], self.win.get_size()[1], 0, sizeUserY, sizeUserX)

        self.score = 0
        self.SCORE_END_GAME = 5
        
        self.imageLoader()
        self.fontLoader()     
        self.songLoader()


    def imageLoader(self):        
        for imageAsteroid in os.listdir(self.__IMG_PATH_ASTEROIDS__):       
            asteroidImage = pygame.image.load(self.__IMG_PATH_ASTEROIDS__ + imageAsteroid)
            self.asteroidsListImages.append(asteroidImage)
        self.user1.image = pygame.image.load(self.__IMG_PATH_USER1__)
        self.user1.image = pygame.transform.scale(self.user1.image, (self.user1.width,self.user1.height))
        self.user2.image = pygame.image.load(self.__IMG_PATH_USER2__)
        self.user2.image = pygame.transform.scale(self.user2.image, (self.user2.width,self.user2.height))

        for imgBoom in os.listdir(self.__IMG_PATH_BOOM__):
            imgBoom = pygame.image.load(self.__IMG_PATH_BOOM__ + imgBoom)
            imgBoom = pygame.transform.scale(imgBoom, (self.user1.width,self.user1.height))
            self.listBoomImages.append(imgBoom)

    def songLoader(self):        
        self.songBoom = pygame.mixer.Sound(self.__SONG_BOOM_PATH__)
        self.songGameOver = pygame.mixer.Sound(self.__S0NG_GAME_OVER_PATH__)
        self.user1.songShot = pygame.mixer.Sound(self.__SONG_SHOT_PATH__)
        self.user2.songShot = pygame.mixer.Sound(self.__SONG_SHOT_PATH__)

    def fontLoader(self):
        self.font = pygame.font.Font(self.__FONT_PATH__, int(self.win.get_size()[1]/15.3))


    
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
                break
            if event.type == pygame.KEYDOWN:                        
                if event.key == pygame.K_ESCAPE:
                    self.isRunMainLoop = False
                    self.isCloseGame = True
                    break
                    
                if abs(self.user1.score - self.user2.score) != self.SCORE_END_GAME:
                    if event.key == pygame.K_1:
                        self.user1.score += 1
                        self.user1.songShot.play()
                    if event.key == pygame.K_2:
                        self.user2.score += 1
                        self.user2.songShot.play()


    def updateBackgroundImage(self):
        self.win.blit(self.imageBackgroundSpace, (0, 0))

    def printScore(self):
        text = self.username1 + ': ' + str(self.user1.score)
        fontScoreDisplay = self.font.render(text , False, (0, 255, 0))
        position = []
        position.append(self.win.get_size()[0]*0.25 - self.font.size(text)[0]/2)
        position.append(self.win.get_size()[1]*0.1)        
        pygame.draw.rect(self.win, (2, 2, 2), (position[0]-5, position[1]-5, self.font.size(text)[0]+10, self.font.size(text)[1]+5)) 
        self.win.blit(fontScoreDisplay, position) 
        
        text = self.username2 + ': ' + str(self.user2.score)
        fontScoreDisplay = self.font.render(text , False, (0, 255, 0))
        position = []
        position.append(self.win.get_size()[0]*0.75 - self.font.size(text)[0]/2)
        position.append(self.win.get_size()[1]*0.1) 
        pygame.draw.rect(self.win, (2, 2, 2), (position[0]-5, position[1]-5, self.font.size(text)[0]+10, self.font.size(text)[1]+5)) 
        self.win.blit(fontScoreDisplay, position) 

    def printUsers(self):
        #pygame.draw.rect(self.win, (255, 2, 2), (self.user1.posX, self.user1.posY,
        #    self.user1.width, self.user1.height))
        #pygame.draw.rect(self.win, (2, 2, 255), (self.user2.posX, self.user2.posY,
        #    self.user2.width, self.user2.height))
        if self.user1.score - self.user2.score == -self.SCORE_END_GAME:
            self.win.blit(self.listBoomImages[self.curImgBoom], (self.user1.posX, self.user1.posY + self.sinValueY))
            
            self.curImgBoomIndex += 1
            if self.curImgBoomIndex > 5:
                self.curImgBoomIndex = 0
                self.curImgBoom += 1
                if self.curImgBoom > len(self.listBoomImages)-1:
                    self.curImgBoom = 0
        else:
            self.win.blit(self.user1.image, (self.user1.posX, self.user1.posY + self.sinValueY))
        
        if self.user2.score - self.user1.score == -self.SCORE_END_GAME:
            self.win.blit(self.listBoomImages[self.curImgBoom], (self.user2.posX, self.user2.posY + self.sinValueY))
            
            self.curImgBoomIndex += 1
            if self.curImgBoomIndex > 5:
                self.curImgBoomIndex = 0
                self.curImgBoom += 1
                if self.curImgBoom > len(self.listBoomImages)-1:
                    self.curImgBoom = 0
        else:
            self.win.blit(self.user2.image, (self.user2.posX, self.user2.posY + self.sinValueY))

            
        widthScore1Line = self.bitWinX * (self.SCORE_END_GAME - (self.user2.score - self.user1.score))
        widthScore2Line = self.bitWinX * (self.SCORE_END_GAME - (self.user1.score - self.user2.score))
        widthScore1Line /= (self.SCORE_END_GAME/5)
        widthScore2Line /= (self.SCORE_END_GAME/5)
        pygame.draw.rect(self.win, (255, 2, 2), (self.bitWinX * 5, self.win.get_size()[1]/2 - 50 + self.sinValueY,
            widthScore1Line, self.user2.height/3))
        pygame.draw.rect(self.win, (2, 2, 255), (self.bitWinX * 15 - widthScore2Line,
            self.win.get_size()[1]/2 - 50 + self.sinValueY, widthScore2Line, self.user2.height/3))


    def gameOver(self):
        pygame.draw.rect(self.win, (2, 2, 2), (self.bitWinX*5, self.win.get_size()[1]/4, 
                self.bitWinX*10, 2*self.win.get_size()[1]/4))
        if self.user1.score - self.user2.score > 0:
            text = self.__TEXT_USER_WIN__ + self.username1
        else:
            text = self.__TEXT_USER_WIN__ + self.username2
        #self.font.size
        # = pygame.transform.scale(self.enemyAsteroidList[-1].image, (self.enemyAsteroidList[-1].radius*2, self.enemyAsteroidList[-1].radius*2))
        font = pygame.font.Font(self.__FONT_PATH_GAME_OVER__, int(self.win.get_size()[1]/15))
        fontScoreDisplay = font.render(text , False, (0, 255, 0))
        position = []
        position.append(self.win.get_size()[0]/2 - font.size(text)[0]/2)
        position.append(self.win.get_size()[1]/2 - font.size(text)[1]/2) 
        self.win.blit(fontScoreDisplay, position) 

        text = self.__TEXT_PRESS_ESC_TO_EXIT__
        font = pygame.font.Font(self.__FONT_PATH_PRESS_KEY__, int(self.win.get_size()[1]/25))
        fontScoreDisplay = font.render(text , False, (0, 255, 0))
        position = []
        position.append(self.win.get_size()[0]/2 - font.size(text)[0]/2)
        position.append(3 * self.win.get_size()[1]/4 - font.size(text)[1]) 
        self.win.blit(fontScoreDisplay, position)



    def updateDisplay(self):
        self.sinValueY = 10*sin(self.sinValue/10)
        self.sinValue += 1
        if self.sinValue > self.sinValueMax:
            self.sinValue = 0 

        self.updateBackgroundImage()
        if self.isPrintUsersScore:
            self.printScore()   
        self.enemyAsteroidUpdated()
        self.printUsers()
        
        if abs(self.user1.score - self.user2.score) == self.SCORE_END_GAME:
            self.gameOver()            
            if not self.flagGameOverSong:
                self.flagGameOverSong = True
                self.songBoom.play()
                self.songGameOver.play()
            
        pygame.display.update()
        
    def main_process_update(self):
        self.eventTest()
        self.updateDisplay()


if __name__ == "__main__":
    print("It is not a main module")