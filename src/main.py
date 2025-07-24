import board
import digitalio
import time

from utils import neopixel_init, neopixel_show

btn = digitalio.DigitalInOut(board.GP25)                                    
btn.direction = digitalio.Direction.INPUT                                   
btn.pull = digitalio.Pull.UP

neopixel_init(board.GP24)
neopixel_show(0,0,0)

if not btn.value:
    import sys

    neopixel_show(0,100,0)
    time.sleep(.1)
    neopixel_show(0,0,0)
    time.sleep(.2)
    neopixel_show(0,100,0)
    time.sleep(.1)
    neopixel_show(0,0,0)

    sys.exit(1)