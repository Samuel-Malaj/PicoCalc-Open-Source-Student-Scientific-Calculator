import gc
print('RAM:',gc.mem_free())
from machine import Pin
import utime as time
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

##############################################################################
#print('Switching off')
#power_off()

''' Main '''
def main():
    while True:
        print('RAM:',gc.mem_free())
        mode = main_menu()
        indicate_wifi()
        clear_mode_line()
        clear_main()
        print('RAM:',gc.mem_free())
        
        if mode == 'calc mode':
            append_output('Calc Mode', 0, 0)
            calculator(expression)
            
        if mode == 'notepad mode':
            append_output('Notepad', 0, 0)
            note_pad(expression)
            
        if mode == 'WiFi':
            wifi()
            
        if mode == 'sms mode':
            append_output('SMS Mode', 0, 0)
            if ap.active() or wlan.isconnected():
                asyncio.run(messaging())
            else:
                append_output('Unavailable', 0, 10)
                append_output('No Wi-Fi', 0, 20)
                time.sleep(1.5)
                
        if mode == 'whatsapp':
            append_output('Whatsapp', 0, 0)
            if wlan.isconnected():
                send_whatsapp()
            else:
                append_output('Unavailable', 0, 10)
                append_output('No WiFi', 0, 20)
                time.sleep(1.5)
                
        if mode == 'games':
            game_select()
            
        if mode == 'weather':
            print('RAM:',gc.mem_free())
            wtth()
                
main()
