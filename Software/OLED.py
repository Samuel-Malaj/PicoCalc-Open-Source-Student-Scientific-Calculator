from machine import I2C, Pin
from ssd1309 import SSD1309
import time

i2c = I2C(0, sda=Pin(16), scl=Pin(17), freq=400_000)
oled = SSD1309(sda=16, scl=17, addr=0x3D)

def clear_mode_line():
    oled.rect(0, 0, 106, 10, 0, fill=True)
    oled.show()

def clear_all():
    oled.clear()
    oled.show()
    
def clear_main():
    oled.rect(0, 10, 128, 54, 0, fill=True)
    oled.show()
    
def display_input(text):
    oled.clear()
    oled.text(text, 0, 10)
    oled.show()
    
def display_output(text):
    oled.clear()
    oled.text(text, 0, 54)
    oled.show()
    
def append_output(text, x, y):
    oled.text(text, x, y)
    oled.show()
    
def display_line(text, x, y):
    oled.clear()
    oled.text(text, x, y)
    oled.show()

#display_output('hello')
# while True:
#     print([hex(d) for d in i2c.scan()])
#     time.sleep(1)
#     try:
#         oled = SSD1309(sda=16, scl=17, addr=0x3D)
#         display_output('hello')
#     except Exception as e:
#         print(e)
