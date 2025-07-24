import board
import digitalio
import storage
import usb_hid

from utils import hide


def enter_programming_mode():
    storage.enable_usb_drive()
    hide(False, False)

def enter_payload_mode():
    usb_hid.enable((usb_hid.Device.KEYBOARD,))
    storage.disable_usb_drive()
    hide(True, True)

btn = digitalio.DigitalInOut(board.GP25)                                    
btn.direction = digitalio.Direction.INPUT                                   
btn.pull = digitalio.Pull.UP

if not btn.value:
    enter_programming_mode()
else:
    enter_payload_mode()