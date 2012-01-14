#!/usr/bin/python
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
wm=None

SPRAY = [5,  80]
DISTA = [190, 214]
xt=800.0
yt=600.0

xp=xt/X
yp=yt/Y
def zangle(n):
    zu = (n-95) / 25.0 - 1
    if zu > 1: 
        zu=1
    if zu < -1 :
        zu = -1
    return zu

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
wm=None
def wiifind(messy,bessy):
    def runner(tela, wii):
        pitch=0
        roll=0
        while 1:
            if wii:
                cur=ImageTk.PhotoImage(curry)
                ps = filter(mtest,  wii.state['ir_src'])
                dist=0
                du=0
                mid=[]
                if wii.state['buttons'] & 2048 :
                    if len(ps)>1 :
                        du=pow(pow(ps[1]['pos'][0]-ps[0]['pos'][0], 2)+pow(ps[1]['pos'][1]-ps[0]['pos'][1], 2), 0.5)
                        DISTA[1]=int(du)
                        pitch=math.asin(zangle(wii.state['acc'][1]))
                        roll=math.asin(zangle(wii.state['acc'][0]))
                        print "distancia mínima"
                        print DISTA
                if wii.state['buttons'] & 1024 :
                    if len(ps)>1 :
                        du=pow(pow(ps[1]['pos'][0]-ps[0]['pos'][0], 2)+pow(ps[1]['pos'][1]-ps[0]['pos'][1], 2), 0.5)
                        DISTA[0]=int(du)
                        print "distancia máxima"
                        print DISTA

                if len(ps)>1 :
                    du=pow(pow(ps[1]['pos'][0]-ps[0]['pos'][0], 2)+pow(ps[1]['pos'][1]-ps[0]['pos'][1], 2), 0.5)
                    dist=int(sprawl(du))
                    xo=(ps[0]['pos'][0]+ps[1]['pos'][0]) / 2.0 - 512
                    yo=384 - (ps[0]['pos'][1]+ps[1]['pos'][1]) / 2.0
                    if ps[1]['pos'][0] != ps[0]['pos'][0] :
                        teta=1 * math.atan(1.0 * (ps[1]['pos'][1] - ps[0]['pos'][1] )/(ps[1]['pos'][0] - ps[0]['pos'][0] ))
                    else :
                        teta = math.pi / 2.0
                    x=xp * (512 + xo * math.cos(teta) - yo * math.sin(teta) )
                    y=yp * (384 + xo * math.sin(teta) + yo * math.cos(teta) )
                    if wii.state['buttons'] & 4 :
                        gradient=ims[dist]
                        tela.create_image(xt-x-dist/2, yt-y-dist/2, image=gradient)

                    tela.create_image(xt-x-16, yt-y-16, image=cur)
			
                else :
                    ant=None
                if wii.state['buttons'] & 1 :
                    tela.delete('all')
                if wii.state['buttons'] & 2 :
                    break
    #        barulho.toca#("alert_sound_ideal_for_software_systems_etc_ver_15.mp3")
    #        top.destroy()
    #        exit()
   
    print 'Conecte Wii...'
    wm = cwiid.Wiimote()
    try:
        barulho.toca(sta)
    except:
        print "\nseu cala boca\n"
    wm.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC | cwiid.RPT_IR
    thread.start_new_thread( runner, ( c, wm ) )
    

i=0;
top = Tkinter.Tk()

things=[]
    

c = Tkinter.Canvas(top, bg="black", height=yt, width=xt)
e=Image.open("empty.png")

curry=Image.open("cursor.png")

ims={}

for i in range(SPRAY[0],SPRAY[1]+1) :
    img=Image.open("buff.png")
    iw=img.resize((i,i), Image.ANTIALIAS)
    opacity=1.0*(SPRAY[1]-i)/(SPRAY[1]-SPRAY[0])
    #print opacity
    alpha = iw.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    iw.putalpha(alpha)
    ims[i]=ImageTk.PhotoImage(iw)

thread.start_new_thread( wiifind, ( c, wm ) )
c.pack()


top.mainloop()
