import numpy as np
import cv2
import sys

left = 108
right = 530
right2 = 546
centor = (left + right)/2

top = 139
bottom = 259

base1 = 177
base2 = 201
base3 = 225

base_diff = 88
top2 = top + base_diff
bottom2 = bottom + base_diff
base2_1 = base1 + base_diff
base2_2 = base2 + base_diff
base2_3 = base3 + base_diff

img = cv2.imread("key1.png")
img2 = cv2.imread("key2.png")
width = img.shape[0]
height = img.shape[1]
cv2.line(img,(left,0),(left,height),(255,255,255),1)
cv2.line(img,(right,0),(right,height),(255,255,255),1)
cv2.line(img,(right2,0),(right2,height),(255,255,255),1)
cv2.line(img,(centor,0),(centor,height),(255,255,255),1)
cv2.line(img,(0,top),(width*2,top),(255,255,255),1)
cv2.line(img,(0,bottom),(width*2,bottom),(255,255,255),1)
cv2.line(img,(0,base1),(width*2,base1),(255,255,255),1)
cv2.line(img,(0,base2),(width*2,base2),(255,255,255),1)
cv2.line(img,(0,base3),(width*2,base3),(255,255,255),1)

cv2.imshow("img", img)

cv2.line(img2,(0,top2),(width*2,top2),(255,255,255),1)
cv2.line(img2,(0,bottom2),(width*2,bottom2),(255,255,255),1)
cv2.line(img2,(0,base2_1),(width*2,base2_1),(255,255,255),1)
cv2.line(img2,(0,base2_2),(width*2,base2_2),(255,255,255),1)
cv2.line(img2,(0,base2_3),(width*2,base2_3),(255,255,255),1)
cv2.imshow("img2", img2)
cv2.waitKey(0)

cv2.destroyAllWindows()
