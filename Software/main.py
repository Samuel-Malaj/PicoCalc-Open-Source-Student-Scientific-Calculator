from machine import Pin
import time
from Calculate import calculate

expression = []
# defining row pins
R1 = Pin(0, Pin.OUT)
R2 = Pin(1, Pin.OUT)
R3 = Pin(2, Pin.OUT)
R4 = Pin(3, Pin.OUT)
R5 = Pin(4, Pin.OUT)
R6 = Pin(5, Pin.OUT)
R7 = Pin(6, Pin.OUT)

# defining column pins
C1 = Pin(7, Pin.IN, Pin.PULL_DOWN)
C2 = Pin(8, Pin.IN, Pin.PULL_DOWN)
C3 = Pin(9, Pin.IN, Pin.PULL_DOWN)
C4 = Pin(10, Pin.IN, Pin.PULL_DOWN)
C5 = Pin(11, Pin.IN, Pin.PULL_DOWN)
C6 = Pin(12, Pin.IN, Pin.PULL_DOWN)

# sorts rows and columns into list
rows = [R1, R2, R3, R4, R5, R6, R7]
columns = [C1, C2, C3, C4, C5, C6]

inputs = [['1', '2', '3'], 
['4', '5', '6'], 
['7', '8', '9'],
['+', '-', '0'], 
['x', '/', 'exe']]
# listening for button presses
def listen():
    while True:
        for row_num, row in enumerate(rows): 
            row.value(1) 
            for column_num, column in enumerate(columns):
                if column.value() == 1:
                    print('X: ', column_num, 'Y: ', row_num)
                    return column_num, row_num
                    time.sleep(1)

                else:
                    print('No Button')

            row.value(0)
while True:    
    x, y = listen()
    char = inputs[y][x]
    print(char)
    if char != 'exe':
        expression.append(char)
        print(expression)

    if char == 'exe':
        answer = calculate(expression)
        print(answer)
        expression = []

    time.sleep(1)
