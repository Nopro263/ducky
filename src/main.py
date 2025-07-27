import board
import digitalio
import time
import os

from utils import neopixel_init, neopixel_show, error

btn = digitalio.DigitalInOut(board.GP25)                                    
btn.direction = digitalio.Direction.INPUT                                   
btn.pull = digitalio.Pull.UP

neopixel_init(board.GP24)
neopixel_show(0,0,0)

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
                    args = parts[1].split(" ")
                else:
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
                ### MORE COMMANDS HERE ###
                else:
                    raise Exception("Unknown command " + command)
            
            except Exception as e:
                error(
                    description="Error " + str(e) + " in line " + str(line_count) + ":\n" + line if len(line) <= 10 else line[:7] + "...",
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
