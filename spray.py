#! /usr/bin/python
# coding=UTF8

import math
import cwiid
import time
import Image, ImageDraw, ImageEnhance
import barulho
import Tkinter
import tkMessageBox
import thread
import threading
import ImageTk

apit = 'blast_from_clothes_cleaning_machine.mp3'
sta = 'fm_synthesis_effect_5_good_for_sci_fi_sounds.mp3'
put = 'punch25.mp3'

X=1024.0
Y=768.0
A=60/360.0*2*math.pi #angulo da lente
D=0.2
DELAY=20
DAC=40

SPRAY = [25,  80]
DISTA = [190, 214]
xt=840.0
yt=630.0

xp=xt/X
yp=yt/Y

def mtest(p):
    return not not p
def distancia(p0,p1) :
    return pow(pow(1.0*p1['x']-p0['x'],2.0)+pow(1.0*p1['y']-p0['y'],2.0),0.5)
def sprawl(d):
    if d > DISTA[1]:
        d = DISTA[1]
    if d < DISTA[0]:
        d = DISTA[0]
    if SPRAY[0]>=SPRAY[1] :
        SPRAY[1]=SPRAY[0]+1
    return SPRAY[1]-1.0*(d-DISTA[0])/(DISTA[1]-DISTA[0])*(SPRAY[1]-SPRAY[0])
def sortof(p) :
    p=sorted(p, key=lambda point: point['pos'][1])
    p.reverse()
    return p
def sortx(p) :
    p=sorted(p, key=lambda point: point['pos'][0])
    return p   
print 'Press 1+2 on your Wiimote now...'
wm = cwiid.Wiimote()
barulho.toca(sta)
wm.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC | cwiid.RPT_IR
i=0;
top = Tkinter.Tk()

things=[]
def runner(tela, wii):
    while wii:
        time.sleep(0.01)
        ps = sortof(filter(mtest,  wii.state['ir_src']))
        dist=0
        du=0
        mid=[]
        if wii.state['buttons'] & 2048 :
            if len(ps)>2 :
                du=pow(pow(ps[1]['pos'][0]-ps[0]['pos'][0], 2)+pow(ps[1]['pos'][1]-ps[0]['pos'][1], 2), 0.5)
                DISTA[1]=int(du)
                print "distancia mínima"
                print DISTA
        if wii.state['buttons'] & 1024 :
            if len(ps)>2 :
                du=pow(pow(ps[1]['pos'][0]-ps[0]['pos'][0], 2)+pow(ps[1]['pos'][1]-ps[0]['pos'][1], 2), 0.5)
                DISTA[0]=int(du)
                print "distancia máxima"
                print DISTA
        if wii.state['buttons'] & 4 :
            if len(ps)>2 :
                du=pow(pow(ps[1]['pos'][0]-ps[0]['pos'][0], 2)+pow(ps[1]['pos'][1]-ps[0]['pos'][1], 2), 0.5)
                dist=int(sprawl(du))
                po=sortx([ps[0],ps[1]])
                #print po
                if po[1]['pos'][0] != po[0]['pos'][0] :
                    m=1.0*(po[1]['pos'][1]-po[0]['pos'][1])/(po[1]['pos'][0]-po[0]['pos'][0])
                    
                    #print m
                    if m != 0.0 : 
                    #    #refazer isto
                        xx=xt*( ps[2]['pos'][0]/m + ps[2]['pos'][1] - po[0]['pos'][1] + m*po[0]['pos'][0] )/(m+1/m)
                    else :
                        xx=xt*(ps[2]['pos'][0]-po[0]['pos'][0])/(po[1]['pos'][0]-po[0]['pos'][0])
                    #mid = [ (ps[1]['pos'][0]+ps[0]['pos'][0]) / 2.0, (ps[1]['pos'][1]+ps[0]['pos'][1]) / 2.0 ]
                    
                    print xx
                    mid = [ xx, (ps[1]['pos'][1]+ps[0]['pos'][1]) / 2.0 ]
            #else :
            #    if len(ps)>0 :
            #        if ps[0]['pos'][0] > X/2 :
            #            mid = [ ps[0]['pos'][0]+du/2.0, (ps[0]['pos'][1]+ps[0]['pos'][1]) / 2.0 ]
            #        else :
            #            mid = [ ps[0]['pos'][0]-du/2.0, (ps[0]['pos'][1]+ps[0]['pos'][1]) / 2.0 ]
            if len(mid) > 1 and dist > 0:
                gradient=ims[dist]
                #print mid
                pos={'x':round(xt-xp*(mid[0]+dist/2.0)), 'y':round(yp*(mid[1]+dist/2.0))}
                tela.create_image(pos['x'], pos['y'], image=gradient)
                #if (not not ant) and (dist > 0):
                #    di = distancia(pos, ant) / dist
                #    print di
                    #pasx=1.0 * (pos['x']-ant['x']) / di
                    #pasy=1.0 * (pos['y']-ant['y']) / di
                    
                ant={'x':pos['x'], 'y':pos['y']}
        else :
            ant=None
        if wii.state['buttons'] & 1 :
            tela.delete('all')
        if wii.state['buttons'] & 2 :
            break
    barulho.toca("alert_sound_ideal_for_software_systems_etc_ver_15.mp3")
    top.destroy()
    exit()


c = Tkinter.Canvas(top, bg="black", height=yt, width=xt)
e=Image.open("empty.png")

ims={}

for i in range(SPRAY[0],SPRAY[1]+1) :
    img=Image.open("buff.png")
    iw=img.resize((i,i), Image.ANTIALIAS)
    opacity=1.0*(SPRAY[1]-i)/(SPRAY[1]-SPRAY[0])
    print opacity
    alpha = iw.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    iw.putalpha(alpha)
    ims[i]=ImageTk.PhotoImage(iw)

thread.start_new_thread( runner, ( c, wm ) )
c.pack()


top.mainloop()
