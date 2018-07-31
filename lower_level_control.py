# -*- coding: utf-8 -*-
"""
Created on Tue Jul 31 13:05:00 2018

@author: lijiancong
"""
import time
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

p_flag1 = 0
p_flag2 = 0
p_flag3 = 0
p_count = 0

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

def park_out(ser):
    GPIO.output(35,GPIO.LOW)
    GPIO.output(37,GPIO.LOW)
    ser.write("1,13,90")
    time.sleep(0.2)
    ser.write("1,13,130")
    turn_right_led(0.5 , 3.4)

def park_in(ser):
    global p_flag1 
    global p_flag2 
    global p_flag3 
    global p_count 
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
