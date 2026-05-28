import lowpower
import time
import machine
from machine import Pin

def power_off():
    safety_pin = machine.Pin(1, machine.Pin.IN, machine.Pin.PULL_UP)
    if safety_pin.value() == 0:
        print("Safety mode: Sleep disabled. Connect GP1 to 3V3 to allow sleep.")
        while True: time.sleep(1)

    button = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_UP)
    indicator = machine.Pin(7, machine.Pin.OUT, value=0)

    LED = Pin('LED', Pin.OUT)
    LED.value(1)
    LED.value(0)
    lowpower.dormant_until_pin(0)