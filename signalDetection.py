# -*- coding: utf-8 -*-
"""
Created on Thu May 24 15:33:54 2018

@author: huchenyang
"""
#import RPi.GPIO as GPIO
#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(37,GPIO.OUT)

import serial  
import time
import numpy as np
import cv2
import os
import functionSig
import datetime

bDebug = True
#os.system('raspistill -ex off')
# 打开串口  
#ser = serial.Serial("/dev/ttyUSB0", 9600)

# =============================================================================
# Hu = np.array([[ 2.67140331e+00],
#        [ 2.49887801e-01],
#        [ 4.93871703e-04],
#        [ 1.24715898e-01],
#        [ 5.45935520e-04],
#        [-5.20105578e-02],
#        [ 8.12394914e-04]])
# =============================================================================

cap=functionSig.set_cam_info2()
while True:
    ret,img = cap.read()
    leftTemp = cv2.imread("leftTemp.jpg")
    rightTemp = cv2.imread("Temp.jpg")
    redTemp = cv2.imread("red.jpg")
    leftTemp =cv2.resize(leftTemp,(30,30),fx=0,fy=0)
    rightTemp =cv2.resize(rightTemp,(30,30),fx=0,fy=0)
    redTemp =cv2.resize(redTemp,(30,30),fx=0,fy=0)
    start = datetime.datetime.now()
    #srcImage = cv2.imread("src\image56.jpg")
    signalResult = functionSig.signalDetect(img,leftTemp,rightTemp,redTemp)
    for i in range(len(signalResult)):
        cv2.circle(img,(signalResult[i][2],signalResult[i][3]),3,(255,0,0),-1)
    print(signalResult)
    end = datetime.datetime.now()
    print (end-start)
    cv2.imshow("src",img)
    #cap.release()
    if cv2.waitKey() & 0xff == ord("q"):
        break
# =============================================================================
# for i in range (1,72):
#     print("now processing : img%d"%i)
#     imageName = "image" + str(i)
#     srcImage = cv2.imread("src\%s.jpg"%imageName)
#     if (type(srcImage) is np.ndarray):
#     # =============================================================================
#     # ret,whiteCircle = cv2.threshold(whiteCircle,50,255,cv2.THRESH_BINARY)
#     # =============================================================================
#         resizedImage =cv2.resize(srcImage,(640,360),fx=0,fy=0)
#         drawing = resizedImage.copy()
#         start = datetime.datetime.now()
#         hsv_image = cv2.cvtColor(resizedImage, cv2.COLOR_BGR2HSV)
#         #b, g, r = cv2.split(resizedImage)
#         resultB = function.findBlue(hsv_image)
#         resultR = function.findRed(hsv_image)q
#         
#         kernelDila = np.ones((5,5),np.uint8)
#         dilation = cv2.dilate(resultR,kernelDila,iterations = 1)  
#         # =============================================================================
#         # ret,bThresh = cv2.threshold(b,130,255,cv2.THRESH_BINARY)
#         # ret,rThresh = cv2.threshold(r,50,255,cv2.THRESH_BINARY_INV)
#         # 
#         # targetImage = np.zeros((rThresh.shape[0],rThresh.shape[1]),dtype=np.uint8)
#         # 
#         # for i in range(0,rThresh.shape[0]):
#         #     for j in range(0,rThresh.shape[1]):
#         #         if ((rThresh[i][j] == 255) and (bThresh[i][j] == 255)):
#         #             targetImage[i,j]=255
#         # =============================================================================
#         # =============================================================================
#         # result = targetImage
#         # result = result.astype(np.uint8)
#         # =============================================================================
#         
#         contoursB = function.coutoursAndverify(resultB)
#         contoursR = function.coutoursAndverify(dilation)
#         
#         # =============================================================================
#         # img,contours, hierarchy = cv2.findContours(result,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)  
#         # cv2.drawContours(srcImage,contours,-1,(0,255,0),3)
#         # for i in range(0,len(contours)):
#         #     area = cv2.contourArea(contours[i])
#         #     if area<=2000:
#         #         del(contours[i])
#         # =============================================================================
#         blueRoi=[]
#         blueInfo = []
#         
#          
#         font=cv2.FONT_HERSHEY_SIMPLEX 
#         for i in range(len(contoursB)):
#             #x,y,w,h = cv2.boundingRect(contoursB[i])
#             x,y,w,h = cv2.boundingRect(contoursB[i])
#             if function.verifyBox(w,h):
#                 blueRoi.append(drawing[y:y+h,x:x+w])
#                
#                 resizeTemp = cv2.resize(blueRoi[-1],(80,80),fx=0,fy=0)
#                 resultRight = cv2.matchTemplate(resizeTemp,rightTemp,cv2.TM_SQDIFF)
#                 resultLeft = cv2.matchTemplate(resizeTemp,leftTemp,cv2.TM_SQDIFF)
#          
#         # =============================================================================
#         #     CannyImage = cv2.Canny(blueRoi[i],200,100)
#         #     resizeCanny = cv2.resize(CannyImage,(80,80),fx=0,fy=0)
#         #     targetCanny = cv2.bitwise_and(whiteCircle,resizeCanny)
#         #     ret,targetCanny = cv2.threshold(targetCanny,25,255,cv2.THRESH_BINARY)
#         #     moments = cv2.moments(CannyImage,2)
#         #     huMoments = cv2.HuMoments(moments)  
#         # =============================================================================
#             #cv2.imwrite("src/Temp.jpg",resizeTemp)
#          
#         # =============================================================================
#         #     ret = function.leftOrRight(blueRoi[i])
#         # =============================================================================
#                 if resultRight <= 7e+07 or resultLeft <= 7e+07:
#                     cv2.rectangle(drawing,(x-10,y-10),(x+w+10,y+h+10),(255,0,0),2)
#                     cv2.circle(drawing,(int(x+w/2),int(y+h/2)),3,(255,0,0),-1)
#                     #blueInfo.append(int(x+w/2),int(y+h/2))
#                     if resultLeft < resultRight:
#                         cv2.putText(drawing, "left", (x-10,y-15), font, 1, (255,0,0),2, 8, 0)
#                     else:
#                         cv2.putText(drawing, "right", (x-10,y-15), font, 1, (255,0,0),2, 8, 0)
#         # =============================================================================
#         #     if ret:
#         #         cv2.putText(drawing, "left", (x-10,y-15), font, 1, (255,0,0),2, 8, 0)
#         #     else:
#         #         cv2.putText(drawing, "right", (x-10,y-15), font, 1, (255,0,0),2, 8, 0)
#         # =============================================================================
#         # =============================================================================
#         #     gray = cv2.cvtColor(blueRoi[i], cv2.COLOR_BGR2GRAY)
#         #     blur = cv2.GaussianBlur(gray,(5,5),0)
#         #     ret,blueRoiThresh = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
#         #     height, width = blueRoiThresh.shape
#         #     areaLeft = 0
#         #     areaRight = 0
#         #     
#         #     for i in range(height):
#         #         for j in range(int(width/2)):
#         #             if blueRoiThresh[i, j] == 255:
#         #                 areaLeft += 1
#         #     
#         #     for i in range(height):
#         #         for j in range(int(width/2),int(width)):
#         #             if blueRoiThresh[i, j] == 255:
#         #                 areaRight += 1
#         #             
#         #     if areaLeft > areaRight:
#         #         cv2.putText(drawing, "left", (x-10,y-15), font, 1, (255,0,0),2, 8, 0)
#         #     else:
#         #         cv2.putText(drawing, "right", (x-10,y-15), font, 1, (255,0,0),2, 8, 0)
#         # =============================================================================
#                 
#         redRoi = []
#         for i in range(len(contoursR)):
#             x,y,w,h = cv2.boundingRect(contoursR[i])
#             if function.verifyBox(w,h):
#                 redRoi.append(drawing[y:y+h,x:x+w])
#                 resizeTemp = cv2.resize(redRoi[-1],(80,80),fx=0,fy=0)
#                # cv2.imwrite("redTemp.jpg",resizeTemp)
#                 resultTemp = cv2.matchTemplate(resizeTemp,redTemp,cv2.TM_SQDIFF)
#                 #resultLeft = cv2.matchTemplate(resizeTemp,leftTemp,cv2.TM_SQDIFF)
#                 if resultTemp<= 5.7e+07:
#                     cv2.rectangle(drawing,(x-10,y-10),(x+w+10,y+h+10),(0,0,255),2)
#                     cv2.putText(drawing, "stop", (x-10,y-15), font, 1, (0,0,255),2, 8, 0)
#             
#         end = datetime.datetime.now()
#         print (end-start)
#         
#         # =============================================================================
#         # start = datetime.datetime.now()
#         # for i in range(0,10):
#         #     b, g, r = cv2.split(srcImage) 
#         #     result = function.findBlue(b,r,130,50)
#         #     contours = function.coutoursAndverify(result)
#         # end = datetime.datetime.now()
#         # print (end-start)
#         # =============================================================================
#         
#         if(bDebug):
#             cv2.imshow("resizedImage",resizedImage) 
#             cv2.imshow("resultR",resultR)
#             cv2.imshow("resultB",resultB)
#             #cv2.imshow("dilationR",dilation)
#             cv2.imshow("drawing",drawing)
#             #cv2.imshow("blue",blueRoi[0])
#             #cv2.imshow("th3",th3)
#          
#         cv2.waitKey()
#         
# =============================================================================
cv2.destroyAllWindows()

# =============================================================================
# def findBlue(imageB,imageR,bThresh,rThresh):
#     
#     ret,bThresh = cv2.threshold(imageB,bThresh,255,cv2.THRESH_BINARY)
#     ret,rThresh = cv2.threshold(imageR,rThresh,255,cv2.THRESH_BINARY_INV)
#     targetImage = np.zeros((imageB.shape[0],imageB.shape[1]))
#     
#     for i in range(0,imageB.shape[0]):
#         for j in range(0,imageB.shape[1]):
#             if ((imageB[i][j] == 255) and (imageB[i][j] == 255)):
#                 targetImage[i,j]=255
#     return targetImage
# =============================================================================
