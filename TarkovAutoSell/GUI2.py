# GUI for user inputs for main()

import tkinter as tk
from tkinter import messagebox
import pyautogui
import time
import Functions
from PIL import Image, ImageTk
from windowCapture import WindowCapture
from matchingFunctions import *
from movement import Movement
import sys
import json
from win32api import GetCursorPos

# test for curve update loop
import pygame
from pygame.locals import *

''' To Do'''

''' //////////////// THINGS ///////////////  '''

''' Testing Curve Evolution  '''                                                                    # (0.2)
# Require update loop that records (x,y) to record curves - could use multiprocessing?

''' Curve Evolution:                                                                                # (0.5)
# when curve is aligned within evolve, thus running through align again in MoveTo() is redundant, except for cases
#when a curve isn't evolved first

# Need to able to test curve evolution
#make button with a function that tests
# Scale the 'Evolved Curve' to the new start and destination.
# For 'human overshoot' let destination be 'random num. + overshoot' then move to 'random num'

'''

''' Can add all 3 times in the one fleasStash screen, so only 1 drag function required'''              # (1)

# On the very left edge of 4th from right.edge square, filter actually goes to the right

''' Smoothing Drag ---- Multi-threading '''

# How can the Drag:Check process be smoothed out?                                                   (1.5)
# Determine where most time is spent processing for screencap() and Detect()

# Use multithreading to smoothen drag:                                                              (2)
# One process will drag, at periods like a square/2 squares, take screencap and boolean to activate other thread
# first process will continue moving
# second process will Detect(), upon matchL:
# both processes end - Then moves to firitem in fleaStash

# use multithreading to calculate curve evolution during main process

' For overshot algorithm'                                                                            # (2.5)
# %chance to retain original RNG destination OR choose a overshot RNG destination - travel to it.
# Then choose ANOTHER RNG position offshot from ACTUAL RNG destination - travel to it
# then GENERATE another ACTUAL destination - travel to it

# So most of the time will travel to destination; with a chance to travel to overshoot destination afterwards;
# then travelling back to the a new destination in the boundary, causing randomness
# OR
# will just travel to a misaligned destination to begin with, overshoot that, THEN travel back to the RNG destination

# Make periodically check many items are in up on market, if there is space, run sell algorithm         (3)

# \\\\  Efficiences  //// #

# Create variable drag speed like a human
# create variable speed in every curve
# Optimize movement on left/right on 'filter by' choice
# Things might all be out by 1, because of the randint(range) function - can result in a large change by the end
# why does mouse sometimes jump?
# make it learn efficient ways (1000)

# Every time RNG function for boundaries if called, it checks state of all booleans - Can this be more efficient?

''' /// Thoughts '''
# Originally working with self.RNGdistance - stored all generations in a list for past data access
# Originally was working with self.startingPos and would write over the same variable over and over,
# but this would cause readability issues ( moving from self.startingPos > self.startingPos in one function)
# thus introduced a list to allow distinction between them - Is this good practice? <<<
# Simply adds 1 line of computation + memory to store list

''' ////////////////////////////////////////////////////'''
''' Required user prep - tarkov screen must be on the stash'''
''' Only have FiR items within stashBoundary or else match to stash fails'''
''' don't use top 2 rows of stash atm, threshold cannot accurately get numbers and determine object shape (due to light)'''



# Defining for 16:9 ratio resolutions.
#self.Xratio = 1264/1920 = 0.6583*
#self.Yratio = 77/1080 = 0.07130
#self.XstashUnit = 63/1920 = 0.0328
#self.YstashUnit = 63/1080 = 0.0583*

# Generalising:
#ratio =


class Gui2:

    Exit = False

    def __init__(self, master, movementobject):
        self.master = master
        self.movementobject = movementobject
        self.stashBoundary = []
        self.XshiftToStash = 1264
        self.YshiftToStash = 77
        self.FiRdict = [0]                      # defined in firdict func
        self.count = 0
        self.Awaiting = True
        self.stashWidthMin = 0
        self.stashWidthMax = 10
        self.stashHeightMin = 0
        self.stashHeightMax = 13
        self.stashimg = []
        self.currentFiRitem = []                 # Position of FiRitem in stash
        self.SavedStartingPositions = []
        'FiR = pos of items in self.stashBoundary'

        # Load self.stashBoundary settings from 'settings.txt'
        try:
            initSettings = open(os.path.join('''C:\\Users\\Philip\\PycharmProjects\\TarkovAutoSell2.1\\TarkovAutoSell''', 'settings.txt'))
            load1 = json.load(initSettings)
            self.stashWidthMin, self.stashWidthMax, self.stashHeightMin, self.stashHeightMax = load1[0], load1[1], load1[2], load1[3]
        except json.decoder.JSONDecodeError:
            print('First time run, using default self.stashBoundary settings')

        # Main background window
        self.canvas = tk.Canvas(self.master, width=940, height=1000)
        self.canvas.pack()
        self.master.title("TarkovAutoSell")

        # Information box No.1
        self.labelx1 = tk.Label(self.master, text='Any FiR items in your chosen area will be sold; ')
        self.canvas.create_window(150, 100, window=self.labelx1)
        self.labelx2 = tk.Label(self.master, text='pls no containers, filled vests/backpacks.')
        self.canvas.create_window(150, 120, window=self.labelx2)
        self.labelx3= tk.Label(self.master, text='''Once you are done, click 'Generate FiR items  ''')
        self.canvas.create_window(150, 140, window=self.labelx3)
        self.labelx4= tk.Label(self.master, text='''to double check the items to be sold''')
        self.canvas.create_window(150, 160, window=self.labelx4)

        # Quit Button
        def close_window():
            self.master.destroy()
            print('Stopped')

        self.button2 = tk.Button( text='Quit...?', command=close_window)
        self.canvas.create_window(50, 50, window=self.button2)

        # Buttons to increase stash size
        def pluswidth():
            try:
                self.stashWidthMax += 1
                ScreenCap()
            except ValueError:
                self.stashWidthMax -= 1
                print('Increased too far right')

        def plusheight():
            try:
                self.stashHeightMax += 1
                ScreenCap()
            except ValueError:
                self.stashHeightMax -= 1
                print('Increased too far down')

        def subtractwidth():
            try:
                self.stashWidthMax -= 1
                ScreenCap()
            except ValueError:
                self.stashWidthMax += 1
                print('Decreased too far right')

        def subtractheight():
            try:
                self.stashHeightMax -= 1
                ScreenCap()
            except ValueError:
                self.stashHeightMax += 1
                print('Decreased too far right')


        self.plusW = tk.Button(text='+W', command=pluswidth)
        self.canvas.create_window(100, 200, window=self.plusW)
        self.plusH = tk.Button(text='+H', command=plusheight)
        self.canvas.create_window(60, 270, window=self.plusH)
        self.subtractW = tk.Button(text='-W', command=subtractwidth)
        self.canvas.create_window(100, 230, window=self.subtractW)
        self.subtractH = tk.Button(text='-H', command=subtractheight)
        self.canvas.create_window(30, 270, window=self.subtractH)


        # Buttons to move stash location
        def Up():
            try:
                self.stashHeightMin -= 1
                self.stashHeightMax -= 1
                ScreenCap()
            except ValueError:
                self.stashHeightMin += 1
                print('Moved too far up')
                try:
                    ScreenCap()
                except ValueError:
                    self.stashHeightMax = 13
                    self.stashHeightMin = 0
                    print('Set to Default')

        def Down():
            try:
                self.stashHeightMax += 1
                self.stashHeightMin += 1
                ScreenCap()
            except ValueError:
                self.stashHeightMax -= 1
                print('Moved too far down')
                try:
                    ScreenCap()
                except ValueError:
                    self.stashHeightMax = 13
                    self.stashHeightMin = 0
                    print('Set to Default')

        def Left():
            try:
                self.stashWidthMin -= 1
                self.stashWidthMax -= 1
                ScreenCap()
            except ValueError:
                self.stashWidthMin += 1
                print('Moved too far Left')
                try:
                    ScreenCap()
                except ValueError:
                    self.stashWidthMin = 0
                    self.stashWidthMax = 10
                    print('Set to Default')

        def Right():
            try:
                self.stashWidthMax += 1
                self.stashWidthMin += 1
                ScreenCap()
            except ValueError:
                self.stashWidthMax -= 1
                print('Moved too far Right')
                try:
                    ScreenCap()
                except ValueError:
                    self.stashWidthMin = 0
                    self.stashWidthMax = 10
                    print('Set to Default')

        self.top1 = tk.Button(text='Up', command=Up)
        self.canvas.create_window(200, 220, window=self.top1)
        self.bot2 = tk.Button(text='Down', command=Down)
        self.canvas.create_window(200, 320, window=self.bot2)
        self.left1 = tk.Button(text='Left', command=Left)
        self.canvas.create_window(150, 270, window=self.left1)
        self.right1 = tk.Button(text='Right', command=Right)
        self.canvas.create_window(250, 270, window=self.right1)

        # Generate stashBoundary Button
        def ScreenCap():

            # Instance of Window in np array form
            wincap = WindowCapture('EscapeFromTarkov')
            TarkovScreenN = wincap.get_screenshot()
            self.stashBoundary = TarkovScreenN[77 + 63 * self.stashHeightMin:77 + 63 * self.stashHeightMax, 1264 + 63 * self.stashWidthMin:1264 + 63 * self.stashWidthMax]

            # Convert into displayable form
            self.stashBoundaryRGB = cv.cvtColor(self.stashBoundary, cv.COLOR_BGR2RGB)
            self.stashimg = ImageTk.PhotoImage(image=Image.fromarray(self.stashBoundaryRGB))

            # Shows self.stashBoundary
            self.canvas.create_image(300, 100, anchor="nw", image=self.stashimg)

        # Generate FiRItems from stashBoundary
        def FirItems():
            '''
            Detects FiRitems in user defined self.stashBoundary; Generates self.FiRdict
            :return: self.FiRdict
            '''
            # Take fresh screencap
            wincap = WindowCapture('EscapeFromTarkov')
            TarkovScreenN1 = wincap.get_screenshot()

            # Select portion of screencap chosen by user in UI
            self.stashBoundary = TarkovScreenN1[
                                 self.YshiftToStash + 63 * self.stashHeightMin:self.YshiftToStash + 63 * self.stashHeightMax,
                                 self.XshiftToStash + 63 * self.stashWidthMin:self.XshiftToStash + 63 * self.stashWidthMax]

            # Detect FiRItems in stashBoundary
            FiR = Detect(self.stashBoundary, fir, 0.8)

            # Check position of FiR match within self.stashBoundary, then take the containing square as a template
            # Create dictionary of { ((itempos, itemcap), ... (pos,cap)) }
            self.FiRdict = {}
            for item in FiR:
                templateX = item[0] + (63 - item[0] % 63)  # Transforming to nearest multiple of 63 above
                templateY = item[1] + (63 - item[1] % 63)
                template = self.stashBoundary[templateY - 63:templateY, templateX - 63:templateX]

                '''
                # Require item location on screen, independent of stashBoundary location.
                self.FiRdict.update({(item[0] + 63*self.stashWidthMin, item[1] + 63 * self.stashHeightMin): template})
                '''

                # FiR item location within self.stashBoundary
                self.FiRdict.update({(item[0], item[1]): template})

            # Choosing current FiR item from self.FiRdict
            try:
                self.currentFiRitem = list(self.FiRdict)[0]
                self.FiRdictKeys = list(self.FiRdict.keys())
                print(self.FiRdictKeys)

                # Converting to displayable form
                self.currentitem0RGB = cv.cvtColor(self.FiRdict[self.FiRdictKeys[0]], cv.COLOR_BGR2RGB)
                self.currentitem0 = ImageTk.PhotoImage(image=Image.fromarray(self.currentitem0RGB))
                self.canvas.create_image(50, 600, anchor="nw", image=self.currentitem0)
            except IndexError as error:
                print(error)
                print('self.FiRdict is empty - there are no FiR items on the screen')
                #return
            try:
                self.currentitem1RGB = cv.cvtColor(self.FiRdict[self.FiRdictKeys[1]], cv.COLOR_BGR2RGB)
                self.currentitem1 = ImageTk.PhotoImage(image=Image.fromarray(self.currentitem1RGB))
                self.canvas.create_image(120, 600, anchor="nw", image=self.currentitem1)
            except IndexError as error:
                print(error)
                print('Cannot print all items, not enough items in FiRdict')
                #return
            try:
                self.currentitem2RGB = cv.cvtColor(self.FiRdict[self.FiRdictKeys[2]], cv.COLOR_BGR2RGB)
                self.currentitem2 = ImageTk.PhotoImage(image=Image.fromarray(self.currentitem2RGB))
                self.canvas.create_image(190, 600, anchor="nw", image=self.currentitem2)
            except IndexError as error:
                print(error)
                print('Cannot print all items, not enough items in FiRdict')
                #return

        self.button4 = tk.Button(text='Show current items being sold', command=FirItems)
        self.canvas.create_window(100, 450, window=self.button4)

        # test save button
        def testsave():
            # save self.stashBoundary settings to 'settings.txt'
            os.chdir('''C:\\Users\\Philip\\PycharmProjects\\TarkovAutoSell2.1\\TarkovAutoSell''')
            stashSettings = [self.stashWidthMin, self.stashWidthMax, self.stashHeightMin, self.stashHeightMax]
            f = open("settings.txt", "w+")
            stashSettings = json.dumps(stashSettings)
            f.write(stashSettings)
            print(stashSettings)
            print('Settings Saved')

        self.buttonTest = tk.Button(text='Save Boundary', command=testsave)
        self.canvas.create_window(330, 50, window=self.buttonTest)

        # Execute button
        def SellThrice():
            # save self.stashBoundary settings to 'settings.txt'
            os.chdir('''C:\\Users\\Philip\\PycharmProjects\\TarkovAutoSell2.1\\TarkovAutoSell''')
            stashSettings = [self.stashWidthMin, self.stashWidthMax, self.stashHeightMin, self.stashWidthMax]
            f = open("settings.txt", "w+")
            stashSettings = json.dumps(stashSettings)
            f.write(stashSettings)
            print(stashSettings)
            print('Settings Saved')

            # Sell algorithm 3 times
            SellItem()
            SellItem()
            SellItem()

        def SellItem():
            '''
            Takes a screenshot of stashBoundary - generates self.FiRdict and self.currentItem.
            Sells item, then self.count += 1
            :return: Item is sold, self.count += 1
            '''

            # Generates self.FiRdict from self.stashBoundary
            FirItems()

            # set initial positions
            self.movementobject.startingPos = pyautogui.position()
            self.movementobject.startingPositions.append(self.movementobject.startingPos)

            # Moving to FiRitem
            self.movementobject.MoveToRandom(self.movementobject.startingPositions[0], self.movementobject.savedCurves[0],
                                             ((self.currentFiRitem[0] + self.XshiftToStash + self.stashWidthMin*63),
                                             (self.currentFiRitem[1] + self.YshiftToStash + self.stashHeightMin*63)),
                                             (-47, 14),
                                             (-47, 14))

            # Moving to FiR item
            time.sleep(1)
            pyautogui.click(button='right')                                                     # Open item dropdown
            self.movementobject.MoveToRandom(self.movementobject.startingPositions[1], self.movementobject.savedCurves[0],
                                             self.movementobject.startingPositions[1],
                                             (3, 110),
                                             (45, 54))

            time.sleep(0.5)
            pyautogui.click(button='left')
            time.sleep(0.5)

            # Moving from 'filter by item' > 'add offer'
            self.movementobject.MoveToRandom(self.movementobject.startingPositions[2], self.movementobject.savedCurves[0],
                                             (1145, 64),
                                             (0, 219),
                                             (0, 33))

            # Calculating values from listings
            print(Functions.Matches)
            Functions.GetValue()

            # Click 'add offer'
            pyautogui.click(button='left')
            time.sleep(0.5)

            # move to fleaStash dragbar
            self.movementobject.MoveToRandom(self.movementobject.startingPositions[3], self.movementobject.savedCurves[0],
                                             (1042, 210),
                                             (0, 6),
                                             (0, 227))
            time.sleep(0.5)

            # Find stashBoundary in flea market stash
            cap = WindowCapture('EscapeFromTarkov')
            stashScreenCap = cap.get_screenshot()
            fleaStash = stashScreenCap[54:1086, 258:1189]
            cv.imshow('test', fleaStash)

            # Run matching algorithm - objectMatch(fleaStash, stashBoundary), select obj.
            # if false, click on bar, drag down, repeat until match found
            XX = Detect(fleaStash, self.stashBoundary, 0.81)
            if XX == []:
                fleaStashBoundaryLoc = self.LocateStashItem(1044, 323, self.stashBoundary)
            else:
                fleaStashBoundaryLoc = XX

            # Allows for exit if error in matching fleaStash - Maybe making this a second thread running all the time?
            if self.Exit == True:
                messagebox.showerror("WHAT HAVE YOU DONE", "take the non FiR items out of your stash area u beautiful numbnut"
                                                           "(couldn't find your items in the fleamarketStash)")
                return

            # move to FiRItem location; within the stashBoundary; within the fleaStash
            fleaStashBoundaryLoc = fleaStashBoundaryLoc[0][0] - 150, fleaStashBoundaryLoc[0][1] - 150                       # Adjusting for x,y, w.r.t fleaStash
            fleaStashLoc = fleaStashBoundaryLoc[0] + 410, fleaStashBoundaryLoc[1] + 206                                     # Adjusted x,y, w.r.t fleaStash on screen + offset by 2/2 BotRight

            self.movementobject.MoveToRandom(self.movementobject.startingPositions[4], self.movementobject.savedCurves[0],
                                             (fleaStashLoc[0] + self.currentFiRitem[0],
                                              fleaStashLoc[1] + self.currentFiRitem[1]),
                                             (-47, 13),
                                             (-47, 13))
            print('stashBoundary at ' + str(fleaStashLoc) + ' on-screen')

            # click Object
            time.sleep(0.5)
            pyautogui.click(button='left')

            # move to '+'
            self.movementobject.MoveToRandom(self.movementobject.startingPositions[5], self.movementobject.savedCurves[0],
                                             (1450,491),
                                             (0, 29),
                                             (0, 20))

            # click it, move to 'Currency', click it
            time.sleep(0.5)
            pyautogui.click(button='left')
            self.movementobject.MoveToRandom(self.movementobject.startingPositions[6],
                                             self.movementobject.savedCurves[0],
                                             (868, 190),
                                             (0, 48),
                                             (0, 9))
            time.sleep(0.1)
            pyautogui.click(button='left')
            time.sleep(0.5)

            # type value - 1
            TheValue = Functions.Matches[0] - 1
            strValue = str(TheValue)
            keys = []
            for digit in strValue:
                keys.append(digit)
            pyautogui.write(keys, interval=0.15)

            # move to 'add', click it
            self.movementobject.MoveToRandom(self.movementobject.startingPositions[7],
                                             self.movementobject.savedCurves[0],
                                             (925, 885),
                                             (0, 70),
                                             (0, 28))
            time.sleep(1)
            pyautogui.click(button='left')

            # move to 'place offer'
            self.movementobject.MoveToRandom(self.movementobject.startingPositions[8],
                                             self.movementobject.savedCurves[0],
                                             (1160, 874),
                                             (0, 299),
                                             (-7, 0))

            time.sleep(0.5)  #
            pyautogui.click(button='left')
            print('item sold')
            pyautogui.press('esc')
            self.Awaiting = False

            # append startingPositions list to SavedStartingPositions, clear startingPositions
            self.SavedStartingPositions.append(self.movementobject.startingPositions)
            self.movementobject.startingPositions = []

            self.count += 1
            time.sleep(0.5)  #

            # end sell loop

        self.button3 = tk.Button( text='Execute', command=SellThrice)
        self.canvas.create_window(250, 50, window=self.button3)

        # Generates and shows boundary on init.
        ScreenCap()

        # Curve Evolution button
        # currently using last saved curve, which is weird
        def Evolve():
            # move normally
            self.movementobject.MoveToRandom((300, 900), self.movementobject.savedCurves[1], (100, -100), (0, 0), (0, 0))

            # move evolved
            #superGigaCurve = Functions.EvolveCurve(self.movementobject.savedCurves[1], 10)
            #self.movementobject.MoveToRandom((300, 900), superGigaCurve, (800, -800), (0, 0), (0, 0))
            pass

        self.button6 = tk.Button(text='EVOLVE!!!!!!!', command=Evolve)
        self.canvas.create_window(250, 600, window=self.button6)
        ''' insert '''

        # record/play curve buttons
        def RecordCurve():
            self.movementobject.recordActive = True
            # record update loop

        def StopRecord():
            self.movementobject.recordActive = False
            self.movementobject.Keep()
        def PlayCurve():
            self.movementobject.MoveToRandom((300, 900), self.movementobject.savedCurves[1], (100, -100), (0, 0), (0, 0))

        self.button7 = tk.Button(text='Record', command=RecordCurve)
        self.canvas.create_window(100, 750, window=self.button7)
        self.button8 = tk.Button(text='StopRecord', command=StopRecord)
        self.canvas.create_window(600, 100, window=self.button8)
        self.button9 = tk.Button(text='StopRecord', command=PlayCurve)
        self.canvas.create_window(250, 680, window=self.button9)

    # GUI Methods
    # ADAPT TO BEING A GUI METHOD - RANDOM MOVE FOR MOVE TO DRAGBAR, NORMAL MOVE AFTERWARDS - CHANGE

    def Drag(self, x, y, ydrag, dragtime, stashboundary):
        # pyautogui.moveTo(x, y, )
        pyautogui.drag(0, ydrag, dragtime, button='left')
        cap = WindowCapture('EscapeFromTarkov')
        stashScreenCap = cap.get_screenshot()
        stashScreen = stashScreenCap[54:1086, 258:1189]
        cv.imshow('test', stashScreen)
        XX = Detect(stashScreen, stashboundary, 0.81)
        print(XX)
        return XX

    def LocateStashItem(self, x, y, stashboundary):
        firstDrag = self.Drag(x, y, 9, 0.1, stashboundary)
        XX, YY = GetCursorPos()
        print('at y pos {}'.format(YY))

        for i in range(0, 29):

            if i == 15:
                # Failsafe if no match in fleaStash
                global Exit
                Exit = True
                break
            if firstDrag == []:
                dragY = self.Drag(x, y + 8 + 19 * i, 20, 0.2, stashboundary)
                XX, YY = GetCursorPos()
                print('at y pos {}'.format(YY))

                if dragY != []:
                    return dragY

            if firstDrag != []:
                return firstDrag



''' Defunct '''

'''
# Dropdown menu for stashHeight, stashWidth
        def set_val():
            self.stashWidth = variable1.get()
            self.stashHeight = variable2.get()

        heightOptions = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
        widthOptions = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        variable1 = tk.IntVar(self.master)
        variable2 = tk.IntVar(self.master)
        variable1.set(widthOptions[3])
        variable2.set(heightOptions[3])

        self.menu1 = tk.OptionMenu(self.master, variable1, *widthOptions)
        self.menu2 = tk.OptionMenu(self.master, variable2, *heightOptions)

        ' CURRENT - MAKE COMMAND ON CLICKING DROPDOWN '
        # when clicking dropdown, runs command set_val
        self.canvas.create_window(65, 300, window=self.menu1)
        self.canvas.create_window(165, 300, window=self.menu2) 
        
        # Showing entry contents below button at 'label1'
        def ShowEntry():
            xx1 = self.entry1.get()

            self.label1 = tk.Label(self.master, text=xx1)
            self.canvas.create_window(100, 230, window=self.label1)

        self.button1 = tk.Button( text='Show user input', command=ShowEntry)
        self.canvas.create_window(100, 180, window=self.button1)
        
        # Entry box for user input
        self.entry1 = tk.Entry(self.master)
        self.canvas.create_window(100, 140, window=self.entry1)
'''


'''
DEFUNCT: after they changed the inventory dropdown menu

            if self.currentFiRitem[0] + self.XshiftToStash + self.stashWidthMin*63 >= 1646:     # Depending on pos in stash, moves to filter in dropdown
                # boolean to activate position change rule
                self.movementobject.FilterByItemPos = True
                self.movementobject.MoveToRandom(self.movementobject.startingPositions[2], self.movementobject.savedCurves[0],
                                                 self.movementobject.startingPositions[2],
                                                 (-150, -107),
                                                 (0, 0))
                self.movementobject.FilterByItemPos = False

                # However if there two 'high' rolls to the left,
                #pyautogui.move(-40, 0, 0.5)
            else:
                pass
                #pyautogui.move(140, 0, 0.5)


'''