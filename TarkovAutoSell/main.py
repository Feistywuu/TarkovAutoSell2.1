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




def Main():

    def WaitThenDetect(e):
        """Wait for the event to be set before doing anything"""
        print('wait_for_event: starting')
        e.wait()
        print('wait_for_event: e.is_set()->', e.is_set())
        if e.is_set == True:
            # receive arguements from GUI

            # Run Detect algorithm
            detect1 = Detect()

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

    # Four processes: main(?), GUI, Detect, Record

    # want MoveTo in 'GUI' Process to intiate when condition(bool() is changed to true in 'Detect'))
    #could use events instead, since we are only using single processes in parallel

    # May need to use lock to organise access to Detect() output.

    # We can use put() into the Queue() to pass bool information
    #we pass the flag variable around the queue, then it runs function defined in main with functions ref. from imports.

    if __name__ == '__main__':
        e1 = multiprocessing.Event()
        e2 = multiprocessing.Event()
        DetectProcess = multiprocessing.Process(name='Detect',
                                                target=WaitThenDetect,
                                                args=(e1,))
        RecordProcess = multiprocessing.Process(name='Record',
                                                target=WaitThenRecord,
                                                args=(e2,))
        GUIProcess = multiprocessing.Process(name='GUI')

        # prepare and start GUI process
        root = tk.Tk()
        A = Movement()
        A.savedCurves.append(x1)
        A.savedCurves.append(x2)
        G = GUI2.Gui2(root, A)
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




Main()

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


