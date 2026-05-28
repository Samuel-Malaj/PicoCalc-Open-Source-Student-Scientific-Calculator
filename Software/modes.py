import uasyncio as asyncio
from Calculate import calculate
from inputs import *
import time
from OLED import *
from WiFi import *
import urequests
import socket

''' Calculator '''
def calculator(expression):
    ANS = '0'
    clear_main()
    while True:
        function, expression = get_expression(calculator_array, character_array, ANS, line=10)
        if function == 'EXE':
            answer = calculate(expression)
            if 'Error' not in answer:
                ANS = answer         
            print(answer)
            clear_main()
            append_output(answer, 0, 54)
        if function == 'WiFi':
            wifi()
        if function == 'MODE':
            return ''

''' Characters '''        
def note_pad(expression):
    while True:
        open('notes.txt', 'a').close()
        with open('notes.txt', 'r') as file:
            note = file.readlines()
        
        clear_main()
        append_output('Note:' + ''.join(note), 0, 10)
        function, expression = get_expression(character_array, shift_character_array, 0, line=20)
        
        if function == 'EXE':
            with open('notes.txt', 'w') as file:
                file.write(''.join(expression))
                file.close()
            clear_main()
            append_output('Saved Note', 0, 10)
    
        if function == 'WiFi':
            wifi()
        if function == 'MODE':
            return ''

''' SMS '''
stop_event = asyncio.Event()
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('0.0.0.0', 5005))
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.setblocking(False)
async def recv_task():
    while not stop_event.is_set():
        try:
            data, addr = s.recvfrom(1024)
            string = str(data.decode())
            clear_main()
            append_output('Received:', 0, 44)
            append_output(string, 0, 54)
        except OSError:
            pass # No data ready
        await asyncio.sleep(0.01)

async def send_task(broadcast_ip):
    while not stop_event.is_set():
        oled.rect(0, 10, 128, 20, 0, fill=True)
        oled.show()
        function, expression = get_expression(character_array, shift_character_array, 0, line=20)
        if function == 'MODE':
            print("Mode change detected. Stopping...")
            stop_event.set()
        elif expression:
            # Join list into string and send
            msg = "".join(expression)
            try:
                s.sendto(msg.encode(), (broadcast_ip, 5005))
                print(f"Sent: {msg}")
                append_output('Sent:', 0, 10)
                append_output(msg, 0, 20)
                time.sleep(1)
                clear_main()
                
            except OSError as e:
                print(e)
            
        await asyncio.sleep(0.1)

async def messaging():
    if ap.active():
        ip_info = ap.ifconfig()
    if wlan.active():
        ip_info = wlan.ifconfig()
    broadcast_ip = ".".join(ip_info[0].split('.')[:-1]) + ".255"
    print('Messaging Mode')
    print('Notice: If not connected to a wifi network, messaging will fail')
    await asyncio.gather(recv_task(), send_task(broadcast_ip))
    
''' Whatsapp ''' 
def send_whatsapp():
    while True:
        function, expression = get_expression(character_array, shift_character_array, 0, line=20)
        if function == 'MODE':
            break
        msg = '+'.join(''.join(expression).split(' '))
        print('Sending:', msg)
        append_output('Sending:', 0, 10)
        append_output(msg, 0, 20)
        api_key = 'API_KEY'
        phone_number = 'PHONE_NUMBER'
        url = f"https://api.callmebot.com/whatsapp.php?phone={phone_number}&text={msg}&apikey={api_key}"
        print(url)
        response = urequests.get(url)
        print(response.text)
        response.close()
        clear_main()

