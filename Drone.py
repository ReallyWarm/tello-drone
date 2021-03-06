from djitellopy import tello
import cv2
import numpy as np
from time import sleep

me = tello.Tello()
me.connect(False)
print(me.get_battery())

me.takeoff()

def empty(a):
    pass

cv2.namedWindow("HSV")
cv2.resizeWindow("HSV",640,240)
cv2.createTrackbar("HUE Min","HSV",0,179,empty)
cv2.createTrackbar("HUE Max","HSV",179,179,empty)
cv2.createTrackbar("SAT Min","HSV",0,255,empty)
cv2.createTrackbar("SAT Max","HSV",255,255,empty)
cv2.createTrackbar("VALUE Min","HSV",0,255,empty)
cv2.createTrackbar("VALUE Max","HSV",255,255,empty)




while True:
    me.send_rc_control(10, 0, 0, 100)
    sleep(20)
    me.send_rc_control(-10, 0, 0, -100)
    sleep(20)
    me.send_rc_control(0, 0, 0, 0)

    img = me.get_frame_read().frame
    img = cv2.resize(img, (640, 240))
    imgHsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    h_min = cv2.getTrackbarPos("HUE Min", "HSV")
    h_max = cv2.getTrackbarPos("HUE Max", "HSV")
    s_min = cv2.getTrackbarPos("SAT Min", "HSV")
    s_max = cv2.getTrackbarPos("SAT Max", "HSV")
    v_min = cv2.getTrackbarPos("VALUE Min", "HSV")
    v_max = cv2.getTrackbarPos("VALUE Max", "HSV")
    # print(h_min)

    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    mask = cv2.inRange(imgHsv, lower, upper)
    result = cv2.bitwise_and(img, img, mask=mask)

    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    hStack = np.hstack([img, mask, result])

    # cv2.imshow('Original', img)
    # cv2.imshow('HSV Color Space', imgHsv)
    # cv2.imshow('Mask',mask)
    # cv2.imshow('Result', result)
    cv2.imshow('Horizontal Stacking', hStack)
    if cv2.waitKey(1) & 0xff == ord('z'):
        break

img.release()
cv2.destroyAllWindows()
me.send_rc_control(10,0,0,100)
sleep(40)
me.send_rc_control(-10,0,0,-100)
sleep(40)
me.send_rc_control(0,0,0,0)
me.land()