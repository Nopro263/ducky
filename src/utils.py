import neopixel_write
import digitalio
import time
import os
import sys

neopixel_pin = None

def hide(internal, saves):
    try:
        import unsafe
        try:
            unsafe.usb_deinit()
            unsafe.usb_hide(internal, saves)
        finally:
            unsafe.usb_init()
    except ImportError:
        pass

def neopixel_init(pin):
    global neopixel_pin
    neopixel_pin = digitalio.DigitalInOut(pin)
    neopixel_pin.direction = digitalio.Direction.OUTPUT

def neopixel_show(r,g,b):
    global neopixel_pin
    color = bytearray([g, r, b])
    neopixel_write.neopixel_write(neopixel_pin, color)

def error(description, exit=False):
    neopixel_show(100,0,0)
    time.sleep(.1)
    neopixel_show(0,0,0)
    time.sleep(.2)
    neopixel_show(100,0,0)
    time.sleep(.1)
    neopixel_show(0,0,0)

    n = 1

    for file in os.listdir("/"):
        if file.startswith("error_report_"):
            i = int(file[13:])

            if i > n:
                n = i+1
    
    name = "error_report_" + str(n) + ".txt"

    with open(name, "w") as f:
        f.write(description)
    
    if exit:
        sys.exit(1)
