# Functions e.g. quickSort
# Maybe Match Class?

import pyautogui
import numpy as np
from matchingFunctions import *
from windowCapture import WindowCapture
import random


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

    # clear 'Matches' variable
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

    # Takes screencap of listings, then determines the value
    cap = WindowCapture('EscapeFromTarkov')
    capn = cap.get_screenshot()

    # Determine value of lowest bids
    # Creating list of sub-images where prices appear, to match against
    listings = []
    for i in range(0, 13):
        listing = capn[155 + 72 * i:190 + 72 * i, 1341:1487]
        listings.append(listing)

    cap = WindowCapture('EscapeFromTarkov')                         # might be redundant, need to test
    capn1 = cap.get_screenshot()

    listings1 = []
    for i in range(0,13):
        listing1CurrencySign = capn1[155 + 72 * i:190 + 72 * i, 1370:1480]
        listings1.append(listing1CurrencySign)

    # Detect currency type for each listing, store in list
    ListingCurrency = []
    for i in range(len(listings1)):
        for j in range(len(CurrencyTypes)):
            print('Currently on listing: ' + str(i) + '. Checking for Currency ' + str(j))
            currencyDetect = Detect(listings1[i], CurrencyTypes[j], 0.85)
            if currencyDetect == []:
                ListingCurrency.append('Ruble')
                continue
            if currencyDetect != [] and j == 0:
                ListingCurrency.append('Dollar')
                print('dollar listing detected at {}'.format(currencyDetect))
                continue
            if currencyDetect != [] and j == 1:
                ListingCurrency.append('Euro')
                print('euro listing detected at {}'.format(currencyDetect))

    # Iterating through Numbers for each Listing; detecting
    for i in range(len(listings)):
        for j in range(len(Numbers)):
            # print('Listing: ' + str(i) + '  Number: ' + str(j))
            B = Detect(listings[i], Numbers[j], 0.85)

            # Making Match objects from Detect() list output
            for match in B:
                matchObject = Match(i, j, match[0], match[1])
                Matches[i].append(matchObject)

    # determine position of each digit in listing: sorting Matchobjects by match.x
    for listing in Matches:
        input_1 = listing
        list_length = len(listing)
        quickSort(listing, 0, list_length - 1)

    # Displaying values for each Match
    for listing in Matches:
        for i in range(len(listing)):
            listing[i] = listing[i].value

    # Add each digit together to form a totalValue
    for listing in Matches:
        for i in range(len(listing)):
            if i == 0:
                totalValue = listing[0]
            if i > 0:
                totalValue = int(str(totalValue) + str(listing[i]))
            if i == range(len(listing))[-1]:
                Matches[Matches.index(listing)] = totalValue

    # convert currencies
    for i in range(len(Matches)):
        if ListingCurrency[i] == 'Dollar':
            Matches[i] = Matches[i]*125
            print('Converted from Dollars '+ str(Matches[i]))
        if ListingCurrency[i] == 'Euro':
            Matches[i] = Matches[i]*146
            print('Converted from Euros ' + str(Matches[i]))

    for row in Matches:
        print('totalValue: ' + str(row))


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


def ChooseRandomInt(xrange, yrange):
    '''
    Takes ranges of x,y - (xmin,xmax) etc. and chooses a random integer lying within each boundary.
    :return: (x,y)
    '''
    try:
        xmin, xmax = xrange
        x = random.randint(xmin, xmax)
    except ValueError:
        x = 0
    try:
        ymin, ymax = yrange
        y = random.randint(ymin, ymax)
    except ValueError:
        y = 0

    return x, y


    # probably doesn't want to be a class method, so that it can work independendlty within the
    # other multi-processing loop?
    # Because the main movement object is updated real time as the mouse moves according to it.
    # Thus the EvolveCurve needs to work on some alternate/dummy variable, maybe dummy.movementobject?
    # CHANGE TO METHOD LATER
def EvolveCurve(curve, X):
    '''
    Takes a existing mouse movement (curve in array form) and runs an algorithm on it, altering so that it
    resembles the original but with slight unpredictable deviations.
    Splits the curve into N segments, works out a deviation factor for each segment and then multiplies each
    respective segment by the factor:
    xyTotal = total number of datapoints in the curve.
    - Choose a value N, where N is 5 >= N >= 1
    This determines the amount of curve segments.
    - Construct a straight line array (linearEqn) from (start > destination). Find the angle of this array
    -from the closest anti-clockwise axis.
    - Calculate distance of every point on 'curve' from 'linearEqn' at iteration 'i'.
    - Rotate this distance by previous angle - (distance*cos(angle)) - to find component orthogonal to linearEqn
    - Calculate deviation for this distance metric for each segment.
    - For each curve segment, multiply every datapoint position by the deviation factor, governed by:
    deviationFactor = sum(N)/(N*deviationMedian).
    - Value will be close to 1. This uses the variability in the ratio mean/median to alter values by small but
    unpredictable amounts.
    - Repeat above X times (10~)
    - May require cleaning irregularities in the curve
    :param curve: array
    :param X: int
    :return: array
    '''
    # maybe not a good idea to mix np.arrays + tuple lambda operations
    datapointSum = len(curve)

    # ensure curve starts at [0,0]
    curve = curve - curve[0]
    dest = curve[-1]

    # get angle using arc tan, if solution is negative, we add pi/2 giving us the acute angle needed
    angleEx = math.atan(dest[1] / dest[0])
    print(angleEx)
    if angleEx < 0:
        angleEx += angleEx + math.pi / 2
        print(angleEx)

    # straight line equation
    def linearEqn(dest1, datapointSum1):
        eqn = np.array([])

        for t in range(datapointSum1):
            np.append(eqn, [math.floor(dest1[0] / dest1[1]) * t, math.floor(dest1[1] / dest1[0]) * t])

        return eqn

    linear = linearEqn(dest, datapointSum)
    print(linear)

    # repeat evolution X times
    for iteration in range(0, X):

        # iterate over curvepoints, compare to expected curve 'linearEqn'
        deltaList = np.array([])
        for i in range(len(curve)):
            # return delta curve starting at (0,0)
            deltaN = np.add(-curve[i], linear[i])
            print(deltaN)
            deltaNsquared = math.sqrt(math.pow(deltaN[0], 2) + math.pow(deltaN[1], 2))

            # compute orthogonal component
            delta = deltaNsquared * math.cos(angleEx)
            np.append(deltaList, delta)

        print(deltaList)
        # Now we have have a delta metric in an array, mapped for every point in in curve/linear
        # calculate deviations from deltaList
        # (1)
        deltaArray = np.array([])
        N = random.randint(2, 5)
        remainder = datapointSum % N
        print(remainder)

        # iterate through segments of curve/linear curve
        for n in range(0, N):
            k = random.randint(0, 1)
            deltaNSum = 0
            deltaNMedian = []
            # add remainder term on last segment
            if n == range(0, N)[-1]:
                # iterate through each datapoint in a segment
                for m in range(math.floor(datapointSum / N) * n, math.floor(datapointSum / N) * (n + 1) + remainder):
                    # sum of deltaN[m] in range
                    deltaNSum += deltaList[m]

                    # median of deltaN[m] in range
                    deltaNMedian = deltaNMedian.append(deltaList[m])
                    deltaNMedian = statistics.median_grouped(deltaNMedian)

                    # more chaos, depend floor/ceil of median on coinflip
                    if k == 0:
                        deltaNMedian = math.floor(deltaNMedian)
                    if k == 1:
                        deltaNMedian = math.ceil(deltaNMedian)
            else:
                for m in range(math.floor(datapointSum / N) * n, math.floor(datapointSum / N) * (n + 1)):
                    # sum of deltaN[m] in range
                    deltaNSum += deltaList[m]

                    # median of deltaN[m] in range
                    deltaNMedian = deltaNMedian.append(deltaList[m])
                    deltaNMedian = statistics.median_grouped(deltaNMedian)

                    # more chaos, depend floor/ceil of median on coinflip
                    if k == 0:
                        deltaNMedian = math.floor(deltaNMedian)
                    if k == 1:
                        deltaNMedian = math.ceil(deltaNMedian)

            # calculate deviation factor
            if n == range(0, N)[-1]:
                deviation = deltaNSum / len(range(0, (math.floor(datapointSum / N)) + remainder)) * deltaNMedian
            else:
                deviation = deltaNSum / len(range(0, math.floor(datapointSum / N))) * deltaNMedian
            print(deviation)

            # times each element in deltaList by deviation factor of each segment, append to deltaArray

            if n == range(0, N)[-1]:
                for m in range(math.floor(datapointSum / N) * n, math.floor(datapointSum / N) * (n + 1) + remainder):
                    np.append(deltaArray, deltaList[m] * deviation)
                    pass
            else:
                for m in range(math.floor(datapointSum / N) * n, math.floor(datapointSum / N) * (n + 1)):
                    np.append(deltaArray, deltaList[m] * deviation)
            print(deltaArray)

        # add new delta to expected curve
        curve = np.add(linear, deltaArray)

    # Here we can clean/fit so it is similiar to original curve

    return curve

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
