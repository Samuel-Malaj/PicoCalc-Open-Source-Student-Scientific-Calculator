from machine import Pin
import time
import network
import errno
from icons import *
from inputs import *
from WiFi import *
from modes import *
from utils import *

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

##############################################################################
#print('Switching off')
#power_off()

        
 
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
            append_output('Notepad', 0, 0)
            note_pad(expression)
                    
            ## messaging
            indicate_wifi()
            clear_main()
            clear_mode_line()
            append_output('SMS Mode', 0, 0)
            if ap.active() or wlan.isconnected():
                asyncio.run(messaging())
            else:
                append_output('Unavailable', 0, 10)
                append_output('No Wi-Fi', 0, 20)
                time.sleep(1.5)
            
            ## whatsapp
            indicate_wifi()
            clear_mode_line()
            clear_main()
            append_output('Whatsapp', 0, 0)
            if wlan.isconnected():
                send_whatsapp()
            else:
                append_output('Unavailable', 0, 10)
                append_output('No WiFi', 0, 20)
                time.sleep(1.5)
        
        except Exception as e:
            print(e)
            try:
                display_line('System Error', 0, 10)
            except:
                LED.toggle()
                time.sleep(1)
                LED.toggle()
                
main()

