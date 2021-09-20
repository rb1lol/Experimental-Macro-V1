 """
Configurable Image to Pixel Experimental Macro - Python Version 3.9 Macro Version 1.2- Rb1 (CIPExM-Py3.9MV1.2-RB1)

HOW TO SET UP MACRO

firstly, download the latest version python onto your computer.

secondly, go to command prompt and input the following commands:

py -m pip install pywin32
py -m pip install pillow
py -m pip install pyautogui
py -m pip install keyboard
py -m pip install opencv-python

thirdly, copy and paste the code below into a python file, then configure as needed.
"""
    
# import the modules
from pyautogui import *
import pyautogui
import keyboard
import time
import random
import win32api,win32con

# tweakable values
tolr = 15
tolgb = 10

click_timelength = 7
scan_timelength = 69
scan_amount = 3
walkoffset = 0.5
step = 5

# functions
def click():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

def waitforkeypress(key):
    while keyboard.is_pressed(key)==False:
        time.sleep(0.01)

def pixelpick(ans):
    print(ans)
    if ans == 'N' or ans == 'n':
        return [240,95,95] 
    elif ans == 'Y' or ans == 'y':
        print("press 'y' to choose the color for the detection pixel")
        waitforkeypress('y')
        xpos,ypos = win32api.GetCursorPos()
        return pyautogui.pixel(xpos,ypos-2)
    else:
        print('unknown command, please say either Y or N')
        exit()

print('SETUP_SCREENSHOT_AREA')

# first pixel in the detection box / top left pixel
print("press 'y' to choose the top left pixel for the detection box")
waitforkeypress('y')
x1,y1 = win32api.GetCursorPos()
P1=[x1,y1]
print('pixel got!')
time.sleep(1)

# last pixel in the detection box / bottom right pixel
print("press 'y' to choose the bottom right pixel for the detection box")
waitforkeypress('y')
x2,y2 = win32api.GetCursorPos()
P2=[x2,y2]
print('pixel got!')

# box dimensions math
wid = P2[0]-P1[0]
hei = P2[1]-P1[1]
if wid <= 0:
    print('Width is below 0, please make sure to put your points in the correct order!')
    exit()
elif hei <= 0:
    print('Height is below 0, please make sure to put your points in the correct order!')
    exit()
else:
    print('AREA: '+str(P1[0])+','+str(P1[1])+','+str(wid)+','+str(hei))

print('SETUP_DETECTION_COLOR')

# get the detection color (auto-assigns if user inputs N)
print('would you like to manually pick the detection color? Y/N')
ans = input()
wanted_color = pixelpick(ans)

print('MAIN_LOOP')

# waits for the user to get set up
print('press h to start the macro, if you would like to stop press k')
waitforkeypress('h')
print('loop started')

# main loop (not going to explain it all)
while 1:
    pixelfound = False
    for n1 in range(0,scan_amount):
        for n2 in range(0,scan_timelength*2):
            pic = pyautogui.screenshot(region=(P1[0],P1[1],wid,hei))
            for x in range(0,wid,step):
                for y in range(0,hei,step):
                    if keyboard.is_pressed('k')==True:
                        exit()
                
                    r,g,b = pic.getpixel((x,y))
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
                break
            print('check '+str(n2))
            time.sleep(0.5)
            
        if pixelfound == True:
            break
        print('restart')
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
    
    print('loop restarting')
