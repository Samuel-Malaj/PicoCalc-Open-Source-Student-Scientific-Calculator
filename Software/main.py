from machine import Pin
import time
from Calculate import calculate
import network
import uasyncio as asyncio
import socket
import lowpower
import errno

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
print('Switching off')
power_off()
LED = Pin('LED', Pin.OUT)
LED.value(1)

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

FUNCTIONS = ['POWER', 'ANS', 'DEL', 'AC', 'MODE', 'EXE', 'SHIFT', 'WiFi']

calculator_array = [['POWER', 'SHIFT', 'WiFi', '#', '#', '#'],
                  ['#', '/', '#', '^', '^', '#'],
                  ['ANS', 'sin(', 'cos(', 'tan(', '(', ')'],
                  ['7', '8', '9', 'DEL', 'AC'],
                  ['4', '5', '6', 'x', '/'],
                  ['1', '2', '3', '+', '-'],
                  ['0', '.', '#', 'MODE', 'EXE']]

character_array = [['POWER', 'SHIFT', 'WiFi', '#', '#', '#'],
                   ['A', 'B', 'C', 'D', 'E', 'F'],
                   ['G', 'H', 'I', 'J', 'K', 'L'],
                   ['M', 'N', 'O', 'DEL', 'AC'],
                   ['P', 'Q', 'R', 'S', 'T'],
                   ['U', 'V', 'W', 'X', 'Y'],
                   ['Z', ' ', '#', 'MODE', 'EXE']]

shift_character_array = [['POWER', 'SHIFT', 'WiFi', '#', '#', '#'],
                   ['#', '#', '#', '#', '#', '#'],
                   ['#', '#', '#', '#', '(', ')'],
                   ['7', '8', '9', 'DEL', 'AC'],
                   ['4', '5', '6', '<', '>'],
                   ['1', '2', '3', 'X', 'Y'],
                   ['0', '.', '#', 'MODE', 'EXE']]

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
        
def get_expression(array, shift_array, ANS):
    expression = []
    shift = False
    while True:
        x, y = listen()
        if shift:
            button = shift_array[y][x]
            shift = False
        else:
            button = array[y][x]
            
        if button in FUNCTIONS:
            if button == 'DEL' and len(expression) > 0:
                expression.pop()
            if button == 'AC':
                expression = []
            if button == 'MODE':
                return 'MODE', expression
            if button == 'EXE':
                return 'EXE', expression
            if button == 'SHIFT':
                shift = True
            if button == 'ANS':
                expression.append(ANS)
            if button == 'POWER':
                print('Power Off')
                machine.reset()
            if button == 'WiFi':
                wifi()
        else:
            expression.append(button)
        print(expression)

def calculator(expression):
    ANS = 0
    while True:
        function, expression = get_expression(calculator_array, character_array, ANS)
        if function == 'EXE':
            answer = calculate(expression)
            if 'Error' not in answer:
                ANS = answer         
            print(answer)
        
        if function == 'MODE':
            return ''
        
def characters(expression):
    while True:
        function, expression = get_expression(character_array, shift_character_array, 0)
        if function == 'EXE':
            pass
        if function == 'MODE':
            return ''
        
def wifi():
    networks = scan()
    counter = 0
    function, expression = get_expression(character_array, shift_character_array, 0)
                    
    if function == 'MODE':
        return ''
                
    if function == 'EXE':
        if counter == 0: # if user hasn't been asked to select network yet
            try:
                num = int(''.join(expression))
                if num == 0:
                    print('SELECTED 0 CREATE NEW <--------')
                    ssid = 'Create New +'
                else:
                    ssid = networks[num-1][0].decode('utf-8')
                    print('Selected:', ssid)
                counter += 1
            except ValueError:
                print('You Must Enter an integer')
                
        if counter == 1 and ssid == 'Create New +':
            print('Create SSID: ')
            function, ssid = get_expression(character_array, shift_character_array, 0)
            print('Create password: ')
            function, password = get_expression(character_array, shift_character_array, 0)
            create_hotspot(''.join(ssid), ''.join(password))
        elif counter == 1:
            print('Enter Wi-Fi password: ')
            function, expression = get_expression(character_array, shift_character_array, 0)
            password = ''.join(expression)
            connect_wifi(ssid, password)
      
def scan():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    time.sleep(1) # Allow time for initialization
    print("Scanning...")
    networks = wlan.scan() # Scan for networks
    print('0: Create New +')
    for num, net in enumerate(networks):
        print(num+1, ':', net[0].decode('utf-8'), net[3]) # Prints (SSID, BSSID, channel, RSSI, security, hidden)
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
    print('Hotspot is active!')
    print('Connect to:', ssid)
    print('Pico W IP Address:', ap.ifconfig()[0])
    
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
        time.sleep(1)
    # 5. Check connection status
    if wlan.status() != 3:
        print(f"Connection failed. Status code: {wlan.status()}")
    else:
        print("Connected successfully!")
        status = wlan.ifconfig()
        print('IP address: ' + status[0])
    wlan.config(pm=0xa11140)
    

async def recv_task():
    while not stop_event.is_set():
        try:
            data, addr = s.recvfrom(1024)
            print(f"\nReceived: {data.decode()}")
        except OSError:
            pass # No data ready
        await asyncio.sleep(0.01)

async def send_task(broadcast_ip):
    while not stop_event.is_set():
        # Call your custom function
        # Expecting: function (str), expression (list/str)
        function, expression = get_expression(character_array, shift_character_array, 0)
        
        if function == 'MODE':
            print("Mode change detected. Stopping...")
            stop_event.set()
        elif expression:
            # Join list into string and send
            msg = "".join(expression)
            try:
                s.sendto(msg.encode(), (broadcast_ip, 5005))
                print(f"Sent: {msg}")
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
 
 
ap = network.WLAN(network.AP_IF)
wlan = network.WLAN(network.STA_IF)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('0.0.0.0', 5005))
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.setblocking(False)

while True:
    calculator(expression)
    characters(expression)
    stop_event = asyncio.Event()
    if ap.active() or wlan.active():
        asyncio.run(messaging())
