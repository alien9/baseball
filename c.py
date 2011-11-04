#!/usr/bin/python

import math
import cwiid
import time

X=1024
Y=768
A=60/360.0*2*math.pi #ângulo da lente
D=0.2

print 'Press 1+2 on your Wiimote now...'
wm = cwiid.Wiimote()

time.sleep(1)

wm.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC | cwiid.RPT_IR
wm.led = 1
def f(x): return not not x

while True:
  pts=filter(f,wm.state['ir_src'])
  if len(pts)==2:
    center=[(pts[1]['pos'][0]+pts[0]['pos'][0])/2,(pts[1]['pos'][1]+pts[0]['pos'][1])/2]
    length=((pts[1]['pos'][0]-pts[0]['pos'][0])**2+(pts[1]['pos'][1]-pts[0]['pos'][1])**2)**0.5
    print center
    print length
    #d=((pts[0]['pos'][0]-pts[1]['pos'][0])**2+(pts[0]['pos'][1]-pts[1]['pos'][1])**2)**0.5
