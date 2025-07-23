# CIRCUITDUCKY
A [circuitpython](https://github.com/adafruit/circuitpython) based implementation of a rubber ducky.

# Installing

The included build.py should automatically flash your board, install the required ([custom](https://github.com/nopro263/circuitpython)) firmware and copy the code in this repository.

## Why does it need a custom build of circuitpython?
It is not possible for a program running on circuitpython to change its usb state after boot.py has been run. The custom port enables these features by disabling the usb-stack, changing the required attributes and reinitializes the usb-stack. It also creates a second partition for storing data that can be accessed when the ducky is operational. \
With all that said, you should (eventually) be able to run this code without the custom build, but then you can't enable the storage attackmode.

# Note
The firmware and code have only been tested on an orpheus-pico-v1 all other board are currently not supported.