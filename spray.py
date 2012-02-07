#!/usr/bin/python
# coding=UTF8

from configobj import ConfigObj
import os
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
import re

apit = 'blast_from_clothes_cleaning_machine.mp3'
sta = 'fm_synthesis_effect_5_good_for_sci_fi_sounds.mp3'
put = 'punch25.mp3'
qua = 'BEEPKIND.WAV'

config = ConfigObj("spray.conf")

try :
    PAL =  [int(config['palheta'][0]),int(config['palheta'][1])]
except :
    PAL=[10,10]

try :
    MAS = [int(config['mask'][0]),int(config['mask'][1])]
except :
    MAS = [500,100]

X=1024.0
Y=768.0
A=60/360.0*2*math.pi #angulo da lente
D=0.2
DELAY=20
DAC=40
wm=None
top = Tkinter.Tk()
SPRAY = [5,  80]
try:
    DISTA = [int(config['dista'][0]),int(config['dista'][1])]
except :
    DISTA = [190, 214]
xt = 1024 #top.winfo_screenwidth()
yt = 768 #top.winfo_screenheight()
top.focus_set() # <-- move focus to this widget
top.bind("<Escape>", lambda e: e.widget.quit())



xp=1.0*xt/X
yp=1.0*yt/Y

def saveconf():
    config['mask']=MAS
    config['palheta']=PAL
    config['dista']=DISTA
    config.write()
    
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
    if (DISTA[1]-DISTA[0])*(SPRAY[1]-SPRAY[0]) != 0 :
        return SPRAY[1]-1.0*(d-DISTA[0])/(DISTA[1]-DISTA[0])*(SPRAY[1]-SPRAY[0])
    return 10
def sortof(p) :
    p=sorted(p, key=lambda point: point['pos'][1])
    p.reverse()
    return p
    
def sortx(p) :
    p=sorted(p, key=lambda point: point['pos'][0])
    return p
    
def ispic(w):
    ru = re.compile('^pic_\d+\.jpg')
    gu = ru.search(w)
    return not not gu
    
def pinta(iw, cor) :
      alpha = iw.split()[3]
      iw = Image.new('RGB', alpha.size, cor)
      iw.paste(iw.convert('RGB'), mask=alpha)
      iw.putalpha(alpha)
      return iw
wm=None
def wiifind(messy,bessy):
    def runner(tela, wii):
        zona = Image.new('RGBA', (xt,yt), (0,0,0))
        canv = ImageTk.PhotoImage(zona)
        tela.create_image(xt/2,yt/2, image=canv)
        masquerades={}
        REVES = False
        cor=0
        pitch=0
        roll=0
        palha = None
        maska = None
        maskara = None
        stencil = None
        mu = None
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
                        saveconf()
                if wii.state['buttons'] & 1024 :
                    if len(ps)>1 :
                        du=pow(pow(ps[1]['pos'][0]-ps[0]['pos'][0], 2)+pow(ps[1]['pos'][1]-ps[0]['pos'][1], 2), 0.5)
                        DISTA[0]=int(du)
                        print "distancia máxima"
                        print DISTA
                        saveconf()

                if len(ps)>1 :
                    du=pow(pow(ps[1]['pos'][0]-ps[0]['pos'][0], 2)+pow(ps[1]['pos'][1]-ps[0]['pos'][1], 2), 0.5)
                    dist=int(sprawl(du))
                    xo=(ps[0]['pos'][0]+ps[1]['pos'][0]) / 2.0
                    yo=(ps[0]['pos'][1]+ps[1]['pos'][1]) / 2.0

                    if ps[1]['pos'][0] != ps[0]['pos'][0] :
                        teta=math.atan(1.0 * (ps[1]['pos'][1] - ps[0]['pos'][1] )/(ps[1]['pos'][0] - ps[0]['pos'][0] ))
                    else :
                        teta = math.pi / 2.0

#                    if REVES :
#                        teta -= math.pi / 2.0
                    x=xp * (512 + (xo-512) * math.cos(teta) + (yo-384) * math.sin(teta) )
                    y=yp * (384 + (yo-384) * math.cos(teta) - (xo-512) * math.sin(teta) )
                    
                    #coordenadas para tela:
                    
                  
                    xu = int(x)
                    yu = int(y)
                    if REVES:
                        yu = yt-yu
#                    if not REVES :
                    xu = int(xt - x)
                    if wii.state['buttons'] & 4 :
                        if palha :
                            yk = yu - ( PAL[1] - 267 )
                            if yk > 0 and yk < 535 :
                                cor = int(math.floor( 12 * (yk-18) / 535 ))
                        elif maska:
                            mk = xu - ( MAS[0] - 282 )
                            if mk > 0 and mk < 566 :
                                maskara = int(math.floor( 5 * mk / 560))
                                print "i've set up maskara as "+str(maskara)  
                        else :
                            gradient=imf[dist][cor]
                            if mu != None:
                                
                                if not cor in masquerades :
                                    masquerades[cor]={}
                                if not maskara in masquerades[cor] :
                                    masquerades[cor][maskara]={}
                                if not teta in masquerades[cor][maskara] :
                                    j=masks[maskara].rotate(teta / (2*math.pi) * -360).copy()
                                    masquerades[cor][maskara][teta] = ImageTk.PhotoImage(pinta(j,colors[cor]))
                                #mi=ImageTk.PhotoImage(masquerades[cor][maskara][teta])
                                tela.create_image(xu,yu,image=masquerades[cor][maskara][teta])


                                #zona.paste(pinta(j,colors[cor]), (xu-j.size[0]/2,yu-j.size[1]/2),j)
                                #canv = ImageTk.PhotoImage(zona)
                                #tela.create_image(xt/2,yt/2, image=canv)
                                #tela.delete(mu)
                                ant=None
                            else :
                                tela.create_image(xu, yu, image=gradient)
                                #zona.paste(ims[dist][cor], (xu-dist/2,yu-dist/2), ims[dist][cor])
                                #canv = ImageTk.PhotoImage(zona)
                                #tela.create_image(xt/2,yt/2, image=canv)
                                ago = {'x':xu, 'y':yu}
                            #if not not ant :
                            #    du = distancia(ago, ant)
                            #    if du > dist :
                            #        passos = 2.5 * du / dist
                            #        if passos < 25 :
                            #            inc = {'x':(ago['x']-ant['x'])/passos,'y':(ago['y']-ant['y'])/passos }
                            #            for pu in range(0, int(passos)) :
                            #                ago['x'] += inc['x']
                            #                ago['y'] += inc['y']
                            #                #zona.paste(ims[dist][cor], (int(ago['x']-dist/2),int(ago['y']-dist/2)), ims[dist][cor])
                            #                tela.create_image(int(ago['x']), int(ago['y']), image=gradient)
                                        #tela.create_image(xt/2,yt/2, image=canv)
                            
                            ant = {'x':xu, 'y':yu}
                    else:
                        ant = None
                        if xu < PAL[0] :
                            if not palha :
                                palha = tela.create_image(PAL[0], PAL[1], image=pal)
                        if not not palha :
                            if xu > PAL[0] + 100 :
                                tela.delete(palha)
                                palha = None
                        
                        if yu < MAS[1] :
                            if not maska :
                                maskara = None
                                if mu:
                                    tela.delete(mu)
                                    mu = None
                                maska = tela.create_image(MAS[0], MAS[1], image=mas)
                        if not not maska :
                            if yu > MAS[1] + 200 :
                                tela.delete(maska)
                                maska = None      
                    if wii.state['buttons'] & 256 :
                        PAL[0] = int(xu)
                        PAL[1] = int(yu)
                        saveconf()
                    if wii.state['buttons'] & 512 :
                        MAS[0] = int(xu)
                        MAS[1] = int(yu)
                        saveconf()

                    tela.create_image(xu, yu, image=cur)
                    if maskara != None:
                        if not masks[maskara] :
                            maskara = None
                        elif not wii.state['buttons'] & 4 :
                            stencil=ImageTk.PhotoImage(masks[maskara].rotate(teta / (2*math.pi) * -360))
                            mu = tela.create_image(xu, yu, image=stencil)
			
                else :
                    ant=None
                if wii.state['buttons'] & 1 :
                    tela.delete('all')
                    tela.create_rectangle(0, 0, xt, yt, width=0, fill='black')
                    #zona = Image.new('RGBA', (xt,yt), (0,0,0))
                    #canv = ImageTk.PhotoImage(zona)
                if wii.state['buttons'] & 8 :
                    barulho.toca(put)
                    REVES = not REVES
                    while wii.state['buttons'] & 8 :
                        print "peraí"
                    
                if wii.state['buttons'] & 2 :
                    break
    #        barulho.toca#("alert_sound_ideal_for_software_systems_etc_ver_15.mp3")
    #        top.destroy()
    #        exit()
   
    print 'Conecte Wii...'
    try:
        wm = cwiid.Wiimote()
    except:
        print "Tente de novo\n"
        thread.start_new_thread( runner, ( messy,bessy) )
        exit()
    barulho.toca(sta)
    wm.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC | cwiid.RPT_IR
    thread.start_new_thread( runner, ( c, wm ) )
    

i=0;


things=[]
    

c = Tkinter.Canvas(top, bg="black", height=yt, width=xt)
def apag(eve):
    if eve.char == 'r' or eve.char == 'R': 
        c.delete('all')
        c.create_rectangle(0, 0, xt, yt, width=0, fill='black')
    if eve.char == 'p' or eve.char == 'P' :
        #printa imagem pra mandar
        if not os.path.exists('images') :
            os.mkdir('images')
        fl = os.listdir('images')
        fl=filter(ispic,fl)
        fl.sort()
        n = 1
        if len(fl) :
            ru = re.compile('_(\d+)\.jpg')
            gu = ru.search(fl.pop())
            if gu!=None :
                n = int(gu.group(1))+1
        c.postscript(file="images/pic_"+(str(n).zfill(5))+".eps") # save canvas as encapsulated postscript
        import subprocess as sp
        child = sp.Popen("mogrify -format jpg images/pic_"+(str(n).zfill(5))+".eps", shell=True) # convert eps to jpg with ImageMagick
        child.wait()
        
    if eve.char == 'q' or eve.char == 'Q':
        exit()

top.bind_all("<Key>", apag )
e=Image.open("empty.png")

curry=Image.open("cursor.png")
pal=Image.open("palheta.png")


pal = ImageTk.PhotoImage(pal)
mas=Image.open("masks.png")
mas = ImageTk.PhotoImage(mas)
ims={}
imf={}
masks=[]
colors=[(255,0,0), (200,0,166), (150,0,215), (106,0,212), (0,0,215), (22,116,212), (44,189,206), (48,204,156), (102,205,0), (204,196,1), (202,124,0), (0,0,0)]

for i in range(SPRAY[0],SPRAY[1]+1) :
    ims[i] = {}
    imf[i] = {}
    for co in range(0, len(colors)) :
      img=Image.open("buff.png")
      iw=img.resize((i,i), Image.ANTIALIAS)
      opacity=1.0 #*(SPRAY[1]-i)/(SPRAY[1]-SPRAY[0])
      #print opacity
      alpha = iw.split()[3]
      alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
      iw = Image.new('RGB', alpha.size, colors[co])
      iw.paste(iw.convert('RGB'), mask=alpha)
      iw.putalpha(alpha)
      imf[i][co]=ImageTk.PhotoImage(iw)
      ims[i][co]=iw

for i in range(0, 6) :
    k = Image.open("masks_"+str(i)+".png")
    masks.append(k)



thread.start_new_thread( wiifind, ( c, wm ) )
c.pack()


top.mainloop()
