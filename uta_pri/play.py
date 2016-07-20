import numpy as np
import cv2
import cv

#cap = cv2.VideoCapture('/Users/hiranosa/Downloads/mp4_h264_aac.mp4')
cap = cv2.VideoCapture('/Users/hiranosa/Downloads/test-music.mp4')
#cap = cv2.VideoCapture('/Users/hiranosa/Downloads/test-taiko.mp4')

while(cap.isOpened()):
    ret, frame = cap.read()
    ## Canny
    #canny = cv2.Canny( frame, 100, 200 )
    #cv2.imshow( "canny", canny );

    ## Lines
    draw = frame.copy()
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray,50,150,apertureSize = 3)
    lines = cv2.HoughLinesP(edges,1,np.pi/180,100,minLineLength=100,maxLineGap=10)
    for line in lines:
        x1,y1,x2,y2 = line[0]
        cv2.line(draw,(x1,y1),(x2,y2),(0,255,0),2)
    
    cv2.imshow('HoughLinesP',draw)

    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
