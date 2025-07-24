import neopixel_write
import digitalio

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