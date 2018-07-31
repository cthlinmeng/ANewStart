# -*- coding: utf-8 -*  
import serial  
import time
import math
import cv2
import datetime
import functionSig
from getline_0713_car2 import img_process,get_angle,set_cam_info
from straight_canny_resize_LM0724 import TurnJudgement
from lower_level_control import start_Beep,right_distance,front_distance,park_in,park_out
from logic import logic_all
# 打开串口  
ser = serial.Serial("/dev/ttyUSB0", 9600)

# Initialization
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

flag_ped_count=0

# Helpful functions definition
def close_all(cap):
    """ close handle"""
    cap.release()
    cv2.destroyAllWindows()       

     
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
        count=0
        cap=set_cam_info()
        start=datetime.datetime.now() 
        ret,img = cap.read()
        
        #camera,raw = set_picamera()
        start_num=1
        park_out(ser)
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
        #for frame in camera.capture_continuous(raw,format = "bgr",use_video_port=True):
        while True:
            #AEB = front_distance()
            #while(AEB<15):
                #ser.write("0,0,90")
                #AEB = front_distance()
                #print(str(AEB))
            # read image
            ret,img = cap.read()
            #camera.capture(raw,format = "bgr")
            #img = frame.array
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
            ##
            Turnflag=0
            
            if Turn_index>=2:
                front_D = front_distance()
                speedStr=str(13)
            else:
                front_D = 100
                [Turnflag,LongLine_Flag]=TurnJudgement(gray)
            ##
            [offset,img_out,flag_ped]=img_process(gray)
            if flag_ped==1 and flag_ped_count==1:
                flag_ped=0
                
            if brake_index>=1:
                park_in(ser)
                       
            angle=get_angle(offset)
            order=logic_all(Turnflag,signalResult,int(angle),front_D,flag_ped,LongLine_Flag)
            signalResult = [[0,0,0]]
            n = ser.write(order)
            #raw.truncate(0)
            
            if cv2.waitKey(2) & 0xff == ord("q"):
                end=datetime.datetime.now()
                #####n = ser.write("0,0,95")
                print (end-start)
                print ("time:"+str(count))
                #cv2.imwrite("test.jpg",frame)
                break
            count=count+1

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

