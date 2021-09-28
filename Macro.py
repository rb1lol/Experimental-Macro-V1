"""
Python Macro (PyM), Created and Developed by Rb1

if need any help, or have any questions you can contact me in this discord: https://discord.gg/RBxF3gZtBN

HOW TO SET UP MACRO

firstly, download the latest version python onto your computer.

secondly, go to command prompt and input the following commands:

py -m pip install pywin32
py -m pip install pillow
py -m pip install pyautogui
py -m pip install keyboard
py -m pip install opencv-python
py -m pip install pydirectinput

thirdly, copy and paste the code below into a python file, then configure as needed.
"""
    
# import the modules
from pyautogui import *
import pyautogui
from pydirectinput import keyDown, keyUp
import keyboard
import time
import random
import win32api,win32con

# tweakable values

# SCAN VALUES

tolr = 15 # tolerance for finding the red color value
tolgb = 10 # tolerance for finding the other color values

scan_timelength = 69 # how long each scan loop takes in seconds
scan_amount = 3 # how many scan loops there are (clicks at the end of each loop to reset fishing pole)

step = 5 # how large the pixel step is between pixels. lower for better accuracy, increase for more effeciency
CPS = 2 # checks per second (CPS) is how many times in a second the loop will scan for a pixel

# CLICK VALUES

click_timelength = 7 # approx. how long your character will click
afterclick = False # clicks after the spamclick, useful in certain enviornments.

# functions
def click():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

def waitforkeypress(key):
    while keyboard.is_pressed(key)==False:
        time.sleep(0.01)

def pixelpick(ans):
    if ans == 'N' or ans == 'n':
        return [240,93,93] 
    elif ans == 'Y' or ans == 'y':
        print("press 'y' to choose the color for the detection pixel")
        waitforkeypress('y')
        xpos,ypos = win32api.GetCursorPos()
        return pyautogui.pixel(xpos,ypos-2)
    else:
        print('unknown command, please say either Y or N')
        exit()

def autowalk(ans):
    AWTimer = 0.035 # how long your chara will auto walk in seconds, tweakable
    if ans !='n':
        keyDown(ans)
        time.sleep(AWTimer)
        keyUp(ans)

print('SETUP_SCREENSHOT_AREA')

# first pixel in the detection box / top left pixel
print("press 'y' to choose the first point for the detection box")
waitforkeypress('y')
x1,y1 = win32api.GetCursorPos()
P1=[x1,y1]
print('pixel got!')
time.sleep(1)

# last pixel in the detection box / bottom right pixel
print("press 'y' to choose the second point for the detection box")
waitforkeypress('y')
x2,y2 = win32api.GetCursorPos()
P2=[x2,y2]
print('pixel got!')

# box dimensions math
for i in range(0,2):
    if P1[i] > P2[i]:
        holdval = P1[i]
        P1[i] = P2[i]
        P2[i] = holdval

wid = P2[0]-P1[0]
hei = P2[1]-P1[1]
if wid <= 0:
    print('Width is below 0!')
    exit()
elif hei <= 0:
    print('Height is below 0!')
    exit()
else:
    print('AREA_MATH: StartX: '+str(P1[0])+', StartY: '+str(P1[1])+', Width: '+str(wid)+', Height: '+str(hei))

print('SETUP_DETECTION_COLOR')

# get the detection color (auto-assigns if user inputs N)
print('prereq: make sure to turn on picture mode (press p)')
print('would you like to manually pick the detection color? Y/N')
ans = input()
wanted_color = pixelpick(ans)

print('SETUP_AUTOWALK')

# ask what key to press automatically after catching or loop
print('prereq: make sure to turn off running for your character')
print('in what direction would you like to walk? (W/A/S/D, N to cancel feature)')
ansAW = str(input()).lower()

print('MAIN_LOOP')

# waits for the user to get set up
print('press h to start the macro, if you would like to stop press k')
waitforkeypress('h')
print('loop started')

# main loop (not going to explain it all, look into it yourself)
while 1:
    pixelfound = False
    for n1 in range(0,scan_amount):
        for n2 in range(0,scan_timelength*CPS):
            pic = pyautogui.screenshot(region=(P1[0],P1[1],wid,hei))
            for x in range(0,wid,step):
                for y in range(0,hei,step):
                    if keyboard.is_pressed('k')==True:
                        exit()
                    
                    # get the color of the pixel (x,y) from the screenshot
                    r,g,b = pic.getpixel((x,y))
                    
                    # checks if the color alligns with the wanted color
                    if (r in range(wanted_color[0]-tolr,wanted_color[0]+tolr)):
                        if (g in range(wanted_color[1]-tolgb,wanted_color[1]+tolgb)):
                            if (b in range(wanted_color[2]-tolgb,wanted_color[2]+tolgb)):
                                pixelfound = True
                                print(wanted_color,pyautogui.pixel(x+P1[0],y+P1[1]))
                                wanted_color = pyautogui.pixel(x+P1[0],y+P1[1])
                                win32api.SetCursorPos((x+P1[0],y+P1[1]))
                                print('pixel has been found!')
                                break
                
                if pixelfound == True:
                    break
                
            if pixelfound == True:
                if n2 <= 5:
                    print('pixel detected too fast! terminating script')
                break
            print('scan loop #'+str(n2)) # prints after every scan loop
            time.sleep(1/CPS)
            
        if pixelfound == True:
            break
        print('failed to detect pixel, looping')
        autowalk(ansAW)
        click()
        
    if pixelfound == True:
        for i in range(click_timelength*100):
            if keyboard.is_pressed('k')==True:
                exit()
            click()
        pixelfound = False
    else:
        print('pixel wasnt found. terminating script')
        exit()
    
    time.sleep(1)
    autowalk(ansAW)
    if afterclick == True:
        click()
    print('click spam ended, restarting loops')
