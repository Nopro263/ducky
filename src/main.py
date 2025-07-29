import board
import digitalio
import time
import os

from utils import neopixel_init, neopixel_show, error
from layout_manager import Keyboard

btn = digitalio.DigitalInOut(board.GP25)                                    
btn.direction = digitalio.Direction.INPUT                                   
btn.pull = digitalio.Pull.UP

neopixel_init(board.GP24)
neopixel_show(0,0,0)

keyboard = Keyboard()

def read_int_or_var(value):
    if value.startswith("$"):
        raise AssertionError("VARs not implemented")
    else:
        return int(value)

def run_file(file):
    print()
    line_handler = [] # a stack of callables
    line_count = 0

    with open("/scripts/" + file) as f:
        for line in f.readlines():
            line = line[:-1] # readlines does not strip \n

            try:
                line_count += 1
                if not line:
                    continue

                parts = line.split(" ", 1)
                command = parts[0].upper()
                if len(parts) > 1:
                    args_string = parts[1]
                    args = parts[1].split(" ")
                else:
                    args_string = ""
                    args = []

                if line_handler:
                    line_handler[-1]()
                    continue
                
                if command == "REM":
                    continue #Do Nothing
                elif command == "REM_BLOCK":
                    def rem_handler():
                        if command == "END_REM":
                            line_handler.pop()

                    line_handler.append(rem_handler)
                elif command == "STRING":
                    if args_string:
                        keyboard.write(args_string.strip())
                    else:
                        def string_handler():
                            if command == "END_STRING":
                                line_handler.pop()
                            else:
                                keyboard.write(line.lstrip())
                        line_handler.append(string_handler)
        
                elif command == "STRINGLN":
                    if args_string:
                        keyboard.write(args_string.strip() + "\n")
                    else:
                        def stringln_handler():
                            if command == "END_STRINGLN":
                                line_handler.pop()
                            else:
                                keyboard.write((line[1:] if line[0] == "\t" else line) + "\n")
                        line_handler.append(stringln_handler)
                elif command == "DELAY":
                    t = read_int_or_var(args[0])
                    time.sleep(t/1000.0)
                ### MORE COMMANDS HERE ###
                else:
                    if command == "INJECT_MOD":
                        raw = args
                    else:
                        raw = [command] + args
                    buttons = keyboard.get_codes(raw)
                    keyboard.hold(buttons)
                    time.sleep(0.050)
                    keyboard.release(buttons)
                    continue
                    raise Exception("Unknown command " + command)
            
            except Exception as e:
                error(
                    description="Error " + str(e) + " in line " + str(line_count) + ":\n" + (line if len(line) <= 50 else line[:7] + "..."),
                    exit=False
                )
                raise e
                
                



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

for script in os.listdir("/scripts"):
    if script.endswith(".ducky"):
        run_file(script)
        break
else:
    error("No scripts were found in /scripts")
