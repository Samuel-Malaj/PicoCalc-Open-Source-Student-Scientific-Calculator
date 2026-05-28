from machine import I2C, Pin
from ssd1309 import SSD1309

oled = SSD1309(sda=16, scl=17, addr=0x3D)

# Classic arc design — outer arc, middle arc, inner arc, dot
WIFI = [
    0b0111111110,  # row 0 — outer arc top
    0b1000000001,  # row 1 — outer arc sides
    0b0011111100,  # row 2 — middle arc top
    0b0100000010,  # row 3 — middle arc sides
    0b0001111000,  # row 4 — inner arc top
    0b0010000100,  # row 5 — inner arc sides
    0b0000110000,  # row 6 — dot
    0b0000110000,  # row 7 — dot
    0b0000000000,  # row 8
    0b0000000000,  # row 9
]

SHIFT = [
    0b1011111101,
    0b1011000001,
    0b1011000001,
    0b1011111101,
    0b1000001101,
    0b1000001101,
    0b1011111101,
]

NO_WIFI = [
    0b0111111110,  # row 0 — outer arc top
    0b1011001101,  # row 1 — outer arc sides
    0b0011111100,  # row 2 — middle arc top
    0b0100110010,  # row 3 — middle arc sides
    0b0001111000,  # row 4 — inner arc top
    0b0011001100,  # row 5 — inner arc sides
    0b0110110110,  # row 6 — dot
    0b0000110000,  # row 7 — dot
    0b0000000000,  # row 8
    0b0000000000,  # row 9
]

ALPHA = [
    0b1000110001,  # row 1 — A top peak
    0b1001111001,  # row 2
    0b1011001101,  # row 3 — A crossbar
    0b1011001101,  # row 4 — A legs
    0b1011111101,  # row 5
    0b1010000101,  # row 6
    0b1010000101,  # row 7 — side borders
    0b1000000001,  # row 8
]

NUMERICAL = [
    0b1000110001,
    0b1011110001,
    0b1000110001,
    0b1000110001,
    0b1000110001, 
    0b1000110001, 
    0b1011111101, 
    0b1011111101,  
]

def draw_icon(oled, icon, x, y):
    width = 10
    for row, bits in enumerate(icon):
        for col in range(width):
            pixel = (bits >> (width - 1 - col)) & 1
            oled.pixel(x + col, y + row, pixel)

def add_icon(oled, icon, x, y):
    draw_icon(oled, icon, x, y)
    oled.show()

