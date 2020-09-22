# Tarkov Auto-sell (Requires Tarkov open)

import tkinter as tk
import json
import os
from windowCapture import WindowCapture
from matchingFunctions import *
import Functions
from movement import Movement
import GUI2

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


# Make stashBoundary user defined - User can drag it

# - stashwindow will be need to recaptured after an item is sold, or else fleaStash will not match
# - Need to detect euros/dollars and either exempt them or convert them

# How will clicking execute button, execute the function three times until count is 3
# well we have the execute command, simply make it do it 3 times, one after another

''' menu '''
# Waits for user inputs to select certain variables, here FiRItems dictionary generated
    # and a stash boundry template is generated


def Main():
    root = tk.Tk()
    A = Movement()
    A.savedCurves.append(x1)
    A.savedCurves.append(x2)
    G = GUI2.Gui2(root, A)
    root.mainloop()


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
# Utilise multi-processing/multi-threading in drag function to match each frame/or other frame whilst dragging down?
# Drag code is a bit 'iffy' - skipped over match drag screen - when range(2,20)

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

''' Additions? '''
''' Drag stashBoundary '''
#Show an image of the stash, either generated at execute or with a button to take
#Drag across image, record x,y pos and compare to image, to calculate a stashboundary within

# When left-click is held, x,y pos is plugged into function w+floor/ceil func, generates new image with portion of image
# transparent, sets self.stashBoundary to this new image. Upon release, set self.stashBoundary to image of that size
# without transparency


