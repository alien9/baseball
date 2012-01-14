#! /usr/bin/python

import math
import cwiid
import time
import Image, ImageDraw
import pyaudio
import mad
import sys
import barulho

class Lata:
  def __init__(self, soq, timeout):
    self.soq=soq
    self.timeout=timeout

  def go(self):
    sta = 'fm_synthesis_effect_5_good_for_sci_fi_sounds.mp3'
    put = 'punch25.mp3'

    X=1024
    Y=768
    A=60/360.0*2*math.pi #angulo da lente
    D=0.2
    DELAY=20
    DAC=40

    #imx=Image.new("RGB", [1000, 50])
    #draw = ImageDraw.Draw(imx)
    ok = False
    wm = None
    while not ok:
      try:
        print 'Press 1+2 on your Wiimote now...'
        wm = cwiid.Wiimote()
        ok = True
      except RuntimeError:
        print 'Bluetooth esta mal.'
        time.sleep(2)
    barulho.toca(sta)
    wm.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC 
    i=0;

    things=[]
    while self.soq.connect:
        time.sleep(0.01)
        #print wm.state
        x=wm.state['acc'][0]
        y=wm.state['acc'][1]
        z=wm.state['acc'][2]
        things.append(y)
     #   draw.rectangle([i, x-100, 1+i, x-99], fill='#ff0000', outline=None)
     #   draw.rectangle([i, y-100, 1+i, y-99], fill='#00ff00', outline=None)
     #   draw.rectangle([i, z-100, 1+i, z-99], fill='#0000ff', outline=None)
        siny=(y-100)/50.0
        if siny > 1:
            siny=1
        if siny < -1:
            siny=-1
        
        angle=math.asin(siny)
        #print angle
        if len(things)>DELAY:
            old=things.pop(0)
            if y-old > DAC:
                barulho.toca(put)
                things=things[DELAY/3:DELAY]
                self.soq.send(str.encode(str(y-old)+"\0"))
        i+=1
        if wm.state['buttons'] & 4 == 4:
            print "B pressed"
            self.soq.close()
            break

 
    #imx.save("x.png")
    barulho.toca("alert_sound_ideal_for_software_systems_etc_ver_15.mp3")


