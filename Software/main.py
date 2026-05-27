from machine import Pin
import time
from Calculate import calculate
import network
import uasyncio as asyncio
import socket
import lowpower
import errno
from icons import *
import urequests
from inputs import *
from WiFi import *
from modes import *

LED = Pin('LED', Pin.OUT)
while True:
    try:
        from OLED import *
        break
    except Exception as e:
        print(e)
        LED.toggle()
        time.sleep(0.5)
        LED.toggle()
# --- 1. SETUP ---
# Safety: If GP1 is connected to GND, don't sleep!
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
    
##############################################################################
# print('Switching off')
# power_off()

#############################################################################
        
 
''' Main '''
def main():
    prepare_socket()
    while True:
        try:
            indicate_wifi()
            clear_mode_line()
            clear_main()
            append_output('Calc Mode', 0, 0)
            calculator(expression)
            
            indicate_wifi()
            clear_mode_line()
            clear_main()
            append_output('Typing Mode', 0, 0)
            characters(expression)
                
            ## messaging
            indicate_wifi()
            clear_main()
            clear_mode_line()
            append_output('SMS Mode', 0, 0)
            if ap.active() or wlan.active():
                asyncio.run(messaging())
            else:
                display_line('SMS unavailable', 0, 10)
                append_output('No Wi-Fi', 0, 20)
                time.sleep(1.5)
                
            indicate_wifi()
            clear_mode_line()
            clear_main()
            oled.rect(0, 0, 106, 10, 0, fill=True)
            oled.show()
            append_output('Whatsapp', 0, 0)
            send_whatsapp()
        
        except Exception as e:
            print(e)
            try:
                display_line('System Error', 0, 10)
            except:
                LED.toggle()
                time.sleep(1)
                LED.toggle()
                
main()

