import cv2 as cv
import numpy as np
from cv2 import aruco

aruco_marker = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
aruco_parameters = aruco.DetectorParameters_create()
cap =  cv.VideoCapture(0)
while True :
    isTrue , frame= cap.read()
    marker_corners , marker_ID,realtimedetect = aruco.detectMarkers(frame,aruco_marker,parameters = aruco_parameters)
    if marker_corners:
        for ids,corners in zip(marker_ID,marker_corners):
            cv.polylines(frame,[corners.astype(np.int32)],True,(0,255,255),4,cv.LINE_AA)
            corners= corners.reshape(4,2)
            corners = corners.astype(int)
            cv.putText(frame, f"id ={ids[0]}", (frame.shape[0 // 2], frame.shape[1] // 2), cv.FONT_HERSHEY_TRIPLEX,1,
                       (0, 0, 0),2,cv.LINE_AA)
            print(marker_ID," ",marker_corners)
    cv.imshow("video", frame)
    if cv.waitKey(1) & 0xFF==ord('d'):
        break
cap.release()
cv.destroyAllWindows()


