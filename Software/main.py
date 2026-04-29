from machine import Pin
import time
from Calculate import calculate

LED = Pin('LED', Pin.OUT)
LED.value(1)

Power = 0xE0E040BF
Vol_Down = 0xE0E0D02F
Vol_Up = 0xE0E0E01F
Enter = 0xE0E016E9

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

FUNCTIONS = ['POWER', 'ANS', 'DEL', 'AC', 'MODE', 'EXE']

calculator_array = [['POWER', '#', '#', '#', '#', '#'],
                  ['#', '/', '#', '^', '^', '#'],
                  ['ANS', 'sin(', 'cos(', 'tan(', '(', ')'],
                  ['7', '8', '9', 'DEL', 'AC'],
                  ['4', '5', '6', 'x', '/'],
                  ['1', '2', '3', '+', '-'],
                  ['0', '.', '#', 'MODE', 'EXE']]

expression = []
ANS = 0

def listen():
    while True:
        for row_num, row in enumerate(rows):
            row.value(1)
            for col_num, col in enumerate(columns):
                if col.value() == 1:
                    row.value(0)        # turn off before returning
                    time.sleep_ms(200)  # debounce
                    return col_num, row_num
            row.value(0)
        time.sleep_ms(10)

while True:
    x, y = listen()
    button = calculator_array[y][x]
    
    if button in FUNCTIONS:
        if button == 'EXE':
            ANS = calculate(expression)
            print(ANS)
            
        if button == 'ANS':
            expression.append(ANS)
            
        if button == 'AC':
            expression = []
            
        if button == 'DEL':
            if len(expression) >= 1:
                expression.pop()
    
    else:
        expression.append(button)
    
    print(expression)
