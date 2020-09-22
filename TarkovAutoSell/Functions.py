# Functions e.g. quickSort
# Maybe Match Class?

import pyautogui
import numpy as np
from matchingFunctions import *
from windowCapture import WindowCapture

Matches = [[],
           [],
           [],
           [],
           [],
           [],
           [],
           [],
           [],
           [],
           [],
           [],
           [], ]

def partition(input_list, low, high):
    i = (low - 1)
    pivot = input_list[high].x
    for j in range(low, high):
        if input_list[j].x <= pivot:
            i = i + 1
            # i is a marker for the last input_value <= pivot
            # Swaps last number iterated over, higher than pivot(input_list[i])
            # with input_value[j]
            # Lastly, swapping pivot to the end of low
            input_list[i], input_list[j] = input_list[j], input_list[i]
    # Moves higher
    input_list[i + 1], input_list[high] = input_list[high], input_list[i + 1]
    return (i + 1)


def quickSort(input_list, low, high):
    if low < high:
        partition_index = partition(input_list, low, high)
        quickSort(input_list, low, partition_index - 1)
        quickSort(input_list, partition_index + 1, high)


def GetValue():
    '''
    Determines value of listings first page, searches pre-determined areas
    for listings, object matches number templates with the listings,

    '''
    # Takes screencap of listings, then determines the value
    cap = WindowCapture('EscapeFromTarkov')
    capn = cap.get_screenshot()

    # Determine value of lowest bids
    # Creating list of sub-images where prices appear, to match against
    listings = []
    for i in range(0, 13):
        listing = capn[155 + 72 * i:190 + 72 * i, 1341:1487]
        listings.append(listing)

    # Iterating through Numbers for each Listing; detecting
    for i in range(len(listings)):
        for j in range(len(Numbers)):
            # print('Listing: ' + str(i) + '  Number: ' + str(j))
            B = Detect(listings[i], Numbers[j], 0.8)

            # Making Match objects from Detect() list output
            for match in B:
                matchObject = Match(i, j, match[0], match[1])
                Matches[i].append(matchObject)

    # Sorting Match objects but Match.x value
    for listing in Matches:
        input_1 = listing
        list_length = len(listing)
        quickSort(listing, 0, list_length - 1)

    # Displaying values for each Match
    for listing in Matches:
        for i in range(len(listing)):
            listing[i] = listing[i].value

    # Determining totalValue and assigning to each listing in Matches
    for listing in Matches:
        for i in range(len(listing)):
            if i == 0:
                totalValue = listing[0]
            if i > 0:
                totalValue = int(str(totalValue) + str(listing[i]))
            if i == range(len(listing))[-1]:
                Matches[Matches.index(listing)] = totalValue

    for row in Matches:
        print('totalValue: ' + str(row))


def Drag(x, y, currentItem):
    pyautogui.moveTo(x, y, )
    pyautogui.drag(0, 100, 1, button='left')
    print('Dragged')
    cap = WindowCapture('EscapeFromTarkov')
    stashScreenCap = cap.get_screenshot()
    stashScreen = stashScreenCap[54:1086, 258:1189]
    #stashScreen = stashScreenCap[0:1200, 100:1300]
    cv.imshow('test', stashScreen)
    XX = Detect(stashScreen, currentItem, 0.81)
    print(XX)
    return XX


def LocateStashItem(x, y, currentItem):
    firstDrag = Drag(x, y, currentItem)

    for i in range(1, 20):

        if i == 9:
            time.sleep(30)          # loop fail-safe
        if firstDrag == []:
            dragY = Drag(x, y + 100 * i, currentItem)

            if dragY != []:
                return dragY

        if firstDrag != []:
            return firstDrag


def initAndClear():
    '''
    Empties contents of 'Matches'
    :return:
    '''

    global Matches

    Matches = [[],
               [],
               [],
               [],
               [],
               [],
               [],
               [],
               [],
               [],
               [],
               [],
               [], ]

class Match():

    def __init__(self, listing, value, x, y):
        self.listing = listing
        self.value = value
        self.x = x
        self.y = y

    # Function that adds each object it runs through to

    def Value(self, MatchesForListing):
        '''
        Called on an arbitrary Match object, but...
        Sorts all current Match objects(in 'Matches' list) for each listing,
        by x value then builds a total Value from each Match self.value
        :param: list, value, x, y
        '''
