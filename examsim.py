import time, datetime, threading #, pygame
import pyttsx3, sys
from playsound import playsound
import keyboard
from gtts import gTTS
from ctypes import *

 
VR=120
tts_engines=["HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_DAVID_11.0"]

engine = pyttsx3.init()
engine.setProperty("rate", VR)
i=0
while True:
    try:
        engine.setProperty("voice", tts_engines[i])
        break
    except:
        i+=1

def play_tts(string):
    global engine
    engine.say(f"{string}")
    engine.runAndWait()

def processTime(hour):
    return (12 if (hour%12==0) else hour%12)
    
def genTime(hour, min):
    hourMy=processTime(hour)
    pmAm="am"
    if hour>12:
        pmAm="pm"
    if min == 0:
        return f"{hourMy} o clock"
    elif min == 15:
        return f"quarter past {hourMy} {pmAm}"
    elif min < 30 and min != 15:
        return f"{min} past {hourMy} {pmAm}"
    elif min == 30:
        return f"half past {hourMy} {pmAm}"
    elif min == 45:
        hourMy = hourMy+1
        if hour==11:
            pmAm="pm"
        elif hour==23:
            pmAm="am"
        hourMy = processTime(hourMy)
        return f"quarter to {hourMy} {pmAm}"
    elif min > 30 and min != 45:
        hourMy = hourMy+1
        newMin = 60-min 
        if hour==11:
            pmAm="pm"
        elif hour==23:
            pmAm="am"
        return f"{newMin} to {hourMy} {pmAm}"

#play_tts("This is a voice test.")
#unused dummy
Paper=input("Paper?")
TIME_MINS=int(input("Time in mins?"))
readRules=""
while readRules!=True and readRules!=False:
    readRules=input("Read rules?")
    if readRules.lower()=="true":
        readRules=True
    elif readRules.lower()=="false":
        readRules=False
def myFunc(root,w,x,y,z, a, block,mouse_listener,keyboard_listener):
    global engine
    global play_tts
    global playsound
    global Paper
    global TIME_MINS
    global readRules
    print("10s. Get the job done.")

    if readRules:
        time.sleep(10)
        playsound("rulesread.mp3")
    time.sleep(10)
    time.sleep(2.5)

    # creating window

    timenow=datetime.datetime.now()
    h1=timenow.hour
    m1=timenow.minute
    h1_=f"{h1}".zfill(2)
    m1_=f"{m1}".zfill(2)
    c=timenow.day
    x.config(text=f"{h1_}:{m1_}")
    #unused dummy
    timenow+=datetime.timedelta(minutes=TIME_MINS)
    d=timenow.day
    h2=timenow.hour
    m2=timenow.minute
    h2_=f"{h2}".zfill(2)
    m2_=f"{m2}".zfill(2)
    z.config(text=f"{h2_}:{m2_}")
    theFollowingMorning=""if c==d else "the following morning"
    play_tts("The time now is " + genTime(h1,m1) + ". We will finish at " + genTime(h2,m2) + f" {theFollowingMorning}. The exam has commenced. ")
    #unused dummy
    playsound("Youmaybegin.mp3")
    def startTimer(TIME_MINS,a):
        timeElaps=TIME_MINS*60
        while timeElaps>0:
            aaa=timeElaps
            hour=0
            while aaa>=3600:
                aaa-=3600
                hour+=1
            min=0
            while aaa>=60:
                aaa-=60
                min+=1
            sec=aaa
            B=""
            if hour>0:
                hour=str(hour)
                B+=f"{hour}:"
            min=str(min).zfill(2)
            B+=f"{min}:"
            sec=str(sec).zfill(2)
            B+=f"{sec}"
            a.config(text=B)
            time.sleep(1)
            timeElaps-=1
        a.config(text="Time's up")
        return
    threading.Thread(target=startTimer,args=[TIME_MINS,a]).start()
    if TIME_MINS>=60:
        time.sleep(((TIME_MINS-30)*60))
        playsound("30mins.mp3")
        time.sleep(25*60)
        playsound("5mins.mp3")
        time.sleep(5*60)
        playsound("time_elapsed.mp3")
    elif TIME_MINS>=10:
        time.sleep(((TIME_MINS-5)*60))
        playsound("5mins.mp3")
        time.sleep(5*60)
        playsound("time_elapsed.mp3")
    else:
        time.sleep(TIME_MINS*60)
        playsound("time_elapsed.mp3")
    windll.user32.BlockInput(False)    
    # Enable mouse and keyboard events
    mouse_listener.stop()
    keyboard_listener.stop()
    root.destroy()
    sys.exit(0)

import tkinter as tk
 
root = tk.Tk()
root.attributes("-fullscreen",True)
root.attributes("-topmost", True)

e = tk.Label(root, text=Paper,font=("Arial",32, "bold"), justify="center")
e.pack(side="top")

w = tk.Label(root, text="Starting Time:",font=("Arial",24))
x = tk.Label(root, text="Not Started",font=("Arial",72))
w.place(
    x=round(root.winfo_screenwidth()/8)
    ,y=round(root.winfo_screenheight()/2)-250
)
x.place(
    x=round(root.winfo_screenwidth()/8)
    ,y=round(root.winfo_screenheight()/2)-200
)

y = tk.Label(root, text="Ending Time:",font=("Arial",24))
z = tk.Label(root, text="Not Started",font=("Arial",72))
y.place(
    x=round(root.winfo_screenwidth()/8)
    ,y=round(root.winfo_screenheight()/2)
)
z.place(
    x=round(root.winfo_screenwidth()/8)
    ,y=round(root.winfo_screenheight()/2)+50
)

b = tk.Label(root, text="Time Remaining:",font=("Arial",32))
b.place(
    x=round(root.winfo_screenwidth()*(5/8))-100
    ,y=round(root.winfo_screenheight()/2)-75
)

a = tk.Label(root, text="Not Started",font=("Arial",96))
a.place(
    x=round(root.winfo_screenwidth()*(5/8))-100
    ,y=round(root.winfo_screenheight()/2)-25
)


pressed_f4 = False  # Is Alt-F4 pressed?

def do_exit():
    global pressed_f4
    print('Trying to close application')
    if pressed_f4:  # Deny if Alt-F4 is pressed
        print('Denied!')
        pressed_f4 = False  # Reset variable
    else:
        close()     # Exit application

def alt_f4(event):  # Alt-F4 is pressed
    global pressed_f4
    print('Alt-F4 pressed')
    pressed_f4 = True

def alt_tab(event):
    print("Alt-Tab pressed")

def close(*event):  # Exit application
    root.destroy()

root.bind('<Alt-F4>', alt_f4)
root.bind('<Alt-Tab>', alt_tab)
root.bind('<Escape>', close)
root.protocol("WM_DELETE_WINDOW",do_exit)
root.overrideredirect(True)

import pynput

# Disable mouse and keyboard events
mouse_listener = pynput.mouse.Listener(suppress=True)
mouse_listener.start()
keyboard_listener = pynput.keyboard.Listener(suppress=True)
keyboard_listener.start()
block=None
threading.Thread(target=myFunc,args=[root,w,x,y,z,a,block,mouse_listener,keyboard_listener]).start()

root.mainloop()
sys.exit(0)