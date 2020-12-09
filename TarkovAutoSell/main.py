# Tarkov Auto-sell (Requires Tarkov open)

import tkinter as tk
import json
import os
from windowCapture import WindowCapture
from matchingFunctions import *
import Functions
from movement import Movement
import GUI2
import multiprocessing
import time

# gui
from tkinter import messagebox
import pyautogui
from PIL import Image, ImageTk
import sys
from win32api import GetCursorPos



# Importing Curves from Curves.txt
os.chdir('''C:\\Users\\Philip\\Documents\\Programming\\Opencv\\TarkovAutoSell''')
Save = open(os.path.join('''C:\\Users\\Philip\\Documents\\Programming\\Opencv\\TarkovAutoSell\\CurveCalculator''',
                         'Curves.txt'))
try:
    x = json.load(Save)
    x1 = np.array(x[0])
    x2 = np.array(x[1])
except IndexError:
    print('not 2 saves')



# If we have SellItem() and SellItem2() defined in main.py,
#when a button is pressed in GUI2, how can we relay that information to main?
# either have main + gui in one? or?

'''         /////////CURRENT//////////////              '''

''' DragNDetect '''
# Define SellItem() in GUI to end at DragnDetect()
# Create function that runs when bool() statement is satisfied i.e. 'if Detected == True:'
# DragNDetect sends information through Queue to GUI process to invoke() (trigger button) in GUI:
# Automatically continues SellItem as the rest of said function

'DragNDetect sends bool information through Queue to Gui process (root.mainloop()) ' #kaput

' Test whether main.py has access to button pressed in root.main()'
'CURRENT'


' Test Server Memory with Queue'
# Import multiprocessing in both files
# put into queue in one file
# put into queue in the other file

' TEST QUEUE BUTTON'
# event with bool condition, false by default
# put bool into Queue
# activate button using bool condition
# check result

' TEST QUEUE + INVOKER() '
# button that does something
# put button.invoker() into Queue
# check result

# User presses button - triggers event, root.mainloop() detects this
# root.mainloop() puts() information into queue
# other processes receive information from the queue

'Start with Record() as a simple example'
# User presses button in GUI > root.main() detects this
# root.mainloop() puts() info into the queue



class Gui2:

    Exit = False

    def __init__(self, master, movementobject, q):
        self.queue = q
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
        self.TestBool = True

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

        ' TESTESTSETSETSWETSETSETSET '
        # TEST button which prints information from Queue
        def ShowQueue():
            print(self.queue)

        self.button20 = tk.Button(text='TESTQUEUE', command=ShowQueue)
        self.canvas.create_window(100, 50, window=self.button20)

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

            '''Process needs to pause here*****'''
            '''DETECTION/DRAG FUNCTION NOW IN MAIN.PY'''


        self.button3 = tk.Button( text='Execute', command=SellThrice)
        self.canvas.create_window(250, 50, window=self.button3)

        def SellItem2():
            '''
            Second half of SellItem() algorithm, invoked through queue
            '''

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

        self.button10 = tk.Button(text='Execute', command=SellItem2)
        self.canvas.create_window(250, 700, window=self.button10)           # probably not needed (remove later)

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
            print('Record == Active')
            self.movementobject.recordActive = True

            # puts event set information into queue

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


def WaitThenDetect(e):
    """Wait for the event to be set before doing anything"""
    print('wait_for_event: starting')
    e.wait()
    print('wait_for_event: e.is_set()->', e.is_set())
    if e.is_set == True:
        # receive argument from

        # Run Detect algorithm
        #detect1 = Detect()

        # Send information to GUI process
        pass


def WaitThenRecord(e):
    """ Wait for the event to be set before doing anything"""
    print('wait_for_event: starting')
    e.wait()
    print('wait_for_event: e.is_set()->', e.is_set())
    if e.is_set == True:
        # receive arguments from GUI
        # Run Record algorithm
        # Send information to GUI process
        pass


def DragNDetect():
    '''
    Executes an initial Detect.
    (1) Process drags down the fleastash, takes screenshot at intervals, sends to Queue and sets event.
    (2) Process Detects screenshot for self.stashBoundary, upon detect, 'break' process (1).

    (1) is GUI update loop - How to access?

    :return:
    '''


    XX = Detect(fleaStash, self.stashBoundary, 0.81)
    if XX == []:
        fleaStashBoundaryLoc = self.LocateStashItem(1044, 323, self.stashBoundary)
    else:
        fleaStashBoundaryLoc = XX


# Four processes: main(?), GUI, Detect, Record

# want MoveTo in 'GUI' Process to intiate when condition(bool() is changed to true in 'Detect'))
#could use events instead, since we are only using single processes in parallel

# May need to use lock to organise access to Detect() output.

# We can use put() into the Queue() to pass bool information
#we pass the flag variable around the queue, then it runs function defined in main with functions ref. from imports.

if __name__ == '__main__':
    queue = multiprocessing.Queue()
    e1 = multiprocessing.Event()
    e2 = multiprocessing.Event()
    DetectProcess = multiprocessing.Process(name='Detect',
                                            target=WaitThenDetect,
                                            args=(e1,))
    RecordProcess = multiprocessing.Process(name='Record',
                                            target=WaitThenRecord,
                                            args=(e2,))
    GUIProcess = multiprocessing.Process(name='GUI')

    queue.put('testingtesting')

    # prepare and start GUI process
    root = tk.Tk()
    A = Movement()
    A.savedCurves.append(x1)
    A.savedCurves.append(x2)
    G = Gui2(root, A, queue)
    root.mainloop()
    # GUIProcess.start()                                - Possibly needed? otherwise: Instantiate G makes process

    while True:

        # set Detect process
        if e1.is_set() == True:
            DetectProcess.start()
            # transfer information to GUI
            # join()

        # set Record Process
        if e2.is_set() == True:
            RecordProcess.start()
            # transfer information to GUI
            # join()

        #processes may need lock state at first
        # unlocked when condition is changed.
        # - How can this be changed from the GUI Process? - they are imported



' TO DO '

# Main Moveto() functions
# Allow only specified bounds of stash to be searched for FiR items - show the stash bounded in the GUI
# Only check stash for FiR items
# Scale dimensions for any monitor size
# complete loop
# Clean up code
# Take median of last 3 results - let users customize certain rules
# Make containers(things with a tag) and/or vests/backpacks not eligible
# Allow somehow to grab all prices, then allow a review before selling the items
# Can't I remove 'Matches' from Functions if I declare it as global within the function?
# Utilise multi-processing/multi-threading in drag function to match each frame/or other frame whilst dragging down?
# Drag code is a bit 'iffy' - skipped over match drag screen - when range(2,20)

'''Errors'''

'''Notes'''
# Can use multiprocessing to run processes concurrently with the GUI main update loop but how would we without that?
# maybe when another update loop would be required, save required data, end process and start the other update loop?

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

''' Additions? '''
''' Drag stashBoundary '''
#Show an image of the stash, either generated at execute or with a button to take
#Drag across image, record x,y pos and compare to image, to calculate a stashboundary within

# When left-click is held, x,y pos is plugged into function w+floor/ceil func, generates new image with portion of image
# transparent, sets self.stashBoundary to this new image. Upon release, set self.stashBoundary to image of that size
# without transparency


