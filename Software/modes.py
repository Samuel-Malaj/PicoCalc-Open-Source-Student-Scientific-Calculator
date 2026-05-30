import uasyncio as asyncio
from Calculate import calculate
from inputs import *
import time
from OLED import *
from WiFi import *
import urequests
import socket
from icons import *

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
    
    while selected != 'MODE' and not winner:
        # X's turn
        selected = select_num(1)
        if selected == 'MODE':
            break
        else:
            end = False
            while (not selected.isdigit() or selected in x_positions or selected in o_positions) and end == False:
                selected = select_num(1)
                if selected == 'MODE':
                    end = True
                    break
        if selected == 'MODE':
            break
        position = positions[int(selected)-1]
        x_positions.append(int(selected))
        draw_icon(oled, x_icon, 21, position[0], position[1])
        oled.show()
        
        print('x:', x_positions)
        if check_winner(x_positions):
            draw_icon(oled, tic_tac_toe_grid, 64, 0, 0)
            oled.text('X Wins!', 65, 32)
            oled.show()
            time.sleep(2)
            winner = True
             
        # O's turn
        selected = select_num(1)
        if selected == 'MODE':
            break
        else:
            end = False
            while (not selected.isdigit() or selected in x_positions or selected in o_positions) and end == False:
                selected = select_num(1)
                if selected == 'MODE':
                    end = True
                    break
        if selected == 'MODE':
            break
        position = positions[int(selected)-1]
        o_positions.append(int(selected))
        draw_icon(oled, o_icon, 21, position[0], position[1])
        oled.show()
        
        if check_winner(o_positions):
            draw_icon(oled, tic_tac_toe_grid, 64, 0, 0)
            oled.text('O Wins!', 65, 32)
            oled.show()
            time.sleep(2)
            winner = True
            
            
games = ['Tic Tac Toe', 'Pong', '67 game']
def game_select():
    clear_mode_line()
    clear_main()
    append_output('Games:', 0, 0)
    for num, game in enumerate(games):
        append_output(str(num+1)+':'+game, 0, 10+(num*10))
    
    selected = len(games)+1
    while int(selected) >= len(games) or not str(selected).isdigit():
        selected = select_num(1)
        if selected == 'MODE':
            return ''
        
    game = games[int(selected)-1]
    
    if game == 'Tic Tac Toe':
        Tic_Tac_Toe()
