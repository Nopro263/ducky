import usb_hid

from adafruit_hid.keyboard import Keyboard as _Keyboard

from layouts.keyboard_layout_win_fr import KeyboardLayout as LayoutFR
from layouts.keyboard_layout_win_de import KeyboardLayout as LayoutDE
from layouts.keyboard_layout_win_cz import KeyboardLayout as LayoutCZ
from layouts.keyboard_layout_win_da import KeyboardLayout as LayoutDA
from layouts.keyboard_layout_win_es import KeyboardLayout as LayoutES
from layouts.keyboard_layout_win_hu import KeyboardLayout as LayoutHU
from layouts.keyboard_layout_win_br import KeyboardLayout as LayoutBR
from layouts.keyboard_layout_win_it import KeyboardLayout as LayoutIT
from layouts.keyboard_layout_win_po import KeyboardLayout as LayoutPO
from layouts.keyboard_layout_win_sw import KeyboardLayout as LayoutSW
from layouts.keyboard_layout_win_tr import KeyboardLayout as LayoutTR
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS as LayoutUS

from layouts.keycode_win_br import Keycode as KeycodeBR
from layouts.keycode_win_cz import Keycode as KeycodeCZ
from layouts.keycode_win_da import Keycode as KeycodeDA
from layouts.keycode_win_de import Keycode as KeycodeDE
from layouts.keycode_win_es import Keycode as KeycodeES
from layouts.keycode_win_fr import Keycode as KeycodeFR
from layouts.keycode_win_hu import Keycode as KeycodeHU
from layouts.keycode_win_it import Keycode as KeycodeIT
from layouts.keycode_win_po import Keycode as KeycodePO
from layouts.keycode_win_sw import Keycode as KeycodeSW
from layouts.keycode_win_tr import Keycode as KeycodeTR
from adafruit_hid.keycode import Keycode as KeycodeUS

class Keyboard:
    layouts = {
        "fr": LayoutFR,
        "de": LayoutDE,
        "cz": LayoutCZ,
        "da": LayoutDA,
        "es": LayoutES,
        "hu": LayoutHU,
        "it": LayoutIT,
        "po": LayoutPO,
        "sw": LayoutSW,
        "tr": LayoutTR,
        "us": LayoutUS,
        "br": LayoutBR
    }
    keycodes = {
        "fr": KeycodeFR,
        "de": KeycodeDE,
        "cz": KeycodeCZ,
        "da": KeycodeDA,
        "es": KeycodeES,
        "hu": KeycodeHU,
        "it": KeycodeIT,
        "po": KeycodePO,
        "sw": KeycodeSW,
        "tr": KeycodeTR,
        "us": KeycodeUS,
        "br": KeycodeBR
    }

    def __init__(self, layout = "us"):
        self.keyboard = _Keyboard(usb_hid.devices)
        self.layout = None
        self.keycode = None

        self.set_layout(layout)
    
    def set_layout(self, layout):
        self.layout = Keyboard.layouts[layout](self.keyboard)
        self.keycode = Keyboard.layouts[layout]
    
    def write(self, text):
        self.layout.write(text)
    
    def hold(self, button):
        self.keyboard.press(getattr(self.keycode,button))
    
    def release(self, button):
        self.keyboard.release(getattr(self.keycode,button))