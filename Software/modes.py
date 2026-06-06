import uasyncio as asyncio
from inputs import *
import utime as time
from OLED import *
import socket
from icons import *
import ujson
import gc
import sys

def unload(module_name):
    if module_name in sys.modules:
        del sys.modules[module_name]
    gc.collect()
    
def unload_var(variable):
    before = gc.mem_free()
    del variable
    gc.collect()
    after = gc.mem_free()
    print("Freed:", after - before, "bytes")
    
''' Calculator '''
def calculator(expression):
    from Calculate import calculate
    print('RAM:',gc.mem_free())
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
            unload('Calculate')
            print('RAM:',gc.mem_free())
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
    stop_event.clear()  # reset so it can be called again
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
        
def check_winner(positions):
    wins = [
    {1,2,3}, {4,5,6}, {7,8,9},  # rows
    {1,4,7}, {2,5,8}, {3,6,9},  # cols
    {1,5,9}, {3,5,7}             # diagonals
    ]
    return any(w.issubset(positions) for w in wins)
        
def Tic_Tac_Toe():
    clear_all()
    draw_icon(oled, tic_tac_toe_grid, 64, 0, 0)
    oled.rect(65, 0, 64, 64, 0, fill=True)
    oled.show()
    pos7 = 0, 0
    pos8 = 22, 0
    pos9 = 44, 0
    pos4 = 0, 22
    pos5 = 22, 22
    pos6 = 44, 22
    pos1 = 0, 44
    pos2 = 22, 44
    pos3 = 44, 44
    positions = [pos1, pos2, pos3, pos4, pos5, pos6, pos7, pos8, pos9]
    o_positions = []
    x_positions = []
    selected = ''
    winner = False
    
    while selected != 'MODE':
        # X's turn
        oled.rect(65, 0, 64, 64, 0, fill=True)
        oled.text("X's Turn", 65, 32)
        oled.show()
        selected = select_num()
        if selected == 'MODE':
            return ''
        selected = int(selected)
        while selected in x_positions or selected in o_positions or selected == 0:
            selected = select_num()
            if selected == 'MODE':
                return ''
            selected = int(selected)
        
        position = positions[selected-1]
        x_positions.append(selected)
        draw_icon(oled, x_icon, 21, position[0], position[1])
        oled.show()
        
        # check if winner or tie
        if check_winner(x_positions):
            oled.rect(65, 0, 64, 64, 0, fill=True)
            oled.text('X Wins!', 65, 32)
            oled.show()
            time.sleep(2)
            return ''
            
        if len(x_positions) + len(o_positions) == 9:
            oled.rect(65, 0, 64, 64, 0, fill=True)
            oled.text('Tie!', 65, 32)
            oled.show()
            time.sleep(2)
            return ''
            
        # O's turn
        oled.rect(65, 0, 64, 64, 0, fill=True)
        oled.text("O's Turn", 65, 32)
        oled.show()
        selected = select_num()
        if selected == 'MODE':
            return ''
        selected = int(selected)
        while selected in x_positions or selected in o_positions or selected == 0:
            selected = select_num()
            if selected == 'MODE':
                return ''
            selected = int(selected)
        
        position = positions[selected-1]
        o_positions.append(selected)
        draw_icon(oled, o_icon, 21, position[0], position[1])
        oled.show()
        
        # check if winner or tie
        if check_winner(o_positions):
            oled.rect(65, 0, 64, 64, 0, fill=True)
            oled.text('O Wins!', 65, 32)
            oled.show()
            time.sleep(2)
            return ''
            
        if len(x_positions) + len(o_positions) == 9:
            oled.rect(65, 0, 64, 64, 0, fill=True)
            oled.text('Tie!', 65, 32)
            oled.show()
            time.sleep(2)
            return ''      
            
games = ['Tic Tac Toe', 'Pong']
def game_select():
    clear_mode_line()
    clear_main()
    append_output('Games:', 0, 0)
    for num, game in enumerate(games):
        append_output(str(num+1)+':'+game, 0, 10+(num*10))
    
    selected = len(games)+1
    while int(selected) >= len(games) or not str(selected).isdigit():
        selected = select_num()
        if selected == 'MODE':
            return ''
        
    game = games[int(selected)-1]
    
    if game == 'Tic Tac Toe':
        Tic_Tac_Toe()
        game_select()
        

weather_icon_map = {
    113: sunny,
    116: partly_cloudy,
    119: cloudy, 122: cloudy, 248: cloudy, 260: cloudy,
    176: rainy, 182: rainy, 185: rainy, 200: rainy, 263: rainy, 266: rainy, 281: rainy, 284: rainy, 293: rainy, 296: rainy, 299: rainy, 302: rainy, 305: rainy, 308: rainy, 311: rainy, 314: rainy, 317: rainy, 320: rainy, 353: rainy, 356: rainy, 359: rainy, 362: rainy, 365: rainy, 374: rainy, 377: rainy, 386: rainy, 179:rainy
}

CONDITION_TO_CODE = {
    "sunny": 113,
    "clear": 113,
    "partly cloudy": 116,
    "cloudy": 119,
    "overcast": 122,
    "mist": 143,
    "fog": 248,
    "freezing fog": 260,
    "patchy rain possible": 176,
    "patchy light drizzle": 263,
    "light drizzle": 266,
    "freezing drizzle": 281,
    "heavy freezing drizzle": 284,
    "patchy light rain": 293,
    "light rain": 296,
    "moderate rain at times": 299,
    "moderate rain": 302,
    "heavy rain at times": 305,
    "heavy rain": 308,
    "light freezing rain": 311,
    "moderate or heavy freezing rain": 314,
    "light sleet": 317,
    "moderate or heavy sleet": 320,
    "patchy light snow": 323,
    "light snow": 326,
    "patchy moderate snow": 329,
    "moderate snow": 332,
    "patchy heavy snow": 335,
    "heavy snow": 338,
    "ice pellets": 350,
    "light rain shower": 353,
    "moderate or heavy rain shower": 356,
    "torrential rain shower": 359,
    "light sleet showers": 362,
    "moderate or heavy sleet showers": 365,
    "light snow showers": 368,
    "moderate or heavy snow showers": 371,
    "light showers of ice pellets": 374,
    "moderate or heavy showers of ice pellets": 377,
    "patchy light rain with thunder": 386,
    "moderate or heavy rain with thunder": 389,
    "patchy light snow with thunder": 392,
    "moderate or heavy snow with thunder": 395,
    "blowing snow": 227,
    "blizzard": 230,
    "thundery outbreaks possible": 200,
    "patchy snow possible": 179,
    "patchy sleet possible": 182,
    "patchy freezing drizzle possible": 185,
    "patchy rain nearby": 176,
    "patchy snow nearby": 179,
    "patchy sleet nearby": 182,
    "patchy freezing drizzle nearby": 185,
    "thundery outbreaks nearby": 200,
}

def auto_detect_location():
    import urequests, json
    response = urequests.get("http://ip-api.com/json/")
    data = response.json()
    response.close()
    unload_var(data)
    unload('json')
    return data['city']

def get_weather(location):
    import urequests
    
    print('RAM:',gc.mem_free())
    LOCATION = location
    URL = f"https://wttr.in/{LOCATION}?format=%t|%f|%M|%C"
    
    response = urequests.get(URL)
    data = response.text.replace('°','').lower().split('|')
    response.close()
    unload_var(response)

    print(data)
    condition = data[3].split(',')[0]
    temp = data[0]
    feels_like = data[1]
    moon = data[2]
    print(feels_like, temp, condition, moon)
    print(condition)

    conditions_icon = weather_icon_map[CONDITION_TO_CODE[condition]]
    draw_icon(oled, conditions_icon, 32, 0, 0)
    oled.text(location, 33, 0)
    oled.text('Temp:'+ temp + "'C", 33, 10)
    oled.text('like:'+ feels_like + "'C", 33, 20)
    oled.show()

def weather():
    import urequests
    clear_main()
    append_output('1:Enter Location', 0, 10)
    append_output('2:Autodetect', 0, 20)
    selected = select_num()
    if selected == 'MODE':
        unload('urequests')
        return ''
    while selected != '1' and selected != '2':
         selected = select_num()
    
    clear_main()
    if selected == '1':
        append_output('Enter location:', 0, 10)
        function, expression = get_expression(character_array, shift_character_array, 0, line=20)
        city = ''.join(expression)
    elif selected == '2':
        append_output('Detecting...', 0, 10)
        city = auto_detect_location()
        
    get_weather(city)
    unload('urequests')
    while True:
        selected = select_num()
        if selected == 'MODE':
            return ''
