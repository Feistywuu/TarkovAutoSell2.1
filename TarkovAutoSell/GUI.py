# GUI

import pygame
from pygame.locals import *
import os

os.chdir('''C:\\Users\\Philip\\Documents\\Programming\\Opencv\\TarkovAutoSell\\CurveCalculator''')

pygame.init()


def load_image(name, colorkey=None):
    fullname = os.path.join(os.getcwd(), name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error:
        print("Cannot load image:", fullname)
        raise SystemExit(str(geterror()))
    image = image.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image


# Interface object Class
class guiobject():

    def __init__(self):
        # x,y pos = 0
        self.x = None
        self.y = None
        self.surf = pygame.Surface((0, 0))

    def text(self, text):
        '''
        Makes text, starting at x,y
        '''
        self.font = pygame.font.Font((pygame.font.get_default_font()), 22)
        self.surf = self.font.render(text, 0, (0, 0, 0), (100, 100, 100))
        return self.surf

    def window(self, w, h):
        '''
        Makes a surface of (w,h) size
        '''
        self.w = w
        self.h = h
        self.surf = pygame.Surface((w, h))
        self.surf.convert()
        self.surf.fill((255, 255, 255))
        return self.surf

    def background(self, screen, image):
        '''
        Creates a background surface with image
        '''
        self.surf = pygame.Surface(screen.get_size())
        self.surf = load_image(image)
        self.surf = self.surf.convert()
        return self.surf












