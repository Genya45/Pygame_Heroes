import pygame
import random
import os
from EnemyAsteroidClass import EnemyAsteroid


class Menu():
    

    def __init__(self, win, username1, username2):        
        self.win = win
        self.isRunMainLoop = True
        self.isPrintUsersScore = True

        
        self.__FONT_PATH_MENU__ = "assets/fonts/new/ofont.ru_Ritalin.ttf"
        self.__FONT_PATH_USERS__ = "assets/fonts/new/ofont.ru_Sangha.ttf"
        #self.__FONT_PATH__ = 'assets/fonts/Lato-Black.ttf'
        self.fontMenu = None
        self.fontUsers = None
        #self.__TEXT_PRESS_ESC_TO_EXIT__ = 'PRESS ESC TO EXIT'
        #self.__TEXT_PRESS_ENTER_TO_START_GAME__ = 'PRESS ENTER TO START GAME'
        self.__TEXT_PRESS_ESC_TO_EXIT__ = 'НАЖМИТЕ ESC ЧТОБЫ ВЫЙТИ'
        self.__TEXT_PRESS_ENTER_TO_START_GAME__ = 'НАЖМИТЕ ENTER ДЛЯ НАЧАЛА ИГРЫ'

        self.username1 = username1
        self.username2 = username2 
        self.currUserInputName = 1
        self.timeToLineAfterNameInInput = 0
        self.flagToLineAfterNameInInput = True
        
        self.__IMG_PATH_BKG_SPACE__ = "assets/images/backgrounds/"     
        self.imageBackgroundSpace = None
        self.imageBackgroundSpaceNumber = None
        
        self.__IMG_PATH_ASTEROIDS__ = "assets/images/asteroids/" 
        self.enemyAsteroidTicks = 0
        self.enemyAsteroidTicksMax = 20
        self.enemyAsteroidList = []
        self.asteroidsListImages = []

        self.isStartGame = False
        self.isCloseGame = False

        self.__MUSIC_BACKGROUND_PATH__ = 'assets/music/BackgroundMenu.mp3'

        
        self.imageLoader()
        self.fontLoader()        
        self.songLoader()


    def imageLoader(self):
        listImagesBackgroundSpace = os.listdir(self.__IMG_PATH_BKG_SPACE__)
        self.imageBackgroundSpaceNumber = random.randint(0, len(listImagesBackgroundSpace) - 1)
        self.imageBackgroundSpace = pygame.image.load(self.__IMG_PATH_BKG_SPACE__ + listImagesBackgroundSpace[self.imageBackgroundSpaceNumber])
        self.imageBackgroundSpace = pygame.transform.scale(self.imageBackgroundSpace, self.win.get_size())
        
        for imageAsteroid in os.listdir(self.__IMG_PATH_ASTEROIDS__):       
            asteroidImage = pygame.image.load(self.__IMG_PATH_ASTEROIDS__ + imageAsteroid)
            self.asteroidsListImages.append(asteroidImage)

    def fontLoader(self):
        self.fontMenu = pygame.font.Font(self.__FONT_PATH_MENU__, 50)
        self.fontUsers = pygame.font.Font(self.__FONT_PATH_USERS__, 50)

    def songLoader(self):
        pygame.mixer.music.load(self.__MUSIC_BACKGROUND_PATH__)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play()

    
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
                elif event.key == pygame.K_SPACE:
                    self.isRunMainLoop = False
                    self.isStartGame = True
                    self.isPrintUsersScore = True
                    pygame.mixer.music.stop()
                    break
                elif event.key == pygame.K_RETURN:
                    self.isRunMainLoop = False
                    self.isStartGame = True
                    self.isPrintUsersScore = False
                    pygame.mixer.music.stop()
                    break
                elif event.key == pygame.K_1:
                    self.currUserInputName = 1
                elif event.key == pygame.K_2:
                    self.currUserInputName = 2
                elif event.key == pygame.K_BACKSPACE:
                    if self.currUserInputName == 1:
                        if len(self.username1) >= 0:
                            self.username1 = self.username1[0:-1]
                    if self.currUserInputName == 2:
                        if len(self.username2) >= 0:
                            self.username2 = self.username2[0:-1]
                else:
                    if self.currUserInputName == 1:
                        self.username1 += event.unicode
                    if self.currUserInputName == 2:
                        self.username2 += event.unicode



    def updateBackgroundImage(self):
        self.win.blit(self.imageBackgroundSpace, (0, 0))

    def printUsersName(self):
        self.timeToLineAfterNameInInput += 1
        if self.timeToLineAfterNameInInput > 20:
            self.timeToLineAfterNameInInput = 0
            self.flagToLineAfterNameInInput = not self.flagToLineAfterNameInInput


        text = self.username1
        fontScoreDisplay = self.fontUsers.render(text , False, (0, 0, 255))
        position = []
        position.append(self.win.get_size()[0]*0.25 - self.fontUsers.size(text)[0]/2)
        position.append(self.win.get_size()[1]*0.1)        
        #pygame.draw.rect(self.win, (2, 2, 2), (position[0]-5, position[1]-5, self.font.size(text)[0]+10, self.font.size(text)[1]+5)) 
        if self.flagToLineAfterNameInInput and self.currUserInputName == 1:
            pygame.draw.rect(self.win, (0, 0, 255), (position[0] + self.fontUsers.size(text)[0], position[1]-5, 5, self.fontUsers.size(text)[1]+5)) 
        self.win.blit(fontScoreDisplay, position) 
        
        text = self.username2
        fontScoreDisplay = self.fontUsers.render(text , False, (255, 0, 0))
        position = []
        position.append(self.win.get_size()[0]*0.75 - self.fontUsers.size(text)[0]/2)
        position.append(self.win.get_size()[1]*0.1)        
        #pygame.draw.rect(self.win, (2, 2, 2), (position[0]-5, position[1]-5, self.font.size(text)[0]+10, self.font.size(text)[1]+5)) 
        if self.flagToLineAfterNameInInput and self.currUserInputName == 2:
            pygame.draw.rect(self.win, (255, 0, 0), (position[0] + self.fontUsers.size(text)[0], position[1]-5, 5, self.fontUsers.size(text)[1]+5))         
        self.win.blit(fontScoreDisplay, position) 

    def selectMenu(self):
        text = self.__TEXT_PRESS_ESC_TO_EXIT__
        fontScoreDisplay = self.fontMenu.render(text , False, (0, 255, 0))
        position = []
        position.append(self.win.get_size()[0]/2 - self.fontMenu.size(text)[0]/2)
        position.append(self.win.get_size()[1]/4)        
        #pygame.draw.rect(self.win, (2, 2, 2), (position[0]-5, position[1]-5, self.font.size(text)[0]+10, self.font.size(text)[1]+5)) 
        self.win.blit(fontScoreDisplay, position) 
        
        text = self.__TEXT_PRESS_ENTER_TO_START_GAME__
        fontScoreDisplay = self.fontMenu.render(text , False, (0, 255, 0))
        position = []
        position.append(self.win.get_size()[0]/2 - self.fontMenu.size(text)[0]/2)
        position.append((self.win.get_size()[1]/4 + self.win.get_size()[1]/2) - self.fontMenu.size(text)[1])
        #pygame.draw.rect(self.win, (2, 2, 2), (position[0]-5, position[1]-5, self.font.size(text)[0]+10, self.font.size(text)[1]+5)) 
        self.win.blit(fontScoreDisplay, position) 






    def updateDisplay(self):
        self.updateBackgroundImage()
        self.selectMenu()   
        self.enemyAsteroidUpdated()
        self.printUsersName()
        pygame.display.update()
        
    def main_process_update(self):
        self.eventTest()
        self.updateDisplay()



if __name__ == "__main__":
    print("It is not a main module")