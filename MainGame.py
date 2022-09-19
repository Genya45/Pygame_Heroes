#   Игра на пайтоне с использованием PyGame


import pygame
from GameProcessClass import MainGame
from MenuClass import Menu

pygame.init()
pygame.mouse.set_visible(False)

#WIN_WIDTH = 600
#WIN_HEIGHT = 600
#FPS = int(1000/60)
FPS = 10    #   частота обновления кадров
#clockFPS = pygame.time.Clock()

username1 = "Игрок 1"
username2 = "Игрок 2"  



#   функция инициализации игрового процеса
def initGameProcess(win):
    global username1
    global username2
    while True:
        menu = Menu(win, username1, username2)    #   инициализация класса игрового процесса        
        while menu.isRunMainLoop:  #   цикл обновления игрового процесса
            pygame.time.delay(FPS)
            #clockFPS.tick(FPS) 
            menu.main_process_update()     #   обновление игрового процесса

        if menu.isCloseGame:
            break

        username1 = menu.username1
        username2 = menu.username2

        mainGame = MainGame(win, menu.imageBackgroundSpace, menu.isPrintUsersScore, username1, username2)    #   инициализация класса игрового процесса        
        while mainGame.isRunMainLoop:  #   цикл обновления игрового процесса
            pygame.time.delay(FPS)
            mainGame.main_process_update()     #   обновление игрового процесса



if __name__ == "__main__":          #   входная точка
    #   размеры окна
    winWidth = 1920
    winHeight = 1080

    #   созданное окно
    #win = pygame.display.set_mode((winWidth,winHeight), pygame.RESIZABLE | pygame.DOUBLEBUF | pygame.HWSURFACE)
    win = pygame.display.set_mode((winWidth, winHeight), pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE)
    #   название окна
    pygame.display.set_caption("Cosmo Game")
    initGameProcess(win)               #   вызов функции игры



pygame.quit()                       #   выход из игры