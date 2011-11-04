#! /usr/bin/python

import math
import cwiid
import time
import Image, ImageDraw
import barulho


apit = 'blast_from_clothes_cleaning_machine.mp3'
sta = 'fm_synthesis_effect_5_good_for_sci_fi_sounds.mp3'
put = 'punch25.mp3'

X=1024
Y=768
A=60/360.0*2*math.pi #angulo da lente
D=0.2
DELAY=20
DAC=40

def mtest(p):
    return not not p

imx=Image.new("RGB", [1000, 50])
draw = ImageDraw.Draw(imx)
print 'Press 1+2 on your Wiimote now...'
wm = cwiid.Wiimote()
barulho.toca(sta)
wm.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC | cwiid.RPT_IR
i=0;

things=[]

while wm:
    time.sleep(0.01)
    ps = filter(mtest,  wm.state['ir_src'])
    if len(ps) == 2:
        print ps[0]['pos'][0]
        d0=((ps[0]['pos'][0]-512)**2+(ps[0]['pos'][1]-384))**0.5
        d1=((ps[1]['pos'][0]-512)**2+(ps[1]['pos'][1]-384))**0.5
        print d0+" "+d1
    
    x=wm.state['acc'][0]
    y=wm.state['acc'][1]
    z=wm.state['acc'][2]
    things.append(y)
    siny=(y-100)/50.0
    if siny > 1:
        siny=1
    if siny < -1:
        siny=-1
    
    angle=math.asin(siny)
    print angle
    if len(things)>DELAY:
        old=things.pop(0)
        if y-old > DAC:
            barulho.toca(put)
            things=things[DELAY/3:DELAY]
    i+=1
    if wm.state['buttons'] & 4 == 4:
        print "B pressed"
        barulho.toca(apit)
        barulho.toca(put)

imx.save("x.png")
barulho.toca("alert_sound_ideal_for_software_systems_etc_ver_15.mp3")
