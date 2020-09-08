# Display Window

# Decided a class wasn't needed, since there is only ever going to be one
# instance/object acted on, thus can just use global variables in place or
# self/object. What others differences are there? and implic. of global vs self

# the global variables are analogous to local in global vs self, the self is
# object that belongs everywhere, every function performs on it of that class
# where as a global function just has it's function is acts for, unless
# it's not the case?

import pygame
from pygame.locals import *
import os
import cv2
import numpy as np
from movement import *
from GUI import guiobject

os.chdir('''C:\\Users\\Philip\\Documents\\Programming\\Opencv\\TarkovAutoSell\\CurveCalculator''')

# Initializing Everything
pygame.init()
x0 = 0
y0 = 0
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x0, y0)
info = pygame.display.Info()
screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.NOFRAME)
# screen = pygame.display.set_mode((1000,800))
pygame.display.set_caption('CurveCalculator')
pygame.mouse.set_visible(1)
clock = pygame.time.Clock()

# Instantiating Objects
bg1 = guiobject()
win1 = guiobject()
t1 = guiobject()
t2 = guiobject()
t3 = guiobject()
c1 = Movement()

# Making GUI Objects
bg1.background(screen, 'bg.jpg')
win1.window(500, 400)
t1.text('Rolling around at the speed of sound')
t2.text('Equation of Curve Given By:')


# t3.text(curve)

# Main loop
def Main():
    run = True
    while run:
        clock.tick(60)

        # User Inputs
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_q:
                'can light up keys for gui'
                # link boolean of light > gui attribute .colour shading
                # link bool(light) to the keys being highlighted
                run = False
            if event.type == KEYDOWN and event.key == K_w:
                c1.Keep()
                print('Last curve kept')
            if event.type == KEYDOWN and event.key == K_e:
                c1.save()
                print('saved to Curves.txt')
            if event.type == KEYDOWN and event.key == K_r:
                try:
                    c1.moving = True
                except IndexError:
                    print('click and move ya mouse first ya dingbat')

            # Playing Saved Curves
            if event.type == KEYDOWN and event.key == K_a:
                try:
                    KeptCurves[0].moving = True
                except IndexError:
                    print('no save there currently (a)')
            if event.type == KEYDOWN and event.key == K_s:
                try:
                    KeptCurves[1].moving = True
                except IndexError:
                    print('no save there currently (s)')
            if event.type == KEYDOWN and event.key == K_d:
                try:
                    KeptCurves[2].moving = True
                except IndexError:
                    print('no save there currently (d)')

            # Recording with clicks
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                c1.curve = []  # is this okay
                c1.recordActive = True
            if event.type == MOUSEBUTTONUP and event.button == 1:
                c1.recordActive = False
                print('Curve Recorded')

        t3.text('this is showing the equation')

        # Moving the base instance
        c1.move()
        c1.record()
        # Calculating moves for Saved instances
        for j in KeptCurves:
            j.move()

        screen.blit(bg1.surf, (0, 0))
        screen.blit(win1.surf, ((info.current_w) / 1.6, (info.current_h) / 7))
        screen.blit(t1.surf, ((info.current_w) / 1.5, (info.current_h) / 6.5))
        screen.blit(t2.surf, ((info.current_w) / 1.5, (info.current_h) / 5))
        screen.blit(t3.surf, ((info.current_w) / 1.5, (info.current_h) / 4.5))

        pygame.display.update()

    pygame.quit()


Main()

'Considerations'

# How does declaring attributes at function call compare VS declaring at
# instantiation?

# Changed global curve > object
# Now having to specify object being acted on at each method ---
# Can simply loop over the one instance

'Solutions'

# json load() can't handle decoding multiple json objects, thus just need to
# wrap all objects in a list, them json them together



