import cv2 as cv
import numpy as np
import serial  as pys
from cv2 import aruco


clicked_points =  []
def eventclick(event,x,y,flag,params):
    global clicked_points
    if event == cv.EVENT_LBUTTONDOWN:
        clicked_points.append((x,y))
        print(x,' ',y)
        cv.imshow('video',frame)

def getangledegrees(p1,p2,p3) :
    fixline = np.array([p2[0]-p1[0],p2[1]-p1[1]])
    clickline = np.array([p3[0]-p1[0],p3[1]-p1[1]])
    dotproduct = np.dot(fixline,clickline)
    mag_line = np.linalg.norm(fixline) * np.linalg.norm(clickline)
    value_cosine = dotproduct / mag_line
    angle_radians = np.arccos(value_cosine)
    angle_degrees = np.degrees(angle_radians)
    if angle_degrees ==0 :
        angle_degrees=0
    return angle_degrees

def getdistance(p1,p2):
    distance_to_travel = np.linalg.norm(p1-p2)
    return distance_to_travel

cv.namedWindow('video')

aruco_marker = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
aruco_parameters = aruco.DetectorParameters_create()
cap =  cv.VideoCapture(0)

screen_width  = 1366
screen_height = 768
cap.set(cv.CAP_PROP_FRAME_WIDTH, screen_width)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, screen_height)


while True :
    isTrue , frame= cap.read()
    marker_corners, marker_ID, realtimedetect = aruco.detectMarkers(frame, aruco_marker, parameters=aruco_parameters)
    if marker_corners:
        for ids,corners in zip(marker_ID,marker_corners):
            corners= corners.reshape(4,2)
            corners = corners.astype(int)
            centerx = int((corners[0][0] + corners[2][0]) / 2)
            centery = int((corners[0][1] + corners[2][1]) / 2)
            global center
            center = (centerx,centery)
            toplinex = int((corners[0][0] + corners[1][0]) / 2)
            topliney = int((corners[0][1] + corners[1][1]) / 2)
            global topline
            topline = (toplinex,topliney)
            cv.line(frame, (center[0], center[1]), (topline[0], topline[1]), (0, 255, 0), 2)
            cv.circle(frame, (centerx, centery), 1, (0, 255, 0), 1)
            cv.setMouseCallback('video',eventclick)
            if len(clicked_points) > 0 :
                latest_point = clicked_points[-1]
                cv.line(frame,(latest_point[0],latest_point[1]),(center[0],center[1]),(0,255,0),2)
                point1 = np.array([centerx,centery])
                point2 = np.array([latest_point[0],latest_point[1]])
                angle = getangledegrees(center,topline,latest_point)
                distance = getdistance(point1,point2)
                cv.putText(frame,f"angle:{angle:.2f} degrees  line length:{distance:.2f}",(0,200),cv.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)

    cv.imshow("video",frame)
    if cv.waitKey(1) & 0xFF==ord('d'):
        break
cap.release()
cv.destroyAllWindows()