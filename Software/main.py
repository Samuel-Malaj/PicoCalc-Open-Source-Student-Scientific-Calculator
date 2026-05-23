from machine import Pin
import time
from Calculate import calculate
import network
import uasyncio as asyncio
import socket
import lowpower
import errno
from icons import *

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
LED.value(1)
clear_all()

R1 = Pin(0, Pin.OUT)
R2 = Pin(1, Pin.OUT)
R3 = Pin(2, Pin.OUT)
R4 = Pin(3, Pin.OUT)
R5 = Pin(4, Pin.OUT)
R6 = Pin(5, Pin.OUT)
R7 = Pin(6, Pin.OUT)

C1 = Pin(7, Pin.IN, Pin.PULL_DOWN)
C2 = Pin(8, Pin.IN, Pin.PULL_DOWN)
C3 = Pin(9, Pin.IN, Pin.PULL_DOWN)
C4 = Pin(10, Pin.IN, Pin.PULL_DOWN)
C5 = Pin(11, Pin.IN, Pin.PULL_DOWN)
C6 = Pin(12, Pin.IN, Pin.PULL_DOWN)

rows = [R1, R2, R3, R4, R5, R6, R7]
columns = [C1, C2, C3, C4, C5, C6]

FUNCTIONS = ['POWER', 'ANS', 'DEL', 'AC', 'MODE', 'EXE', 'SHIFT', 'WiFi', 'LEFT', 'RIGHT']

calculator_array = [['POWER', 'SHIFT', 'WiFi', 'WiFi', 'LEFT', 'RIGHT'],
                  ['#', '/', '#', '^', '^', '#'],
                  ['ANS', 'sin(', 'cos(', 'tan(', '(', ')'],
                  ['7', '8', '9', 'DEL', 'AC'],
                  ['4', '5', '6', 'x', '/'],
                  ['1', '2', '3', '+', '-'],
                  ['0', '.', '0 ', 'MODE', 'EXE']]

character_array = [['POWER', 'SHIFT', 'WiFi', 'WiFi', 'LEFT', 'RIGHT'],
                   ['A', 'B', 'C', 'D', 'E', 'F'],
                   ['G', 'H', 'I', 'J', 'K', 'L'],
                   ['M', 'N', 'O', 'DEL', 'AC'],
                   ['P', 'Q', 'R', 'S', 'T'],
                   ['U', 'V', 'W', 'X', 'Y'],
                   ['Z', ' ', '#', 'MODE', 'EXE']]

shift_character_array = [['POWER', 'SHIFT', 'WiFi', 'WiFi', 'LEFT', 'RIGHT'],
                   ['#', '#', '#', '#', '#', '#'],
                   ['#', '#', '#', '#', '(', ')'],
                   ['7', '8', '9', 'DEL', 'AC'],
                   ['4', '5', '6', '<', '>'],
                   ['1', '2', '3', 'X', 'Y'],
                   ['0', '.', '0', 'MODE', 'EXE']]

expression = []
ANS = 0
##############################################################################
def listen():
    while True:
        for row_num, row in enumerate(rows):
            row.value(1)
            for col_num, col in enumerate(columns):
                if col.value() == 1:
                    row.value(0)   # turn off before returning
                    LED.value(0)
                    time.sleep_ms(200)  # debounce
                    LED.value(1)
                    return col_num, row_num
            row.value(0)
        time.sleep_ms(10)
          
def get_expression(array, shift_array, ANS, line):
    expression = []
    shift = False
    X = 0
    while True:
        if shift:
            add_icon(oled, SHIFT, 118, 0)
        else:
            oled.rect(118, 0, 10, 10, 0, fill=True)
            oled.show()
        x, y = listen()
        if shift:
            button = shift_array[y][x]
            shift = False
        else:
            button = array[y][x]
            if button == 'SHIFT':
                shift = True
            
        if button in FUNCTIONS:
            if button == 'DEL' and len(expression) > 0:
                expression.pop()
            if button == 'AC':
                expression = []
                clear_main()
                X = 0
            if button == 'MODE':
                return 'MODE', expression
            if button == 'EXE':
                return 'EXE', expression
            if button == 'ANS':
                expression.append(ANS)
            if button == 'POWER':
                print('Power Off')
                display_line('Power Off', 0, 0)
                time.sleep(2)
                machine.reset()
            if button == 'WiFi':
                wifi()
            if button == 'LEFT':
                X += 10
            if button == 'RIGHT':
                print('RIGHT')
                X -= 10
        else:
            expression.append(button)
        print(expression)

        oled.rect(0, line, 118, 8, 0, fill=True)
        oled.show()
        append_output(''.join(expression), X, line)

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
        
        if function == 'MODE':
            return ''
        
def characters(expression):
    while True:
        function, expression = get_expression(character_array, shift_character_array, 0, line=10)
        if function == 'EXE':
            pass
        if function == 'MODE':
            return ''
        
def wifi():
    oled.rect(0, 0, 106, 10, 0, fill=True)
    oled.show()
    networks = scan()
    counter = 0
    function, expression = get_expression(character_array, shift_character_array, 0, line=10)
                    
    if function == 'MODE':
        return ''             
    if function == 'EXE':
        if counter == 0: # if user hasn't been asked to select network yet
            try:
                num = int(''.join(expression))
                if num == 0:
                    print('SELECTED 0 CREATE NEW')
                    display_line('SELECTED 0 CREATE NEW', 0, 10)
                    ssid = 'Create New +'
                else:
                    ssid = networks[num-1][0].decode('utf-8')
                    print('Selected:', ssid)
                    clear_main()
                    append_output('Selected:', 0, 10)
                    append_output(ssid, 0, 20)
                    
                counter += 1
            except ValueError:
                print('You Must Enter an integer')
                
        if counter == 1 and ssid == 'Create New +':
            print('Create SSID: ')
            display_line('Create SSID: ', 0, 10)
            function, ssid = get_expression(character_array, shift_character_array, 0, line=20)
            print('Create password: ')
            display_line('Create Password: ', 0, 10)
            function, password = get_expression(character_array, shift_character_array, 0, line=20)
            create_hotspot(''.join(ssid), ''.join(password))
        elif counter == 1:
            print('Enter Wi-Fi password: ')
            display_line('Enter Wi-Fi password: ', 0, 10)
            function, expression = get_expression(character_array, shift_character_array, 0, line=20)
            password = ''.join(expression)
            connect_wifi(ssid, password)
    
    if wlan.isconnected() or ap.isconnected():
        add_icon(oled, WIFI, 0, 0)
      
def scan():
    clear_main()
    global wlan
    wlan.active(True)
    time.sleep(1)
    print("Scanning WiFi...")
    append_output('Scanning WiFi...', 0, 10)
    networks = wlan.scan() # Scan for networks
    print('0:Create New +')
    append_output('0:Create New +', 0, 20)
    for num, net in enumerate(networks):
        network = ''.join([str(num+1), ':', net[0].decode('utf-8'), str(net[3])]) # Prints (SSID, BSSID, channel, RSSI, security, hidden)
        print(network)
        append_output(network, 0, num * 10 + 30)
        
    print('Select Wi-Fi Network: ')
    wlan.deinit()
    return networks

def create_hotspot(ssid, password):
    network.WLAN(network.STA_IF).active(False)
    ap = network.WLAN(network.AP_IF)
    ap.config(essid=ssid, password=password)
    ap.active(True)
    while not ap.active():
        pass
    print('Hotspot active!')
    display_input('Hotspot active!')
    time.sleep(2)
    clear_main()
    print('Connect to:', ssid)
    print('Pico W IP Address:', ap.ifconfig()[0])
    
    if ap.active() or wlan.isconnected():
        add_icon(oled, WIFI, 107, 0)
        print('connected')
    
def connect_wifi(ssid, password):
    network.WLAN(network.AP_IF).active(False)
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    # 4. Wait for connection (with timeout)
    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('Waiting for connection...')
        display_line('Waiting for connection...', 0, 10)
        time.sleep(1)
    # 5. Check connection status
    if wlan.status() != 3:
        print(f"Connection failed. Status code: {wlan.status()}")
    else:
        print("Connected successfully!")
        display_line("Connected successfully!", 0, 10)
        status = wlan.ifconfig()
        print('IP address: ' + status[0])
    wlan.config(pm=0xa11140)
    
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
 
''' Main '''
ap = network.WLAN(network.AP_IF)
wlan = network.WLAN(network.STA_IF)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('0.0.0.0', 5005))
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.setblocking(False)

while True:
    try:
        oled.rect(0, 0, 106, 10, 0, fill=True)
        oled.show()
        append_output('Calc Mode', 0, 0)
        calculator(expression)
        
        oled.rect(0, 0, 106, 10, 0, fill=True)
        oled.show()
        append_output('Typing Mode', 0, 0)
        clear_main()
        characters(expression)
        
        ## messaging
        oled.rect(0, 0, 106, 10, 0, fill=True)
        oled.show()
        append_output('SMS Mode', 0, 0)
        clear_main()
        stop_event = asyncio.Event()
        if ap.active() or wlan.active():
            asyncio.run(messaging())
        else:
            display_line('SMS unavailable', 0, 10)
            append_output('No Wi-Fi', 0, 20)
            time.sleep(1.5)
    
    except Exception as e:
        print(e)
        try:
            display_line('System Error', 0, 10)
        except:
            LED.toggle()
            time.sleep(1)
            LED.toggle()



