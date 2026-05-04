from machine import Pin
import time
from Calculate import calculate
import network

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

FUNCTIONS = ['POWER', 'ANS', 'DEL', 'AC', 'MODE', 'EXE', 'SHIFT']

calculator_array = [['POWER', '#', '#', '#', '#', '#'],
                  ['#', '/', '#', '^', '^', '#'],
                  ['ANS', 'sin(', 'cos(', 'tan(', '(', ')'],
                  ['7', '8', '9', 'DEL', 'AC'],
                  ['4', '5', '6', 'x', '/'],
                  ['1', '2', '3', '+', '-'],
                  ['0', '.', '#', 'MODE', 'EXE']]

character_array = [['POWER', 'SHIFT', '#', '#', '#', '#'],
                   ['A', 'B', 'C', 'D', 'E', 'F'],
                   ['G', 'H', 'I', 'J', 'K', 'L'],
                   ['M', 'N', 'O', 'DEL', 'AC'],
                   ['P', 'Q', 'R', 'S', 'T'],
                   ['U', 'V', 'W', 'X', 'Y'],
                   ['Z', ' ', '#', '#', 'EXE']]

shift_character_array = [['POWER', '#', '#', '#', '#', '#'],
                   ['#', '#', '#', '#', '#', '#'],
                   ['#', '#', '#', '#', '(', ')'],
                   ['7', '8', '9', 'DEL', 'AC'],
                   ['4', '5', '6', '<', '>'],
                   ['1', '2', '3', 'X', 'Y'],
                   ['0', '.', '#', '#', 'EXE']]

expression = []
ANS = 0

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

def calculator(expression):
    ANS = 0
    while True:
        x, y = listen()
        button = calculator_array[y][x]
        
        if button in FUNCTIONS:
            if button == 'EXE':
                ANS = calculate(expression)
                expression = [ANS]
                print(ANS)          
            if button == 'ANS':
                if ANS:
                    expression.append(ANS)          
            if button == 'AC':
                expression = []              
            if button == 'DEL':
                if len(expression) >= 1:
                    expression.pop()                  
            if button == 'MODE':
                return ''
        
        else:
            expression.append(button)
        
        print(expression)
        
def characters(expression):
    shift = False
    while True:
        x, y = listen()
        if shift:
            button = shift_character_array[y][x]
            shift = False
        else:
            button = character_array[y][x]
        
        if button in FUNCTIONS:
            if button == 'SHIFT':
                shift = True
            if button == 'DEL':
                if len(expression) > 0: 
                    expression.pop()
            
            if button == 'AC':
                expression = []
                             
            if button == 'MODE':
                return ''
        
        else:
            expression.append(button)
        
        print(expression)
        
def wifi():
    shift = False
    expression = []
    scan()
    while True:
        x, y = listen()
        if shift:
            button = shift_character_array[y][x]
            shift = False
        else:
            button = character_array[y][x]
        
        if button in FUNCTIONS:
            if button == 'DEL':
                if len(expression) > 0:
                    expression.pop()
                    
            if button == 'MODE':
                return ''
                
            if button == 'EXE':
                try:
                    num = int(''.join(expression))
                    ssid = networks[num-1][0].decode('utf-8')
                    print('Selected:', ssid)
                    print('Enter Password: ')
                    expression = []
                    
                except:
                    try:
                        password = ''.join(expression)
                        print(ssid, password)
                        connect_wifi(ssid, password)
                        
                    except Exception as e:
                        print('ERROR: ', e)
                        
        else:
            expression.append(button)
        print(expression)
        
def scan():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    time.sleep(1) # Allow time for initialization

    print("Scanning...")
    networks = wlan.scan() # Scan for networks
    for num, net in enumerate(networks):
        print(num+1, ':', net[0].decode('utf-8'), net[3]) # Prints (SSID, BSSID, channel, RSSI, security, hidden)
    
    print('Select Wi-Fi Network: ')
    
def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
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
     
     
while True:
    calculator(expression)
    characters(expression)
    wifi()
