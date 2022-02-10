import serial
import time
import statistics

import cv2
import numpy as np

from sklearn.metrics import pairwise

time.sleep(2)
#######################
Arduino_serial=serial.Serial('COM5',9600)

commands=[]
background=None

accumulated_weight=0.5

roi_top=20
roi_bottom=200
roi_right=300
roi_left=500
######################
def led_control(fingers):
    global commands
    user_input=str(fingers)
    commands.append(int(user_input))
    #based in detection the data is sent to indication circuit
    if user_input=='1':
        time.sleep(0.2)
        Arduino_serial.write(b'1')
    elif user_input=='2':
        time.sleep(0.2)
        Arduino_serial.write(b'2')
    elif user_input=='3':
        time.sleep(0.2)
        Arduino_serial.write(b'3')
    elif user_input=='4':
        time.sleep(0.2)
        Arduino_serial.write(b'4')
    elif user_input=='0':
        time.sleep(0.2)
        Arduino_serial.write(b'0')
    elif user_input>='5':
        print('Invalid command!!')
        #if the command is for long time then send data to on/off the device
    if len(commands)>19:
        csum=sum(commands)
        print(csum)
        if csum==20 or statistics.mode(commands)==1:
            Arduino_serial.write(b'a')
            time.sleep(2)
            commands=[]
        elif csum==40 or statistics.mode(commands)==2:
            Arduino_serial.write(b'b')
            time.sleep(2)
            commands=[]
        elif csum==60 or statistics.mode(commands)==3:
            Arduino_serial.write(b'c')
            time.sleep(2)
            commands=[]
        elif (csum in range(70,90)) and statistics.mode(commands)==4: #as detecting 4 is more error prone
            Arduino_serial.write(b'd')
            time.sleep(2)
            commands=[]
        elif csum<15 and statistics.mode(commands)==0:
            Arduino_serial.write(b's')
            time.sleep(2)
            commands=[]
        else:
            commands=[]
######################
def calc_accum_avg(frame,accumulate_weight):
    global background

    if background is None:
        background=frame.copy().astype('float')
        return None

    cv2.accumulateWeighted(frame,background,accumulate_weight)
#####################

def segment(frame,threshold_min=25):#variable to be callibrated

    diff=cv2.absdiff(background.astype('uint8'),frame)

    ret,thresholded=cv2.threshold(diff,threshold_min,255,cv2.THRESH_BINARY)
    #thresholded=cv2.adaptiveThreshold(diff,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,8)

    contours,hierarchy = cv2.findContours(thresholded.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    if len(contours)==0:
        return None

    else:
        #assuming the largest external contour in roi, is the hand
        hand_segment=max(contours,key=cv2.contourArea)

        return(thresholded,hand_segment)
#####################

def count_fingers(thresholded,hand_segment):

    conv_hull=cv2.convexHull(hand_segment)
    #format can be understood after seeing documentation

    #Top
    top=tuple(conv_hull[conv_hull[:,:,1].argmin()][0])#tuples of x,y cords
    bottom=tuple(conv_hull[conv_hull[:,:,1].argmax()][0])
    left=tuple(conv_hull[conv_hull[:,:,0].argmin()][0])
    right=tuple(conv_hull[conv_hull[:,:,0].argmax()][0])

    cX=(left[0]+right[0])//2
    cY=(top[1]+bottom[1])//2

    distance=pairwise.euclidean_distances([(cX,cY)],Y=[left,right,top,bottom])[0]

    max_distance=distance.max()

    radius=int(0.8*max_distance)#ratio to be callibrated but 0.8-0.9 generally
    circumference=(2*np.pi*radius)

    circular_roi=np.zeros(thresholded.shape[:2],dtype='uint8')

    cv2.circle(circular_roi,(cX,cY),radius,255,10)

    circular_roi=cv2.bitwise_and(thresholded,thresholded,mask=circular_roi)

    contours,hierarchy=cv2.findContours(circular_roi.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

    count=0

    for cnt in contours:

        (x,y,w,h)=cv2.boundingRect(cnt)

        out_of_wrist=(cY+(cY*0.25))>(y+h)

        limit_points=((circumference*0.25)>cnt.shape[0])

        if out_of_wrist and limit_points:
            count+=1

    return count
##############################

cam=cv2.VideoCapture(0)

num_frames=0

while True:

    ret,frame=cam.read()

    frame_copy=frame.copy()

    roi=frame[roi_top:roi_bottom,roi_right:roi_left]

    gray=cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY)

    gray=cv2.GaussianBlur(gray,(9,9),0)

    if num_frames<60:#first 60 frames to accumulate background
        calc_accum_avg(gray,accumulated_weight)

        if num_frames<=59:
            cv2.putText(frame_copy,'WAIT, LOADING',(200,300),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
            cv2.imshow('Finger count',frame_copy)
    else:
        hand=segment(gray)

        if hand is not None:
            thresholded,hand_segment=hand
            #Draws contours around real hand in live stream
            cv2.drawContours(frame_copy,[hand_segment+(roi_right,roi_top)],-1,(255,0,0),5)

            fingers=count_fingers(thresholded,hand_segment)

            cv2.putText(frame_copy,str(fingers),(70,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
            led_control(fingers)
            cv2.imshow('Thresholded',thresholded)

    cv2.rectangle(frame_copy,(roi_left,roi_top),(roi_right,roi_bottom),(0,0,255),5)

    num_frames+=1

    cv2.imshow('Finger count',frame_copy)

    k=cv2.waitKey(1)&0xFF

    if k==27:
        print('Shutting down')
        time.sleep(0.1)
        Arduino_serial.close()
        break

cam.release()
cv2.destroyAllWindows()
