from OLED import *
from machine import Pin
import time
from icons import add_icon, NO_WIFI, SHIFT, WIFI, ALPHA, NUMERICAL

LED = Pin('LED', Pin.OUT)
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
                  ['0', '.', '0', 'MODE', 'EXE']]

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
    if array == calculator_array:
        oled.rect(95, 0, 10, 7, 0, fill=True)
        oled.show()
        add_icon(oled, NUMERICAL, 95, 0)
    
    if array == character_array:
        oled.rect(95, 0, 10, 7, 0, fill=True)
        oled.show()
        add_icon(oled, ALPHA, 95, 0)
    
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
                return 'WiFi', None
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
