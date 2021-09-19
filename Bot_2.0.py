from pyautogui import *
import pyautogui
import keyboard
import time
import random
import win32api,win32con

tolr = 15
tolg = 10

click_timelength = 7
scan_timelength = 120
scan_amount = 3

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
        return [240,90,90] 
    elif ans == 'Y' or ans == 'y':
        print("press 'y' to choose the color for the detection pixel")
        waitforkeypress('y')
        xpos,ypos = win32api.GetCursorPos()
        return pyautogui.pixel(xpos,ypos)

print('SETUP_SCREENSHOT_AREA')

print("press 'y' to choose the top left pixel for the detection box")
waitforkeypress('y')
x1,y1 = win32api.GetCursorPos()
P1=[x1,y1]
print('pixel got!')
time.sleep(1)

print("press 'y' to choose the bottom right pixel for the detection box")
waitforkeypress('y')
x2,y2 = win32api.GetCursorPos()
P2=[x2,y2]
print('pixel got!')

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
    
print('SETUP_PIXEL')

print('would you like to manually pick the detection color? Y/N')
ans1 = input()
wanted_color = pixelpick(ans1)

print('SETUP_AUTOWALK')
print('what direction would you like to autowalk? W/A/S/D/N')
ans2 = input()
walkoffset = 0.1

print('MAIN_LOOP')

print('press h to start the macro, if you would like to stop press k')
waitforkeypress('h')
print('loop started')

while 1:
    pixelfound = False
    for n1 in range(0,scan_amount):
        for n2 in range(0,scan_timelength*2):
            pic = pyautogui.screenshot(region=(P1[0],P1[1],wid,hei))
            for x in range(0,wid,5):
                for y in range(0,hei,5):
                    if keyboard.is_pressed('k')==True:
                        exit()
                
                    r,g,b = pic.getpixel((x,y))
                    if (r in range(wanted_color[0]-tolr,wanted_color[0]+tolr)):
                        if (g in range(wanted_color[1]-tolg,wanted_color[1]+tolg)):
                            pixelfound = True
                            wanted_color = pyautogui.pixel(x+P1[0],y+P1[1])
                            win32api.SetCursorPos((x+P1[0],y+P1[1]))
                            print('pixel has been found!')
                            break
                
                if pixelfound == True:
                    break
                
            if pixelfound == True:
                break
            time.sleep(0.5)
            
        if pixelfound == True:
            break
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
    pyautogui.keydown(ans2)
    time.sleep(walkoffset)
    pyautogui.keyup(ans2)
    print('loop restarting')
