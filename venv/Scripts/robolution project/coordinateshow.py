import cv2 as cv
import numpy as np

def eventclick(event,x,y,flag,params):

    if event == cv.EVENT_LBUTTONDOWN:
        x= x- xcenter
        y= ycenter -y
        print(x,' ',y)
        cv.imshow('video',flipper)

if __name__== "__main__":

    capture = cv.VideoCapture(0)
    while True:
        isTrue,frame=capture.read()
        flipper = cv.flip(frame,1)
        xcenter= flipper.shape[1]//2
        ycenter=flipper.shape[0]//2
        cv.circle(flipper, (xcenter,ycenter),1, (255, 0, 0), -1)
        cv.imshow('video',flipper)
        cv.setMouseCallback('video',eventclick)

        if cv.waitKey(1) & 0xFF ==ord('d'):
            break

cv.destroyAllWindows()
