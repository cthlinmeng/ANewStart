# -*- coding: utf-8 -*  
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(32, GPIO.IN)                          # right US Echo
GPIO.setup(36, GPIO.OUT)                         # right US Trig
GPIO.setup(15, GPIO.IN)                          # front US Echo
GPIO.setup(38, GPIO.OUT)                         # front US Trig
GPIO.setup(37, GPIO.OUT,initial = GPIO.HIGH)     # red1
GPIO.setup(35, GPIO.OUT,initial = GPIO.HIGH)     # red2
GPIO.setup(33, GPIO.OUT,initial = GPIO.LOW)      # yellow_right
GPIO.setup(31, GPIO.OUT,initial = GPIO.LOW)      # yellow_left
GPIO.setup(11, GPIO.OUT,initial = GPIO.HIGH)     # Beep
import serial  
import time
import math
import cv2
import datetime
#import functionSigNight as functionSig
import functionSig
#from getline_draw import*
#from getline_fitone import*
from getline_0713_car2 import*
from straight_canny_resize_LM0703 import *
#from picamera.array import PiRGBArray
#from picamera import PiCamera

# 打开串口  
ser = serial.Serial("/dev/ttyUSB0", 9600)
#GPIO.output(37,GPIO.LOW)
#GPIO.output(37,GPIO.HIGH)
#str1 = "1,20,70"
#n = ser.write(str1)
#time.sleep(0.3)
#str1 = "1,20,110"
#print str1
#n = ser.write(str1)
#time.sleep(0.1)
global brake_index
global speedStr
global speedFlag
global Turn_index
global flag_ped_count
global signal_turn_index
signal_turn_index=0
Turn_index=0
speedFlag=1
speedStr='15'
brake_index=0
p_flag1 = 0
p_flag2 = 0
p_flag3 = 0
p_count = 0
flag_ped_count=0

def turn_right_led(flash_period,turn_time):
    flash_num = (turn_time*10) // (flash_period*10)
    left_time = (turn_time*10) % (flash_period*10)/10
    for i in range(int(flash_num)):
        if ( i % 2 == 0):
            GPIO.output(33,GPIO.HIGH)
            time.sleep(flash_period)
        else:
            GPIO.output(33,GPIO.LOW)
            time.sleep(flash_period)
    if (int(flash_num) % 2 == 0):
        GPIO.output(33,GPIO.LOW)
        time.sleep(left_time)
    else:
        GPIO.output(33,GPIO.HIGH)
        time.sleep(left_time)
        GPIO.output(33,GPIO.LOW)

def turn_left_led(flash_period,turn_time):
    flash_num = (turn_time*10) // (flash_period*10)
    left_time = (turn_time*10) % (flash_period*10)/10
    for i in range(int(flash_num)):
        if ( i % 2 == 0):
            GPIO.output(31,GPIO.HIGH)
            time.sleep(flash_period)
        else:
            GPIO.output(31,GPIO.LOW)
            time.sleep(flash_period)
    if (int(flash_num) % 2 == 0):
        GPIO.output(31,GPIO.LOW)
        time.sleep(left_time)
    else:
        GPIO.output(31,GPIO.HIGH)
        time.sleep(left_time)
        GPIO.output(31,GPIO.LOW)

def stop_led(stop_time):
    GPIO.output(35,GPIO.HIGH)
    GPIO.output(37,GPIO.HIGH)
    time.sleep(stop_time)
    GPIO.output(35,GPIO.LOW)
    GPIO.output(37,GPIO.LOW)

def start_Beep():
    for i in range(0,5):
        GPIO.output(11,GPIO.LOW)
        time.sleep(0.1)
        GPIO.output(11,GPIO.HIGH)
        time.sleep(0.1)

def close_all(cap):
    """ close handle"""
    cap.release()
    cv2.destroyAllWindows()
    
def logic_all(Turnflag,signalResult,angle,frontD,flag_ped,LongLine_Flag):
    global brake_index
    global Turn_index
    global speedStr
    global speedFlag
    global flag_ped_count
    global signal_turn_index
    if signalResult[0][1] > 700:
        #print("signal")
        if signalResult[0][0] == 0:
            order = str("1,0,95")
            print(order)
            ser.write(order)
            #print("beforeStop")
            time.sleep(2.7)
            #print("afterStop")
        elif signalResult[0][0] == 1:
            order = str("1,"+speedStr+",130")
            #print(order)
            ser.write(order)
            turn_right_led(0.5,2.2)
            signal_turn_index=1
            #time.sleep(2.4)
        elif signalResult[0][0] == 2:
            order = str("1,"+speedStr+",130")
            #print(order)
            ser.write(order)
            turn_right_led(0.5,2.2)
            signal_turn_index=1
            #time.sleep(3)
        elif signalResult[0][0] == 3:
            #print("##########"+str(speedFlag))
            if speedFlag == 1:
                speedStr = '18'
                speedFlag = 2
                order = str("1,"+speedStr+",130")
            elif speedFlag == 2:
                #print("Good")
                speedStr = '15'
                speedFlag = 3
                order =str("1,"+speedStr+",130")
    elif signal_turn_index==1 & LongLine_Flag==1:
         order = str("1,15,45")
         ser.write(order)
         turn_left_led(0.5,2.5)
         signal_turn_index==0
    
    elif flag_ped==1:
        flag_ped_count=1
        #print("pedes!!")
        order=str("1,10,97")
        ser.write(order)
        GPIO.output(35,GPIO.HIGH)
        GPIO.output(37,GPIO.HIGH)
        time.sleep(3.2)
        GPIO.output(35,GPIO.LOW)
        GPIO.output(37,GPIO.LOW)
    
    elif Turnflag>0:
        if Turnflag==1:
            order = str("1,15,45")
            ser.write(order)
            turn_left_led(0.5,2.5)
            #time.sleep(2.5)
        else:
            order = str("1,15,130")
            Turn_index=Turn_index+1
            ser.write(order)
            turn_right_led(0.5,2.5)
            #time.sleep(2.5)
    elif frontD<40:
        brake_index=brake_index+1
        order=str("1,0,95")
        ser.write(order)
        stop_led(1)
        #time.sleep(3)
        if brake_index==4:
            order=str("1,0,95")
            ser.write(order)
            time.sleep(1)
            order=str("1,13,120")
            ser.write(order)
            turn_right_led(0.5,2.2)
            #time.sleep(2.2)
            order=str("1,13,40")
            ser.write(order)
            turn_left_led(0.5,4.0)
            #time.sleep(4.4)
            order=str("1,13,130")
            ser.write(order)
            turn_right_led(0.5,1.8)
            #time.sleep(1.8)
            speedStr = '13'
    
    else:
        order = str("1,"+speedStr+","+str(angle))
        #print(order)
    #print(order)
    return order

def right_distance():
    GPIO.output(36,GPIO.LOW)
    time.sleep(0.002)
    GPIO.output(36,GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(36,GPIO.LOW)
    start = time.time()

    while GPIO.input(32) == 0:
        start = time.time()
    while GPIO.input(32) == 1:
        stop = time.time()
    elapsed = stop - start
    distance = elapsed * 34300
    distance = distance /2
    #print "Right_Distance : %.lfcm" % distance
    return distance

def front_distance():
    GPIO.output(38,GPIO.LOW)
    time.sleep(0.0002)
    GPIO.output(38,GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(38,GPIO.LOW)
    start = time.time()

    while GPIO.input(15) == 0:
        start = time.time()
    while GPIO.input(15) == 1:
        stop = time.time()
    elapsed = stop - start
    distance = elapsed * 34300
    distance = distance /2
    #print "Front_Distance : %.lfcm" % distance
    return distance
        

     
if __name__ == '__main__':
    try:
        flag = True
        leftTemp = cv2.imread("leftTemp.jpg")
        rightTemp = cv2.imread("Temp.jpg")
        redTemp = cv2.imread("red.jpg")
        speedTemp = cv2.imread("speedTemp.jpg")
        #leftTemp =cv2.resize(leftTemp,(30,30),fx=0,fy=0)
        rightTemp =cv2.resize(rightTemp,(30,30),fx=0,fy=0)
        redTemp =cv2.resize(redTemp,(30,30),fx=0,fy=0)
        time.sleep(5)
        start_Beep()

        #cap=set_cam_info()

        #start=datetime.datetime.now()
        count=0
        #ret,img = cap.read()
        camera,raw = set_picamera()
        start_num=1
        GPIO.output(35,GPIO.LOW)
        GPIO.output(37,GPIO.LOW)
        ser.write("1,13,90")
        time.sleep(0.2)
        ser.write("1,13,130")
        turn_right_led(0.5 , 3.4)
        '''
        ser.write("1,13,90")
        time.sleep(2)
        ser.write("1,0,94")
        GPIO.output(33,GPIO.HIGH)
        GPIO.output(31,GPIO.HIGH)
        time.sleep(0.6)
        GPIO.output(33,GPIO.LOW)
        GPIO.output(31,GPIO.LOW)
        time.sleep(0.6)
        GPIO.output(33,GPIO.HIGH)
        GPIO.output(31,GPIO.HIGH)
        time.sleep(0.6)
        GPIO.output(33,GPIO.LOW)
        GPIO.output(31,GPIO.LOW)
        time.sleep(1)
        #time.sleep(3.7)
        '''
        for frame in camera.capture_continuous(raw,format = "bgr",use_video_port=True):
        #while True:
            #AEB = front_distance()
            #while(AEB<15):
                #ser.write("0,0,90")
                #AEB = front_distance()
                #print(str(AEB))
            #front_D=100
            # read image
            #img = cv2.imread("image/image5.jpg")
            #ret,img = cap.read()
            #camera.capture(raw,format = "bgr")
            img = frame.array
            #print(img.shape)
            #cv2.imshow("show",img)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

           ##
            if speedFlag<3: 
                if flag == True :
                    signalResult = functionSig.signalDetect(img,leftTemp,rightTemp,redTemp,speedTemp)
                    if signalResult[0][1] is not 0:
                        timeStart= datetime.datetime.now()
                        flag = False
                else:
                    timeNow = datetime.datetime.now()
                    timeIn = timeNow-timeStart
                    if timeIn.seconds > 6:
                       flag = True
            else:
                signalResult = [[0,0,0]]
            
            #signalResult=[]
            #signalResult = functionSig.signalDetect(img,leftTemp,rightTemp,redTemp,speedTemp)
            #print("SignalDetected:" + str(signalResult))
            ##
            Turnflag=0
            
            if Turn_index>=2:
                front_D = front_distance()
                speedStr=str(13)
            else:
                front_D = 100
                [Turnflag,LongLine_Flag]=TurnJudgement(gray)
            ###########################################
            [offset,img_out,flag_ped]=img_process(gray)
            if flag_ped==1 and flag_ped_count==1:
                flag_ped=0
            #############################################
            if brake_index>=1:
                right_D = right_distance()
                if ((right_D < 20 ) and (not p_flag1) and (not p_flag2) and (not p_flag3)):
                    p_count = p_count + 1
                    if (p_count > 1):
                        p_flag1 = 1
                        p_count = 0
                if ((right_D > 20) and p_flag1 and (not p_flag2) and (not p_flag3)):
                    p_count = p_count + 1
                    if (p_count > 1):
                        p_flag2 = 1
                        p_count = 0                   
                if ((right_D < 20) and p_flag1 and p_flag2 and (not p_flag3)):
                    p_count = p_count + 1
                    if (p_count > 1):
                        p_flag3 = 1
                        p_count = 0
                if (p_flag3):
                    ser.write("1,13,90")
                    time.sleep(0.85)
                    ser.write("0,0,90")
                    time.sleep(1)
                    GPIO.output(35,GPIO.HIGH)
                    GPIO.output(37,GPIO.HIGH)
                    ser.write("2,13,130")
                    GPIO.output(11,GPIO.LOW)
                    GPIO.output(33,GPIO.HIGH)
                    time.sleep(0.5)
                    GPIO.output(11,GPIO.HIGH)
                    GPIO.output(33,GPIO.LOW)
                    time.sleep(0.5)
                    GPIO.output(11,GPIO.LOW)
                    GPIO.output(33,GPIO.HIGH)
                    time.sleep(0.5)
                    GPIO.output(11,GPIO.HIGH)
                    GPIO.output(33,GPIO.LOW)
                    time.sleep(0.5)
                    GPIO.output(11,GPIO.LOW)
                    GPIO.output(33,GPIO.HIGH)
                    time.sleep(0.5)
                    GPIO.output(11,GPIO.HIGH)
                    GPIO.output(33,GPIO.LOW)
                    time.sleep(0.5)
                    GPIO.output(11,GPIO.LOW)
                    GPIO.output(33,GPIO.HIGH)
                    time.sleep(0.5)
                    GPIO.output(11,GPIO.HIGH)
                    GPIO.output(33,GPIO.LOW)
                    time.sleep(0.5)
                    GPIO.output(11,GPIO.LOW)
                    GPIO.output(33,GPIO.HIGH)
                    time.sleep(0.4)
                    #GPIO.output(11,GPIO.HIGH)
                    #GPIO.output(33,GPIO.LOW)
                    #time.sleep(0.1)
                    #time.sleep(4.8)
                    ser.write("2,9,90")
                    GPIO.output(33,GPIO.LOW)
                    GPIO.output(11,GPIO.HIGH)
                    time.sleep(1.2)
                    '''GPIO.output(11,GPIO.LOW)
                    time.sleep(0.5)
                    GPIO.output(11,GPIO.HIGH)
                    time.sleep(0.4)'''
                    '''GPIO.output(11,GPIO.HIGH)
                    time.sleep(0.8)
                    GPIO.output(11,GPIO.LOW)
                    time.sleep(0.8)'''
                    #time.sleep(2.5)
                    ser.write("0,13,90")
                    GPIO.output(33,GPIO.LOW)
                    GPIO.output(11,GPIO.HIGH)
                    time.sleep(0.15)
                    GPIO.output(11,GPIO.LOW)
                    time.sleep(0.4)
                    start_Beep()
                    GPIO.output(35,GPIO.LOW)
                    GPIO.output(37,GPIO.LOW)
                    break
                    
                
            #angle=95
            angle=get_angle(offset)
            #angle=140
            order=logic_all(Turnflag,signalResult,int(angle),front_D,flag_ped,LongLine_Flag)
            signalResult = [[0,0,0]]
            #order = str("1,0,120")
            #cv2.imshow('fig',img_out)
            #print(angle)
            #cv2.imwrite("image1/image"+str(start_num)+".jpg",img_out)
            #cv2.imwrite("image1/imagea"+str(start_num)+".jpg",imga)
            #order="1,0,"+str(int(120))
            #order="1,0,90"
            n = ser.write(order)
            raw.truncate(0)
            
            if cv2.waitKey(2) & 0xff == ord("q"):
                end=datetime.datetime.now()
                #####n = ser.write("0,0,95")
                print (end-start)
                print ("time:"+str(count))
                #cv2.imwrite("test.jpg",frame)
                break
                
            '''
            if cv2.waitKey(1000//12) & 0xff == ord("c"):
                #end=datetime.datetime.now()
                #####n = ser.write("0,0,95")
                print ('11')
                cv2.imwrite("image/image"+str(start_num)+".jpg",img)
                start_num=start_num+1
                #cv2.imwrite("test.jpg",frame)
                #break
                '''
            count=count+1
            #if count>10:
                #end=datetime.datetime.now()
                #plt.figure()
                #plt.imshow(img_ori)
                #cv2.imshow('fig',img_ori)
                #cv2.imshow(img_out)
                #plt.figure()
                #plt.imshow(img_out)
                #print (end-start)
                #print ("time:"+str(count))
                #break
    except KeyboardInterrupt:  
        if ser != None:
            #end=datetime.datetime.now()
            print ("end-start")
            print ("time:"+str(count))
            str1 = "1,0,90"
            n = ser.write(str1)
            time.sleep(0.2)
            print ("\nfinish")
            #str1 = "0,20,110"
            #n = ser.write(str1)
            ser.close() 
########################################
