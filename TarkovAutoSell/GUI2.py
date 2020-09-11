# GUI for user inputs for main()

import tkinter as tk
import pyautogui
import time

''' Goals '''
#Create a genereate stash boundary button in gui
# Show an image of the stash, either generated at execute or with a button to take
# Drag across image, record x,y pos to calculate a stashboundary within
# Display stashboundary in place of the image of the stash
# Display current item

# Dropdown box with selection of rules
# Entry boxes to enter variables for chosen rules

# Do I want GUI still open during main loop?
# If so: insert gui main loop into main() and replace pygame events with user input in GUI

# do i have to create a GUI object each time it changes firitem?
# no: place dictionary within creategui class
# - Create button which generates the FiRItems dictionary within gui class

def MoveToFiR(firitem, movementobject):
    pyautogui.moveTo(firitem[0] + 1264, firitem[1] + 77, 2)         # Moving to FiR item
    pyautogui.click(button='right')                                 # Open 'filter by item'
    pyautogui.move(10, -78, 0.5)
    time.sleep(1)
    pyautogui.click(button='left')                                  # Clicks it
    time.sleep(1)
    movementobject.moving = True

# firdict can be generated with a button later, as opposed to on init.


class CreateGui:
    def __init__(self, master, movementobject, firdict):
        self.master = master
        self.movementobject = movementobject
        self.firdict = firdict
        self.FiRItem = None

        # Main background window
        self.canvas = tk.Canvas(root, width = 400, height = 300)
        self.canvas.pack()

        # Entry box for user input
        self.entry1 = tk.Entry(root)
        self.canvas.create_window(200, 140, window=self.entry1)

        # Showing entry contents below button at 'label1'
        def ShowEntry():
            x1 = self.entry1.get()

            self.label1 = tk.Label(root, text=x1)
            self.canvas.create_window(200, 230, window=self.label1)

        self.button1 = tk.Button( text='Show user input', command=ShowEntry)
        self.canvas.create_window(200, 180, window=self.button1)

        # Quit Button
        def close_window():
            root.destroy()
            print('Stopped')

        self.button2 = tk.Button( text='Quit...?', command=close_window)
        self.canvas.create_window(100, 100, window=self.button2)

        ''' User-Input Commands'''

        # Execute button
        #self.button3 = tk.Button( text='Execute', command=MoveToFiR())

    def FirItemLoop(self):
        '''
        Sets current FiRitem iterated over in GUI
        :return:
        '''
        for FiRItem in self.FiRDict:
            self.FiRItem = FiRItem

root = tk.Tk()
G = CreateGui(root)
root.mainloop()

