import network
from inputs import *
import time
from OLED import *
import socket
from icons import add_icon, NO_WIFI, SHIFT, WIFI

ap = network.WLAN(network.AP_IF)
wlan = network.WLAN(network.STA_IF)

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
        add_icon(oled, WIFI, 107, 0)
      
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
    
def prepare_socket():
    ap = network.WLAN(network.AP_IF)
    wlan = network.WLAN(network.STA_IF)

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('0.0.0.0', 5005))
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.setblocking(False)