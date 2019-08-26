#-------------------------------------------------------------------------------
# Name:        Go board recognition project
# Purpose:     Watershed function (OpenCV version)
#
# Author:      skolchin
#
# Created:     20.08.2019
# Copyright:   (c) skolchin 2019
#-------------------------------------------------------------------------------

import cv2
import numpy as np

# Apply watershed transformation
# The algorithm derived from OpenCV's publication 'Image Segmentation with Watershed Algorithm'
# and adopted to use stone coordinations as an indicators of peaks
# instead of original "max peak value" method
def apply_watershed(gray, stones, n_thresh, f_bw, f_debug = False):
    # Prepare gray image
    if f_bw == 'B':
       # To have watershed properly determine black stones, board dividers
       # have to be removed with dilation
       kernel = np.ones((3, 3), dtype = np.uint8)
       gray = cv2.dilate(gray, kernel, iterations = 1)
       gray = cv2.bitwise_not(gray)

    if f_debug:
       cv2.imshow('Gray', gray)

    # Prepare thresholded image
    _, thresh = cv2.threshold(gray, n_thresh, 255, cv2.THRESH_BINARY)
    if f_debug: cv2.imshow('Threshold', thresh)

    #b = np.zeros(stones.shape, dtype = np.bool)
    #b[7] = 1
    #stones = stones[b].reshape(1, stones.shape[1])

    # Prepare peaks map
    peaks = np.zeros(thresh.shape, dtype = np.uint8)
    for i in range(len(stones)):
        x = int(stones[i,0])
        y = int(stones[i,1])

        if thresh[y,x] > 0:
           #cv2.circle(peaks, (x,y), 1, (i+1), -1)
           peaks[y,x] = (i+1)
        else:
           # Circle center falls to black point
           # Loop around to find white point on thresholded image
           r = 5
           r2 = r*2
           f = False
           for dy in range(r2+1):
               for dx in range(r2+1):
                   vy = y+r-dy
                   vx = x+r-dx
                   if vx >= 0 and vy >= 0 and vx < thresh.shape[1] and vy < thresh.shape[0] and thresh[vy, vx] > 0:
                      f = True
                      #cv2.circle(peaks, (x+r2-dx,y+r2-dy), 1, (i+1), -1)
                      peaks[vy, vx] = (i+1)
                      break
               if f: break
           if not f:
              # Ignore the stone
              print('Cannot find peak for stone ({},{},{})'.format(x,y,r))

    if f_debug:
       #m = np.array(peaks*10000).astype(np.uint8)
       m = np.zeros((thresh.shape[0],thresh.shape[1],3), dtype = np.uint8)
       for i in range(3): m[:,:,i] = thresh
       for y in range(peaks.shape[0]):
           for x in range(peaks.shape[1]):
               if peaks[y,x] > 0:
                  for i in range(3):
                      for j in range(3):
                          m[y+i-1,x+j-1] = (0,0,255)
       cv2.imshow('Peaks', m)

##    # Do distance transform
##    dist = cv2.distanceTransform(thresh, cv2.DIST_L2, 3)
##    cv2.normalize(dist, dist, 0, 1.0, cv2.NORM_MINMAX)
##    if f_debug: cv2.imshow('Distance', dist)
##
##    # Threshold to normalize DT to 1
##    _, dist = cv2.threshold(dist, 0.4, 1.0, cv2.THRESH_BINARY)
##
##    # Find total markers
##    dist_8u = peaks.astype('uint8')
##    contours, _ = cv2.findContours(dist_8u, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
##
##    # Create the marker image for the watershed algorithm
##    markers = np.zeros(thresh.shape, dtype=np.int32)
##
##    # Draw the foreground markers
##    for i in range(len(contours)):
##        cv2.drawContours(markers, contours, i, (i+1), -1)
##
##    # Draw the background marker
##    cv2.circle(markers, (5,5), 3, (255,255,255), -1)
##
##    if f_debug:
##       m = np.array(markers*10000).astype(np.uint8)
##       cv2.imshow('Markers', m)
##
##    # Apply watershed
##    img3 = np.empty((gray.shape[0], gray.shape[1], 3), dtype=np.uint8)
##    img3[:,:,0] = gray
##    img3[:,:,1] = gray
##    img3[:,:,2] = gray
##    cv2.watershed(img3, markers)

    # Apply watershed
    markers = peaks.astype(np.int32)
    img3 = np.empty((gray.shape[0], gray.shape[1], 3), dtype=np.uint8)
    for i in range(3): img3[:,:,i] = thresh
    cv2.watershed(img3, markers)

    if f_debug:
       mark = markers.astype('uint8')
       #mark = cv2.bitwise_not(mark)
       cv2.imshow('Markers_v2', mark)
       m = img3.copy()
       m[markers == -1] = [0,0,255]
       cv2.imshow('Borders', m)

    # Collect results
    dst = np.zeros(gray.shape, dtype=np.uint8)
    rt = []
    for c in np.unique(markers):
        if c <= 0: continue
        mask = np.zeros(markers.shape, dtype=np.uint8)
        mask[markers == c] = 255
        cnts, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cm = max(cnts, key=cv2.contourArea)
        ((x, y), r) = cv2.minEnclosingCircle(cm)
        if f_debug: print("x = {}, y = {}, r = {}".format(x,y,r))

        if r <= 20.0:
           rt.append ([int(x), int(y), int(r)])
           cv2.circle(dst, (int(x), int(y)), int(r), (255,255,255), -1)

    # Filter out outlied R's
##    if len(rt) > 0:
##        rlist = [f[2] for f in rt]
##        mean_r = sum(rlist) / float(len(rlist))
##        rt2 = []
##        for r in rt:
##            if r[2] >= mean_r-3 and r[2] <= mean_r+3:
##                rt2.append(r)
##                cv2.circle(dst, (r[0],r[1]), r[2], (255,255,255), -1)
##
##        rt = rt2

    dst = cv2.bitwise_not(dst)
    if f_debug: cv2.imshow('Result', dst)

    return np.array(rt), dst
