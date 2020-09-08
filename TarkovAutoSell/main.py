# Tarkov Auto-sell

#   Press a button to execute this script; requires tarkov open

import time
import pyautogui
import json
import os
import numpy as np
import cv2
import pygame
from pygame.locals import *
from time import time
from windowCapture import WindowCapture
from matchingFunctions import *
import Functions
from movement import Movement

# Importing Curves from Curves.txt
os.chdir('''C:\\Users\\Philip\\Documents\\Programming\\Opencv\\TarkovAutoSell''')
Save = open(os.path.join('''C:\\Users\\Philip\\Documents\\Programming\\Opencv\\TarkovAutoSell\\CurveCalculator''',
                         'Curves.txt'))
try:
    x = json.load(Save)
    print(x)
    x1 = np.array(x[0])
    x2 = np.array(x[1])
except IndexError:
    print('not 2 saves')

# Assuming whole number of squares on top-side
# Bounds in MainStash
#CLICKED 1266 77
#CLICKED 1896 935

#CLICKED 1266 115 - 62/63
#CLICKED 1328 178 - 63/62
#CLICKED 1391 240 - 63/64
#CLICKED 1454 304 - 63/63
#CLICKED 1517 367 - 64/63
#CLICKED 1581 430

stashWidth = 4
stashHeight = 4

wincap =  WindowCapture('EscapeFromTarkov')
TarkovScreenN = wincap.get_screenshot()
stashBoundry = TarkovScreenN[77:77+63*stashHeight, 1264:1264+63*stashWidth]
cv.imshow('mainStash', stashBoundry)
# Calculate x,y pos of items within the boundries

# Instance of Window in np array form, matching algorithm is run on it
wincap = WindowCapture('EscapeFromTarkov')
TarkovScreen1 = wincap.get_screenshot()
FiR = Detect(TarkovScreen1, fir, 0.8)
print(FiR)

# Creating another screencap
wincap = WindowCapture('EscapeFromTarkov')
TarkovScreen2 = wincap.get_screenshot()

# Creating template for each FiR item
# Create dictionary of { ((FiR(x,y);screencap), ...((x,y);cap) )
FiRdict = {}
for item in FiR:
    template = TarkovScreen2[(item[1] - 35):(item[1] + 16), (item[0] - 48):(item[0] + 16)]
    FiRdict.update({item: template})

# Instantiating/Initializing stuff
pygame.init()
x0 = 0
y0 = 0
info = pygame.display.Info()
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x0, y0)
# screen = pygame.display.set_mode((info.current_w, info.current_h) , pygame.NOFRAME)
screen = pygame.display.set_mode((100, 100))
pygame.display.set_caption('Mistakes were made')
pygame.mouse.set_visible(1)
clock = pygame.time.Clock()

# Sometimes goes to wrong FiRitem - Why?
# How can matchObject distinguish between different objects of the same template? Will this cause issues?
# - Can define bounds for FiRitems to be found, search for that bounded area within the stash
# - Allow user to drag a boundry

def Menu():
    # Waits for user inputs to select certain variables, here FiRItems dictionary generated
    # and a stash boundry template is generated
    pass
    Awaiting = True
    while Awaiting:
        clock.tick(60)
        break

    pass

def Main():
    # Need object to act on
    A = Movement()
    count = 0                   # item sold count
    Awaiting = True

    # Gradually looping over the item locations in FiR
    if FiRdict == {}:
        print('no objects on screen')
    for FiRItem in FiRdict:
        print(id(Functions.Matches))
        Functions.initAndClear()                                         # Clears 'Matches' for new item
        print(id(Functions.Matches))
        cv.imshow('current template', FiRdict[FiRItem])
        print('Current item: ' + str(FiRItem))
        # Aligning curve x1, to item position, destination 'add offer'
        A.align(FiRItem, (1300, 75), x1)

        if count % 3 == 0 and count != 0:  # If 3 items sold, doesn't await user input
            Awaiting = True

        f = 0  # Frame count
        # Awaiting for user inputs
        while Awaiting == True:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_q:  # Quit
                    pygame.quit()
                    print('Stopped')
                if event.type == KEYDOWN and event.key == K_w:
                    pyautogui.moveTo(FiRItem[0], FiRItem[1], 2)  # Moving to FiR item,
                    pyautogui.click(button='right')  # Open 'filter by item',
                    pyautogui.move(10, -78, 0.5)
                    time.sleep(1)
                    pyautogui.click(button='left')  # Clicks it
                    time.sleep(1)
                    A.moving = True

            if f % 90 == 0:
                print('''Awaiting execution m'lord''')

            A.move()  # Moves to 'add offer'    Why is this making me move to FiRItem each frame? Why doesn't it print
            f += 1

            if A.moving == False and pyautogui.position() == A.dest:
                print('Moved and reached')
                break

        # Moving to FiR item, open 'filter by item', click 'add offer'
        if Awaiting == False:
            pyautogui.moveTo(FiRItem[0], FiRItem[1], 2)
            pyautogui.click(button='right')
            pyautogui.move(10, -78, 0.5)
            time.sleep(1)
            pyautogui.click(button='left')  # without sleep(1), why discard?
            time.sleep(1)  # related to A.moving = True
            A.moving = True

            while A.moving == True:
                clock.tick(60)
                A.move()

                if A.moving == False and pyautogui.position() == A.dest:
                    print('Moved and reached')
                    break

        Functions.GetValue()

        # Click 'add offer'
        pyautogui.click(button='left')
        time.sleep(1)

        # Find item in stash
        cap = WindowCapture('EscapeFromTarkov')
        stashScreenCap = cap.get_screenshot()
        stashScreen = stashScreenCap[204:931, 408:1039]
        cv.imshow('test', stashScreen)

        # Run matching algorithm - objectMatch(stash, FiR template), select obj.
        # if false, click on bar, drag down, repeat until match found
        XX = Detect(stashScreen, FiRdict[FiRItem], 0.72)
        if XX == []:
            stashitemLoc = Functions.LocateStashItem(1044, 323, FiRdict[FiRItem])
        # Adjusted x,y, shoving to right+down by 2 pixels, since detect takes
        # the top left corner
        stashItemLocOnScreen = stashitemLoc[0][0] + 410, stashitemLoc[0][1] + 206

        # Move to object
        A.MoveTo(pyautogui.position(), stashItemLocOnScreen, x2)

        # Click Object
        time.sleep(0.1)
        pyautogui.click(button='left')

        # Creating loop for movement to '+'
        A.MoveTo(pyautogui.position(), (1462, 500), x2)

        # Click it, Moving to 'Currency', clicking it
        pyautogui.click(button='left')
        A.MoveTo(pyautogui.position(), (996, 197), x1)
        time.sleep(0.1)
        pyautogui.click(button='left')
        time.sleep(0.5)

        print(Functions.Matches)                  # Why is Matches empty?
        # Typing Value - 1
        TheValue = Functions.Matches[0] - 1
        strValue = str(TheValue)
        keys = []
        for digit in strValue:
            keys.append(digit)
        pyautogui.write(keys, interval=0.15)

        # Moving to 'add', clicking it
        A.MoveTo(pyautogui.position(), (962, 899), x1)
        time.sleep(0.1)
        pyautogui.click(button='left')

        # Moving
        A.MoveTo(pyautogui.position(), (1274, 893), x2)
        time.sleep(0.1)

        pyautogui.click(button='left')
        print('item sold')
        pyautogui.press('esc')
        Awaiting = False

        # Why is match location on the left side center of FiRItem?
        # i.e the detect location in drag

        count += 1

Menu()
Main()

' TO DO '

# Main Moveto() functions
# Allow only specified bounds of stash to be searched for FiR items - show the stash bounded in the GUI
# Only check stash for FiR items
# Scale dimensions for any monitor size
# complete loop
# Clean up code
# Take median of last 3 results
# Make containers(things with a tag) and/or vests/backpacks not eligible
# Allow somehow to grab all prices, then allow a review before selling the items
# Can't I remove 'Matches' from Functions if I declare it as global within the function?

'''Errors'''

'''Notes'''

# Main loop, calculates shift every time it iterates to item
# vs calculating all shifts, storing in list and referring to them
# Will use shift per loop


# If we were in a x,y axis centered on the FiR item, we could have 1 singular
# gradient matrix [Kx, Ky], but since we are not centered on x,
# each x1:(x,y) plot, needs a respective k matrix.

# Work centered on 0, by only dealing with change quantities
# so need x1 in terms of distance

'''Considerations'''

# Can make get_screenshot() only capture the inventory side of tarkov
# left side is not needed.

# If item is behind FiR symbol, the matching will not reach required threshold
# Matching only the FiR symbol, with background cropped will remedy that

# can let user program destinations

# Containers cause an issue, since their menu has 'tag' + others in it

# Understand how sys.insert works

# Work out this pixel as a fraction of screen dimensions



