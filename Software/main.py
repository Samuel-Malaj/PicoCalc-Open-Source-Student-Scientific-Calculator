from machine import Pin
import time

# defining row pins
R1 = Pin(0, Pin.OUT)
R2 = Pin(1, Pin.OUT)
R3 = Pin(2, Pin.OUT)
R4 = Pin(3, Pin.OUT)
R5 = Pin(4, Pin.OUT)
R6 = Pin(5, Pin.OUT)
R7 = Pin(6, Pin.OUT)

# defining column pins
C1 = Pin(4, Pin.IN, Pin.PULL_DOWN)
C2 = Pin(5, Pin.IN, Pin.PULL_DOWN)
C3 = Pin(6, Pin.IN, Pin.PULL_DOWN)
C4 = Pin(7, Pin.IN, Pin.PULL_DOWN)
C5 = Pin(8, Pin.IN, Pin.PULL_DOWN)
C6 = Pin(9, Pin.IN, Pin.PULL_DOWN)

# sorts rows and columns into list
rows = [R1, R2, R3, R4, R5, R6, R7]
columns = [C1, C2, C3, C4, C5, C6]

# listening for button presses
while True:
    for row_num, row in enumerate(rows): 
        row.value(1) 
        for column_num, column in enumerate(columns):
            if column.value() == 1:
                print('X: ', column_num, 'Y: ', row_num)
                time.sleep(1)

            else:
                print('No Button')

        row.value(0)
