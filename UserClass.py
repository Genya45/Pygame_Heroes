
class User:
    def __init__(self, posX, posY, maxW, maxH, image, height = 100, width = 100):
        #   позиция
        self.posX = posX
        self.posY = posY
        #   размеры окна
        self.maxW = maxW
        self.maxH = maxH
        #   размеры
        self.height = height
        self.width = width
        #   изображение 
        self.image = image
        self.score = 0
