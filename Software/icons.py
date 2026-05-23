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

# Same outer arcs, X replaces inner arcs
NO_WIFI = [
    0b0111111110,  # row 0 — outer arc top
    0b1000000001,  # row 1 — outer arc sides
    0b0011111100,  # row 2 — middle arc top
    0b0110000110,  # row 3 — X top arms
    0b0000110000,  # row 4 — X centre
    0b0000110000,  # row 5 — X centre
    0b0110000110,  # row 6 — X bottom arms
    0b0000000000,  # row 7
    0b0000000000,  # row 8
    0b0000000000,  # row 9
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

# oled.clear()
# draw_icon(oled, WIFI, 0, 0)
# draw_icon(oled, NO_WIFI, 11, 0)
# draw_icon(oled, SHIFT, 22, 0)
# oled.show()