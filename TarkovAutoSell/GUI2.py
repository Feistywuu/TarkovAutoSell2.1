# GUI for user inputs for main()

import tkinter as tk
import pyautogui
import time
import Functions
from PIL import Image, ImageTk
from windowCapture import WindowCapture
from matchingFunctions import *
from movement import Movement

''' Goals '''

# Dropdown box with selection of rules
# Entry boxes to enter variables for chosen rules

# Do I want GUI still open during main loop?
# If so: insert gui main loop into main() and replace pygame events with user input in GUI

# do i have to create a GUI object each time it changes firitem?
# no: place dictionary within creategui class
# - Create button which generates the FiRItems dictionary within gui class
# dictionary are unordered, so count should change which location is chosen rather than index of dictionary

#make x1,x2 attributes of movement class
# Make button: opens screen where you can draw the curve, then append to attribute A.savedCurves
# for now hardcoded

# firdict can be generated with a button later, as opposed to on init.
#integrate first with dict predetermined

#Display current item

# Can self.stashBoundary change upon self.height,self.width changing upon dropdown select?

'''
CLICKED 0 39
CLICKED 987 1077
'''

''' Required user prep - tarkov screen must be on the stash'''

''' To DO'''
# In FiRItems(), assign self.FiRdict ... =

# Issue with detection, why is fleaStash and self.stashBoundary different?
# Both use the get_screenshot() function.
# Make test detect() function, some pre-defined screencaps, display and compare them.

class Gui2:

    def __init__(self, master, movementobject):
        self.master = master
        self.movementobject = movementobject
        self.stashBoundary = []
        self.FiRdict = [0]                      # defined in firdict func
        self.count = 0
        self.Awaiting = True
        self.stashHeightMin = 0
        self.stashWidthMin = 0
        self.stashWidthMax = 4      #10
        self.stashHeightMax = 4     #14
        self.stashimg = []
        self.currentitem = []                   # set when FiRitems generated

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
        self.canvas.create_window(200, 340, window=self.bot2)
        self.left1 = tk.Button(text='Left', command=Left)
        self.canvas.create_window(150, 270, window=self.left1)
        self.right1 = tk.Button(text='Right', command=Right)
        self.canvas.create_window(250, 270, window=self.right1)

        # Test Detect() function.
        def test():
            '''
            Shows functions of Detect() function.
            #1 Test between cv.imshow(fleaStash) and stashBoundary
            #2
            :return:
            '''

            # Errors in detection... then:
            # Errors loading images, related to image colour swap?

            # First Image
            test3img = test333[154:600, 350:650]
            #np.uint8(test3img)
            test333img = ImageTk.PhotoImage(image=Image.fromarray(test3img))
            self.canvas.create_image(300, 600, anchor="nw", image=test333img)
            print(test333img)
            cv.imshow('tqweaewssdf', test333img)

            ''' LINE 219 image ONLY APPEARS WHEN LINE 221 is there? Why? And then resulting picture is RGB colour swapped?'''

            # Second Image
            self.testimg = ImageTk.PhotoImage(image=Image.fromarray(self.stashBoundary))
            self.canvas.create_image(50, 600, anchor="nw", image=self.testimg)

        self.button6 = tk.Button(text='test detect', command=test)
        self.canvas.create_window(50, 550, window=self.button6)

        # Generate stashBoundary Button
        def ScreenCap():

            # Instance of Window in np array form
            wincap = WindowCapture('EscapeFromTarkov')
            TarkovScreenN = wincap.get_screenshot()
            self.stashBoundary = TarkovScreenN[77 + 63 * self.stashHeightMin:77 + 63 * self.stashHeightMax, 1264 + 63 * self.stashWidthMin:1264 + 63 * self.stashWidthMax]

            # Convert into displayable form
            self.stashimg = ImageTk.PhotoImage(image=Image.fromarray(self.stashBoundary))

            # Shows self.stashBoundary
            self.canvas.create_image(300, 100, anchor="nw", image=self.stashimg)

        # Generate FiRItems from stashBoundary
        def FirItems():
            '''
            Detects FiRitems in user defined self.stashBoundary; Generates self.FiRdict
            :return: self.FiRdict
            '''
            # Detect FiRItems in stashBoundary
            FiR = Detect(self.stashBoundary, fir, 0.8)

            # Check position of FiR match, then take the containing square as a template
            # Create dictionary of { ((itempos, itemcap), ... (pos,cap)) }
            self.FiRdict = {}
            for item in FiR:
                templateX = item[0] + (63 - item[0] % 63)  # Transforming to nearest multiple of 63 above
                templateY = item[1] + (63 - item[1] % 63)
                template = self.stashBoundary[templateY - 63:templateY, templateX - 63:templateX]
                self.FiRdict.update({item: template})

        self.button4 = tk.Button(text='Generate FiR items list', command=FirItems)
        self.canvas.create_window(100, 450, window=self.button4)

        # Execute button
        def SellItem():
            '''
            Takes a new Screenshot of stashBoundary - generates self.FiRdict, self.FiRItem, self.stashBoundary and
            self.currentItem. Then, self.count += 1
            :return: Item is sold
            '''


            # Choosing a FiR item
            self.FiRItem = list(self.FiRdict)[self.count]
            print(self.FiRItem)

            # Moving to FiRitem
            pyautogui.moveTo(self.FiRItem[0] + 1264, self.FiRItem[1] + 77, 2)   # Moving to FiR item
            pyautogui.click(button='right')                                     # Open 'filter by item'
            pyautogui.move(10, -78, 0.5)
            time.sleep(1)
            pyautogui.click(button='left')                                      # Clicks it
            time.sleep(1)
            self.movementobject.moving = True

            # Moving from 'filter by item' > 'add offer'
            self.movementobject.MoveTo((self.FiRItem[0] + 1254, self.FiRItem[1] - 1), (1300, 75), self.movementobject.savedCurves[0])

            # Calculating values from listings
            Functions.GetValue()

            # Click 'add offer'
            pyautogui.click(button='left')
            time.sleep(1)

            # Find stashBoundary in flea market stash
            cap = WindowCapture('EscapeFromTarkov')
            stashScreenCap = cap.get_screenshot()
            # fleaStash = stashScreenCap[204:931, 408:1039]
            fleaStash = stashScreenCap[54:1086, 258:1189]
            cv.imshow('test', fleaStash)

            # Run matching algorithm - objectMatch(fleaStash, stashBoundary), select obj.
            # if false, click on bar, drag down, repeat until match found
            XX = Detect(fleaStash, self.stashBoundary, 0.81)
            if XX == []:
                fleaStashBoundaryLoc = Functions.LocateStashItem(1044, 323, self.stashBoundary)
            else:
                fleaStashBoundaryLoc = XX

            # Move to stashBoundary match within fleaStash
            fleaStashBoundaryLoc = fleaStashBoundaryLoc[0][0] - 150, fleaStashBoundaryLoc[0][
                1] - 150  # Adjusting for x,y, w.r.t fleaStash
            fleaStashLoc = fleaStashBoundaryLoc[0] + 410, fleaStashBoundaryLoc[
                1] + 206  # Adjusted x,y w.r.t fleaStash on screen + offset by 2/2 BotRight
            pyautogui.moveTo(fleaStashLoc[0], fleaStashLoc[1])
            print('stashBoundary at ' + str(fleaStashLoc) + ' on-screen')
            time.sleep(1)  #

            # Move to FiRItem location; within the stashBoundary; within the fleaStash
            print(fleaStashLoc[0] + self.FiRItem[0])
            print(fleaStashLoc[1] + self.FiRItem[1])
            time.sleep(1)  #
            self.movementobject.MoveTo(pyautogui.position(),
                                       (fleaStashLoc[0] + self.FiRItem[0], fleaStashLoc[1] + self.FiRItem[1]),
                                       self.movementobject.savedCurves[1])

            # Click Object
            time.sleep(0.1)
            pyautogui.click(button='left')

            # Creating loop for movement to '+'
            self.movementobject.MoveTo(pyautogui.position(), (1462, 500), self.movementobject.savedCurves[1])

            # Click it, Moving to 'Currency', clicking it
            pyautogui.click(button='left')
            self.movementobject.MoveTo(pyautogui.position(), (996, 197), self.movementobject.savedCurves[0])
            time.sleep(0.1)
            pyautogui.click(button='left')
            time.sleep(0.5)

            # Typing Value - 1
            TheValue = Functions.Matches[0] - 1
            strValue = str(TheValue)
            keys = []
            for digit in strValue:
                keys.append(digit)
            pyautogui.write(keys, interval=0.15)

            # Moving to 'add', clicking it
            self.movementobject.MoveTo(pyautogui.position(), (962, 899), self.movementobject.savedCurves[0])
            time.sleep(0.1)
            pyautogui.click(button='left')

            # Moving
            self.movementobject.MoveTo(pyautogui.position(), (1274, 893), self.movementobject.savedCurves[1])
            time.sleep(0.1)

            time.sleep(1)  #
            pyautogui.click(button='left')
            print('item sold')
            pyautogui.press('esc')
            self.Awaiting = False

            # Why is match location on the left side center of FiRItem?
            # i.e the detect location in drag

            self.count += 1
            time.sleep(1)  #

        self.button3 = tk.Button( text='Execute', command=SellItem)
        self.canvas.create_window(250, 50, window=self.button3)

        # Generates and shows boundary on init.
        ScreenCap()

        # CurveCalc button
        ''' insert '''





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