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

vars = {}
functions = {}
function_stack = []

button_function = None
button_enabled = True
executing_button = False

sleep_start = 0
sleep_duration = 0
sleeping = False

def read_int_or_var(value):
    if value.startswith("$"):
        return vars[value]
    else:
        return int(value)

def execute_calculation(args):
    return read_int_or_var(args[0]) # other stuff supported in the future

def run_file(file):
    global button_function, button_enabled, executing_button, sleep_start, sleep_duration, sleeping
    print()
    line_handler = [] # a stack of callables
    line_count = 0

    with open("/scripts/" + file) as f:
        lines = f.readlines()
        while line_count < len(lines):
            line = lines[line_count][:-1] # readlines does not strip \n
            print(line_count)
            try:
                line_count += 1
                if not line:
                    continue

                parts = line.lstrip().split(" ", 1)
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
                #print(not btn.value,button_enabled,button_function,executing_button)
                if not btn.value and button_enabled and button_function and not executing_button:
                    executing_button = True
                    function_stack.append(line_count-1)
                    line_count = button_function
                    continue

                if not executing_button:
                    if sleep_start + sleep_duration > time.monotonic_ns():
                        time.sleep(0.001)
                        line_count -= 1
                        continue
                    elif sleeping:
                        sleeping = False
                        line_count += 1
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
                    sleep_duration = t * 1000000
                    sleep_start = time.monotonic_ns()
                    sleeping = True
                    line_count -= 1
                    continue
                
                elif command == "WAIT_FOR_BUTTON_PRESS":
                    while btn.value:
                        pass
                
                elif command == "VAR":
                    if args[1] != "=":
                        raise AttributeError("???")
                    
                    if args[2].upper() == "TRUE":
                        args[2] = "1"
                    elif args[2].upper() == "FALSE":
                        args[2] = "0"

                    if args[0] in vars:
                        raise ArithmeticError("variable already declared")
                    
                    vars[args[0]] = read_int_or_var(args[2])
                elif command == "FUNCTION":
                    function_name = args[0][:-2]
                    function_entry = line_count
                    def function_handler():
                        if command == "END_FUNCTION":
                            functions[function_name] = function_entry
                            line_handler.pop()
                    line_handler.append(function_handler)
                elif command == "END_FUNCTION":
                    line_count = function_stack.pop()
                    continue

                elif command == "BUTTON_DEF":
                    function_entry = line_count
                    def function_handler():
                        global button_function
                        if command == "END_BUTTON":
                            button_function = function_entry
                            line_handler.pop()
                    line_handler.append(function_handler)
                elif command == "END_BUTTON":
                    executing_button = False
                    line_count = function_stack.pop()
                    continue
                elif command == "DISABLE_BUTTON":
                    button_enabled = False
                elif command == "ENABLE_BUTTON":
                    button_enabled = True
                ### MORE COMMANDS HERE ###
                elif command.startswith("$"):
                    if args[0] != "=":
                        raise AttributeError("???")
                    vars[parts[0]] = execute_calculation(args[1:])
                elif command.endswith("()"): # raw function call
                    function_stack.append(line_count)
                    line_count = functions[parts[0][:-2]]
                    continue

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
