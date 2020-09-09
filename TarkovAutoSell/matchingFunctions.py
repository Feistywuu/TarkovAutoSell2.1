# Runs Matching algorithm for object template vs a background image

import os
import cv2 as cv
import numpy as np
import time

os.chdir('''C:\\Users\\Philip\\Documents\\Programming\\Opencv\\TarkovAutoSell\\Images''')

fir = cv.imread('FiR.png', cv.IMREAD_UNCHANGED)

Numbers = [cv.imread('0.png', cv.IMREAD_UNCHANGED),
           cv.imread('1.png', cv.IMREAD_UNCHANGED),
           cv.imread('2.png', cv.IMREAD_UNCHANGED),
           cv.imread('3.png', cv.IMREAD_UNCHANGED),
           cv.imread('4.png', cv.IMREAD_UNCHANGED),
           cv.imread('5.png', cv.IMREAD_UNCHANGED),
           cv.imread('6.png', cv.IMREAD_UNCHANGED),
           cv.imread('7.png', cv.IMREAD_UNCHANGED),
           cv.imread('8.png', cv.IMREAD_UNCHANGED),
           cv.imread('9.png', cv.IMREAD_UNCHANGED), ]

smolNumbers = [cv.imread('0s.png', cv.IMREAD_UNCHANGED),
               cv.imread('1s.png', cv.IMREAD_UNCHANGED),
               cv.imread('2s.png', cv.IMREAD_UNCHANGED),
               cv.imread('3s.png', cv.IMREAD_UNCHANGED),
               cv.imread('4s.png', cv.IMREAD_UNCHANGED),
               cv.imread('5s.png', cv.IMREAD_UNCHANGED),
               cv.imread('6s.png', cv.IMREAD_UNCHANGED),
               cv.imread('7s.png', cv.IMREAD_UNCHANGED),
               cv.imread('8s.png', cv.IMREAD_UNCHANGED),
               cv.imread('9s.png', cv.IMREAD_UNCHANGED), ]

slash = cv.imread('slash.png', cv.IMREAD_UNCHANGED)

# print(Numbers[1])

# h, w = fir.shape[:2]           #Maybe change to [:-1]?
start_time = time.time()


def Detect(screenshot, image, thresh):
    '''
    Takes an image in np array form, performs matchTemplate algorithm on it,
    checking every pixel.
    The best is recorded in a list, removed from resulting match array,
    then repeated, till the matches are of poor too quality.
    :return: list of Best Matches (x,y) pos
    '''
    threshold = thresh
    MatchedItems = []
    # Dropping alpha channel on image, making C_CONTIGUOUS
    image = image[..., :3]
    image = np.ascontiguousarray(image)
    h, w = image.shape[:2]
    result = cv.matchTemplate(screenshot, image, cv.TM_CCOEFF_NORMED)

    # fake out max_val for first run through loop
    max_val = 1
    while max_val > threshold:
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
        print('About to append; max_val: ' + str(max_val))

        if max_val > threshold:
            # appending x,y of match to list
            MatchedItems.append((max_loc[0], max_loc[1]))

            # slicing result array, replacing best match location with 0's.)
            # cv.imshow('123123',result)
            result[max_loc[1] - h // 2 + 4:max_loc[1] + h // 2 + 1, max_loc[0] - w // 2:max_loc[0] + w // 2 + 1] = 0
            # cv.imshow('zxczxc',result)
            test = cv.rectangle(screenshot, (max_loc[0], max_loc[1]), (max_loc[0] + w + 1, max_loc[1] + h + 1), (0, 255, 0))
            # cv.imshow('test',test)

            # print('Best match top left position: %s' % str(max_loc))
            # print('Best match confidence: %s#' % max_val)

    return MatchedItems

# Size of screenshot must be larger by template/2 in each x,y, since upon match location, we slice result array
# width/height either side of max_loc to prevent a match from the same object

# Make numbers smaller, do black space doesn't add to match weight

# Can make rules to provide corrections via context, ie bounds between
# above/below listings:

# After a number has been successfully matched, remove it from pool of
# matches, so in '5600', it matches 0 three times, then after confirming a better
# match of 5&6 it will use those instead... requires template to match better
# to respective numbers + knowing number of digits/dim of pool i.e
# number of digits cannot change,
# or else a false positive could just be a new number

'Errors'

# Stuck in 'while max_val > threshold:'
# since result not updating, since result slicing would do something like [-2:19], because the
# the bounds of the result array is too small compared to the size of the square to be inserted.
'Solution:'  # Manually decrease square size by 2, to fit result array

'Matching Data'

'5998'
# FalsePositions:
# 3: {8/9:0.723, }
# 6: {5?:0.803, }
# 8: {5/9??:0.742, }

'5600'
# 0 {5/6:0.906, }
# 8 {6/0?:0.797, }











