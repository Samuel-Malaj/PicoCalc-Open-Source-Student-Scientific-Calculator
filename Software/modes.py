import uasyncio as asyncio
from Calculate import calculate
from inputs import *
import time
from OLED import *
from WiFi import *
import urequests

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
        
def characters(expression):
    while True:
        function, expression = get_expression(character_array, shift_character_array, 0, line=10)
        if function == 'EXE':
            pass
        if function == 'WiFi':
            wifi()
        if function == 'MODE':
            return ''

stop_event = asyncio.Event()

async def recv_task():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setblocking(False)
    s.bind(('', 5005))
    try:
        while not stop_event.is_set():
            try:
                data, addr = s.recvfrom(1024)
                string = data.decode()
                clear_main()
                append_output('Received:', 0, 44)
                append_output(string, 0, 54)
            except OSError:
                pass
            await asyncio.sleep(0.01)
    finally:
        s.close()

async def send_task(broadcast_ip):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setblocking(False)
    try:
        while not stop_event.is_set():
            oled.rect(0, 10, 128, 20, 0, fill=True)
            oled.show()
            function, expression = get_expression(character_array, shift_character_array, 0, line=20)
            if function == 'MODE':
                print("Mode change detected. Stopping...")
                stop_event.set()
            elif expression:
                msg = "".join(expression)
                try:
                    s.sendto(msg.encode(), (broadcast_ip, 5005))
                    print(f"Sent: {msg}")
                    append_output('Sent:', 0, 10)
                    append_output(msg, 0, 20)
                    await asyncio.sleep(1)  # not time.sleep
                    clear_main()
                except OSError as e:
                    print(e)
            await asyncio.sleep(0.1)
    finally:
        s.close()

async def messaging():
    stop_event.clear()  # reset for reuse
    if ap.active():
        ip_info = ap.ifconfig()
    if wlan.active():
        ip_info = wlan.ifconfig()
    broadcast_ip = ".".join(ip_info[0].split('.')[:-1]) + ".255"
    print('Messaging Mode')
    await asyncio.gather(recv_task(), send_task(broadcast_ip))
    
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
