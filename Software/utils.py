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
    whatsapp_select = 1, 4
    games_select = 2, 4
    while True:
        clear_main()
        oled.rect(0, 0, 128, 10, 0, fill=True)
        add_icon(oled, NUMERICAL, 95, 0)
        indicate_wifi()
        oled.blit(calc_icon, 0, 10+y)
        oled.blit(notepad_icon, 63, 10+y)
        oled.blit(sms_icon, 0, 38+y)
        oled.blit(wifi_icon, 63, 38+y)
        oled.blit(whatsapp_icon, 0, 66+y)
        oled.blit(games_icon, 63, 66+y)
        oled.show()
        
        X, Y = listen()
        
        if X == calc_select[0] and Y == calc_select[1]:
            clear_main()
            return 'calc mode'
        elif X == notepad_select[0] and Y == notepad_select[1]:
            clear_main()
            return 'notepad mode'
        elif X == sms_select[0] and Y == sms_select[1]:
            clear_main()
            return 'sms mode'
        elif X == wifi_select[0] and Y == wifi_select[1]:
            wifi()
        elif X == whatsapp_select[0] and Y == whatsapp_select[1]:
            return 'whatsapp'
        elif X == games_select[0] and Y == games_select[1]:
            return 'games'
        
        elif X == 4 and Y == 1:
            clear_main()
            y += 15
            
        elif X == 5 and Y == 1:
            clear_main()
            y -= 15
