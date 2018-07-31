# -*- coding: utf-8 -*-
"""
Created on Thu Jun 28 10:28:44 2018

@author: menglin
"""
#import matplotlib.pyplot as plt # plt 用于显示图片
#import matplotlib.image as mpimg # mpimg 用于读取图片
import numpy as np
import cv2
#from getline_draw import*


#%%
def LongLine(edges):
    count_pixels_threshold=75
    row_min=25
    row_max=31
    col_min=50
    col_max=100
    LongLine_Flag=0
    count0=0
    count255=0
    for i in range(row_min,row_max) :
        for j in range(col_min,col_max):
            if edges[i,j]==0:
                count0=count0+1
            else :
                count255=count255+1
    if count255>=count_pixels_threshold:
        LongLine_Flag=1
    #print('edgepixels'+str(count255))
    return LongLine_Flag
    
#%%
def TurnJudgement(gray):
    count_pixels=25
    Turn_Flag=0
    count_left=0
    count_right=0
    row_min=30
    row_max=75
    col_min=50
    col_max=100
    gray=cv2.resize(gray,(160,90))
    edges = cv2.Canny(gray, 50, 150)
    LongLine_Flag=LongLine(edges)
    #print(LongLine_Flag)
    if LongLine_Flag==1:
        for i in range(row_min,row_max) :
            for j in range(2,col_min):
                if edges[i,j]==255:
                    count_left= count_left+1
            for k in range(col_max,158):
                if edges[i,k]==255:
                    count_right=count_right+1
        if count_right-count_left>count_pixels:
            Turn_Flag=1 ## left turn
        elif count_left-count_right>count_pixels:
            Turn_Flag=2 ## right turn
    #print('Right:' +str(count_right))
    #print('Left:'+str(count_left))
    return Turn_Flag,LongLine_Flag
#%%
#flag=TurnJudgement(gray_copy)
#print(flag)
