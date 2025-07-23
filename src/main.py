import board
import digitalio
import time
import unsafe

def hide(internal, saves):
    try:
        unsafe.usb_deinit()
        unsafe.usb_hide(internal, saves)
    finally:
        unsafe.usb_init()

btn = digitalio.DigitalInOut(board.GP25)                                    
btn.direction = digitalio.Direction.INPUT                                   
btn.pull = digitalio.Pull.UP

state = None
last_update = 0

def set_state(is_long_press: bool):
    global state, last_update
    if is_long_press == state and time.monotonic_ns() - last_update < 500000000:
        return
    
    state = is_long_press
    last_update = time.monotonic_ns()

    if is_long_press:
        print("\n\nlong hold - opening DUCKY\n\n")
        hide(True, False)
    else:
        print("\n\ndouble press - opening CIRCUITPY\n\n")
        hide(False, True)

stats_last_started_pressing = 0
stats_last_stopped_pressing = 0

_prev_state = None
while True:
    v = btn.value
    if v != _prev_state:
        if v:
            stats_last_stopped_pressing = time.monotonic_ns()
        else:
            if time.monotonic_ns() - stats_last_started_pressing < 1000000000:
                set_state(False)
            stats_last_started_pressing = time.monotonic_ns()

        _prev_state = v
    
    if not v and time.monotonic_ns() - stats_last_started_pressing > 1000000000:
        set_state(True)
    
