# -*- coding: utf-8 -*-
import numpy as np
import cv
import cv2
import sys

# 譜面左端
left = 108
# 譜面右端
right = 530
# 譜面の画面の右端
right2 = 546
# 譜面真ん中(4小節目)
centor = (left + right)/2
# 1小節分の大きさ
measure = (right - left)/8

# 1番目の譜面取得タイミング(4〜8小節目ノートを拾うタイミング)
# 譜面トップ
top = 139
# 譜面ボトム
bottom = 259

# 3線の1番目
base1 = 177
# 3線の2番目
base2 = 201
# 3線の3番目
base3 = 225

# 1番目の譜面取得タイミング(4〜8小節目ノートを拾うタイミング)
# y軸の差分
base_diff = 88
top2 = top + base_diff
bottom2 = bottom + base_diff
base2_1 = base1 + base_diff
base2_2 = base2 + base_diff
base2_3 = base3 + base_diff

bases = [[base1, base2, base3],[base2_1,base2_2,base2_3]]

# 判定マージン
mergine = 2
# 時間マージン
time_mergine = 200

cap = cv2.VideoCapture(sys.argv[1])
x_template = cv2.imread("x_template.png")
x_template = cv2.cvtColor(x_template,cv2.COLOR_BGR2GRAY)
template_width = x_template.shape[0]
template_height = x_template.shape[1]

prev_time = 0
while(cap.isOpened()):
    ret, frame = cap.read()
    ## Canny
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    canny = cv2.Canny( gray, 50, 100 )
    cv2.imshow( "canny", canny )
    draw = frame.copy()

    ## labeling too slow, and can't detect
    #dst = frame.copy()
    #binary = cv2.threshold(canny, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    #n, label = cv2.connectedComponents(binary)
    #rgbs = np.random.randint(0,255,(n+1,3))
    #for y in xrange(0, binary.shape[0]):
    #    for x in xrange(0, binary.shape[1]):
    #        if label[y, x] > 0:
    #            dst[y, x] = rgbs[label[y, x]]
    #        else:
    #            dst[y, x] = [0, 0, 0]
    #cv2.imshow("label", dst)


    ## Lines fast and detect. but multiple detect....
    #lines = cv2.HoughLinesP(canny,1,np.pi/90,300,minLineLength=50,maxLineGap=20)
    #for line in lines:
    #    x1,y1,x2,y2 = line[0]
    #    cv2.line(draw,(x1,y1),(x2,y2),(0,255,0),2)

    ## lines fast and detect. good.
    lines = cv2.HoughLines(canny,1,np.pi/10,200)
    count = [0,0]
    for line in lines:
        for rho,theta in line:
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a*rho
            y0 = b*rho
            x1 = int(x0 + 1000*(-b))
            y1 = int(y0 + 1000*(a))
            x2 = int(x0 - 1000*(-b))
            y2 = int(y0 - 1000*(a))
            cv2.line(draw,(x1,y1),(x2,y2),(0,0,255),2)
            index = 0
            for base3 in bases:
                for base in base3:
                    if abs(y1 - base) < mergine:
                        count[index] = count[index] + 1
                index = index + 1
    time = cap.get(cv2.cv.CV_CAP_PROP_POS_MSEC)
    if (time - prev_time) > time_mergine:
        if count[0] >= 3:
            print "fire1!! %d" % (time)
            cut = canny[top:bottom, centor-measure:right2]
            cv2.imshow("fire1!!", cut)
            prev_time = time
        if count[1] >= 3:
            time = cap.get(cv2.cv.CV_CAP_PROP_POS_MSEC)
            print "fire2!! %d" % (time)
            cut = canny[top2:bottom2, left:centor]
            cv2.imshow("fire2!!", cut)
            prev_time = time
    
    ## circles detect multi... bad.
    #circles = cv2.HoughCircles(canny,cv2.HOUGH_GRADIENT,1,10, param1=20,param2=20,minRadius=10,maxRadius=20)
    #circles = np.uint16(np.around(circles))
    #if circles is not None:
    #    for (x, y, r) in circles[0]:
    #        cv2.circle(draw, (x, y), r, (0, 0, 255), -1)

    cv2.imshow('HoughLinesP',draw)

    ## template match slow!!! and detect low
    ## button detect testing..
    #matches = cv2.matchTemplate(canny, x_template, cv2.TM_CCOEFF_NORMED);
    #threshold = 0.5
    #for y in xrange(matches.shape[0]):
    #    for x in xrange(matches.shape[1]):
    #        if matches[y][x] > threshold:
    #            cv2.rectangle(draw, (x, y),
    #                          (x + template_width, y + template_height),
    #                          (255, 0, 0), 3)

    #cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        for line in lines:
            for rho,theta in line:
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a*rho
                y0 = b*rho
                x1 = int(x0 + 1000*(-b))
                y1 = int(y0 + 1000*(a))
                x2 = int(x0 - 1000*(-b))
                y2 = int(y0 - 1000*(a))
                cv2.line(draw,(x1,y1),(x2,y2),(0,0,255),2)
        cv2.imwrite("capture.png", draw);
        break

cap.release()
cv2.destroyAllWindows()
