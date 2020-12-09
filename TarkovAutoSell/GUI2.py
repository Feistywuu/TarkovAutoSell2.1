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
import multiprocessing

# test for curve update loop
import pygame
from pygame.locals import *

''' To Do'''

''' //////////////// THINGS ///////////////  '''

# THE WHOLE MULTIPROCESSING THING
# SellThrice() needs to be written to account for 2 functions                                        (0.1)


' ON IT!!!!!!!!!!!!!!!!!!!!!!!!!'
''' Testing Curve Evolution  '''                                                                    # (0.2)
# Require update loop that records (x,y) to record curves - could use multiprocessing?
# Make indepedent - still uses Curve.txt in main.py
#- if curve.txt is empty, make dummy init curve array

''' Curve Evolution:                                                                                # (0.5)
# when curve is aligned within evolve, thus running through align again in MoveTo() is redundant, except for cases
#when a curve isn't evolved first

# Need to able to test curve evolution
#make button with a function that tests
# Scale the 'Evolved Curve' to the new start and destination.
# For 'human overshoot' let destination be 'random num. + overshoot' then move to 'random num'

'''
# remove curse dependance at start of main                                                              #(1.2)
# make gui update loop exit properly

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