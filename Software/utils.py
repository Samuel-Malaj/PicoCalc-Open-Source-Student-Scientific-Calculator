import lowpower
import time
import machine
from machine import Pin
from icons import *
from inputs import *
from WiFi import *
from OLED import *

def power_off():
    safety_pin = machine.Pin(1, machine.Pin.IN, machine.Pin.PULL_UP)
    if safety_pin.value() == 0:
        print("Safety mode: Sleep disabled. Connect GP1 to 3V3 to allow sleep.")
        while True: time.sleep(1)

    button = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_UP)
    indicator = machine.Pin(7, machine.Pin.OUT, value=0)

    LED = Pin('LED', Pin.OUT)
    LED.value(1)
    LED.value(0)
    lowpower.dormant_until_pin(0)
    
def main_menu():
    y = 0
    clear_all()
    calc_select = 0, 5
    notepad_select = 1, 5
    sms_select = 2, 5
    sms_select = 3, 5
    wifi_select = 0, 4
    while True:
        clear_main()
        add_large_icon(oled, calc_mode, 0, 10+y)
        add_large_icon(oled, notepad_mode, 63, 10+y)
        add_large_icon(oled, sms_mode, 0, 38+y)
        add_large_icon(oled, wifi_mode, 63, 38+y)
        oled.rect(0, 0, 128, 10, 0, fill=True)
        oled.show()
        add_icon(oled, NUMERICAL, 95, 0)
        indicate_wifi()
        
        X, Y = listen()
        
        if X == calc_select[0] and Y == calc_select[1]:
            clear_main()
            return 'calc mode'
        if X == notepad_select[0] and Y == notepad_select[1]:
            clear_main()
            return 'notepad mode'
        if X == sms_select[0] and Y == sms_select[1]:
            clear_main()
            return 'sms mode'
        if X == wifi_select[0] and Y == wifi_select[1]:
            wifi()
        
        if X == 0 and Y == 0:
            clear_main()
            y += 10
            
        if X == 0 and Y == 1:
            clear_main()
            y -= 10
