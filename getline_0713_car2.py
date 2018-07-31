# -*- coding: utf-8 -*-
"""
Created on Mon Jul  2 09:36:19 2018

@author: lijiancong
"""
import numpy as np
import math
import cv2
import datetime
import time

#import matplotlib.pyplot as plt
from picamera.array import PiRGBArray
from picamera import PiCamera

def set_picamera():
    camera = PiCamera()
    camera.resolution = (640,360)
    camera.framerate = 30
    camera.brightness=60
    camera.shutter_speed = 10000
    camera.exposure_mode = 'night'
    camera.iso=800
    time.sleep(5)
    g = camera.awb_gains
    camera.awb_mode='off'
    camera.awb_gains = g
    #start = datetime.datetime.now()
    rawCapture = PiRGBArray(camera,size=(640,360))
    
    return camera,rawCapture

def set_cam_info():
    """set camera information"""
    cap = cv2.VideoCapture(0)
    cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH,640)
    cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT,480)
    #cap.set(cv2.cv.CV_CAP_PROP_EXPOSURE,0)
    cap.set(cv2.cv.CV_CAP_PROP_FPS,5)
    return cap

def grayscale(img):
    """Applies the Grayscale transform
    This will return an image with only one color channel
    but NOTE: to see the returned image as grayscale
    (assuming your grayscaled image is called 'gray')
    you should call plt.imshow(gray, cmap='gray')"""
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # Or use BGR2GRAY if you read an image with cv2.imread()
    # return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def canny(img, low_threshold, high_threshold):
    """Applies the Canny transform"""
    return cv2.Canny(img, low_threshold, high_threshold)

def region_of_interest(img, vertices):
    """
    Applies an image mask.
    
    Only keeps the region of the image defined by the polygon
    formed from `vertices`. The rest of the image is set to black.
    `vertices` should be a numpy array of integer points.
    """
    #defining a blank mask to start with
    mask = np.zeros_like(img)    
    #defining a 3 channel or 1 channel color to fill the mask with depending on the input image
    if len(img.shape) > 2:
        channel_count = img.shape[2]  # i.e. 3 or 4 depending on your image
        ignore_mask_color = (255,) * channel_count
    else:
        ignore_mask_color = 255
        
    #filling pixels inside the polygon defined by "vertices" with the fill color    
    cv2.fillPoly(mask, vertices, ignore_mask_color)
    
    #returning the image only where mask pixels are nonzero
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image

def perspect_change(img): 
    all_scale=0.25
    delta=64*all_scale
    
    scale_x=0.65
    scale_y=1.5
    x_offset=28
    y_offset=-41
          
    rectangle_in=np.array([
            [250*all_scale,300*all_scale],
            [370*all_scale,300*all_scale],
            [244*all_scale,400*all_scale],
            [375*all_scale,400*all_scale]], dtype = "float32")
    rectangle_out=np.array([
            [250*scale_x*all_scale+x_offset,300*scale_y*all_scale+y_offset],
            [370*scale_x*all_scale+x_offset,300*scale_y*all_scale+y_offset],
            [250*scale_x*all_scale+x_offset,300*scale_y*all_scale+delta+y_offset],
            [370*scale_x*all_scale+x_offset,300*scale_y*all_scale+delta+y_offset]], dtype = "float32")
    M = cv2.getPerspectiveTransform(rectangle_in, rectangle_out)
    warped = cv2.warpPerspective(img, M, (img.shape[1], 71))
    return warped

def get_line_features(edge):
    dmin=3
    dmax=4
    doff=2
    num_ped=0
    flag_ped=0
    features=np.zeros((15,3))
    for row in range(15):
        left_line=edge[row*5,0:80]
        left=np.where(left_line[::-1]==255)
        right=np.where(edge[row*5,80:]==255)
        if len(left[0])+len(right[0])<10:
            if len(left[0])>0 and 79-left[0][0]>dmax:
                if np.sum(left_line[79-left[0][0]-dmax:79-left[0][0]-(dmin-1)])>0 and (left_line[79-left[0][0]-doff])==0:
                    features[row][0]=1
                    features[row][1]=79-left[0][0]-doff 
            if len(right[0])>0:
                if np.sum(edge[row*5,right[0][0]+80+dmin:right[0][0]+80+(dmax+1)])>0 and edge[row*5,right[0][0]+80+doff]==0:
                    features[row][0]=features[row][0]+2
                    features[row][2]=right[0][0]+80+doff
        else:
            for i_left in range(len(left[0])):
                if len(left[0])>0 and 79-left[0][i_left]>dmax:
                    if np.sum(left_line[79-left[0][i_left]-dmax:79-left[0][i_left]-(dmin-1)])>0 and (left_line[79-left[0][i_left]-doff])==0:
                        features[row][0]=1
                        features[row][1]=79-left[0][i_left]-doff 
                        break
            for i_right in range(len(right[0])):
                if len(right[0])>0:
                    if np.sum(edge[row*5,right[0][i_right]+80+dmin:right[0][i_right]+80+(dmax+1)])>0 and edge[row*5,right[0][i_right]+80+doff]==0:
                        features[row][0]=features[row][0]+2
                        features[row][2]=right[0][i_right]+80+doff
                        break
            num_ped=num_ped+1
            if num_ped>7:
                flag_ped=1
                
    return features,flag_ped

def get_offset(features):
    offset=0
    height=70
    lane_width_half=55
    Left=np.zeros((2,15))
    Right=np.zeros((2,15))
    Num=np.zeros((2,1))
    Num=Num.astype('int16')
    for i in range(14,-1,-1):
        if features[i][0]==3:
            Left[0][Num[0][0]]=features[i][1]
            Left[1][Num[0][0]]=i*5
            Right[0][Num[1][0]]=features[i][2]
            Right[1][Num[1][0]]=i*5
            Num[0][0]=Num[0][0]+1
            Num[1][0]=Num[1][0]+1
        elif features[i][0]==1:
            Left[0][Num[0][0]]=features[i][1]
            Left[1][Num[0][0]]=i*5
            Num[0][0]=Num[0][0]+1
        elif features[i][0]==2:
            Right[0][Num[1][0]]=features[i][2]
            Right[1][Num[1][0]]=i*5
            Num[1][0]=Num[1][0]+1
    if Num[0][0]>1 and Num[1][0]>1:
        A_left=np.polyfit(Left[1,:Num[0][0]],Left[0,:Num[0][0]] , 1)
        A_right=np.polyfit(Right[1,:Num[1][0]],Right[0,:Num[1][0]] , 1)
        if A_left[0]*height+A_left[1]>90:
            A=[A_right[0],A_right[1]-lane_width_half]
        elif A_right[0]*height+A_right[1]<70:
            A=[A_left[0],A_left[1]+lane_width_half]
        else:
            A=(A_left+A_right)/2
    elif Num[0][0]>1:
        A_left=np.polyfit(Left[1,:Num[0][0]],Left[0,:Num[0][0]] , 1)
        A=[A_left[0],A_left[1]+lane_width_half]
    elif Num[1][0]>1:
        A_right=np.polyfit(Right[1,:Num[1][0]],Right[0,:Num[1][0]] , 1)
        A=[A_right[0],A_right[1]-lane_width_half]
    else:
        A=[0.0, 75.0]
    XX=A[0]*height+A[1]
    offset=XX-75
    return offset

def img_process(img):
    low_threshold=50
    high_threshold=100
    imshape_x=160
    imshape_y=71
    img_cut=img[180:480,:]
    img_gray_small=cv2.resize(img_cut,(160,75))
    img_per=perspect_change(img_gray_small)
    img_canny=canny(img_per, low_threshold, high_threshold)
    vertices = np.array([[(int(0.063*imshape_x),0),(int(0.183*imshape_x), imshape_y), (int(0.824*imshape_x), imshape_y),(int(0.943*imshape_x), 0)]], dtype=np.int32)
    masked_edges=region_of_interest(img_canny, vertices)
    #plt.figure()
    #plt.imshow(masked_edges,cmap='gray')
    [features,flag_pedes]=get_line_features(masked_edges)
    offset=get_offset(features)
    #cv2.line(img_per, (int(offset)+80, 71), ((int(offset)+80, 67)), [255,0,0], 2)
    return offset,img_per,flag_pedes
    
def get_angle(offset):
    k_left=0.60
    k_right=0.45
    rate=3
    if offset<0:
        angle=max(90+k_left*rate*offset,30)
    else:
        angle=min(90+k_right*rate*offset,135)
    return angle

'''
if __name__ == '__main__':
    # initialization
    #cap=set_cam_info()
    count=0
    # processing

    start=datetime.datetime.now()
    while True:
        # read image
        img = cv2.imread("image_car2/lm34.jpg")
        img_gray=grayscale(img)
        [offset,img_out]=img_process(img_gray)
        
        #ret,img = cap.read()
        count=count+1
        if count>1:
            end=datetime.datetime.now()
            cv2.imshow('fig',img_out)
            #plt.figure()
            #plt.imshow(img_out,cmap='gray')
            print (end-start)
            print ("time:"+str(count))
            break
        waitkey(1)
        '''
            
