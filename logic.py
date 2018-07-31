# -*- coding: utf-8 -*-
"""
Created on Tue Jul 31 13:13:06 2018

@author: lijiancong
"""
import time
from lower_level_control import turn_left_led,turn_right_led,stop_led
def logic_all(Turnflag,signalResult,angle,frontD,flag_ped,LongLine_Flag,ser):
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
        time.sleep(3.2)

    
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