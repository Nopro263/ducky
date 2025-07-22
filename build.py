import argparse
import os
import sys
import enum
import urllib.request
import shutil
import time

class OS(enum.IntEnum):
    UNKNOWN = 0
    BOOTLOADER = 1
    CIRCUITPYTHON = 2
    CIRCUITDUCKY = 3

def os_detect(device: str) -> bool:
    if device.endswith(os.path.sep):
        device = device[:-1]
    
    files = os.listdir(device)
    dirname = os.path.dirname(device)
    devicename = os.path.basename(device)

    print(dirname, devicename)

    if "INFO_UF2.TXT" in files and len(files) == 2:
        return OS.BOOTLOADER

    if os.path.exists(os.path.join(dirname, "DUCKY")):
        return OS.CIRCUITDUCKY
    
    if ("code.py", "boot_out.txt") in files:
        return OS.CIRCUITPYTHON 

    return OS.UNKNOWN


def flash_device(device: str):
    print("downloading firmware.uf2")
    file,m = urllib.request.urlretrieve("https://github.com/Nopro263/ducky/releases/latest/download/firmware.uf2")
    print("writing firmware.uf2")
    shutil.copyfile(file, os.path.join(device, "firmware.uf2"))

    for i in range(10):
        if not os.path.exists(device):
            print()
            wait_for_remount(os.path.dirname(device))
            return
        
        print("waiting for unmount" + "." * (i % 4))
        time.sleep(1)
    
    error("Device did not unmount after 10s")

def wait_for_remount(dir: str):
    device = os.path.join(dir, "CIRCUITPY")

    for i in range(10):
        if os.path.exists(device):
            print()
            copy_to_device(device)
            return
        
        print("waiting for remount" + "." * (i % 4))
        time.sleep(1)
    
    error("Device did not remount after 10s")

def copy_to_device(device: str):
    for file in os.listdir(device):
        if file.startswith("."):
            continue
        if os.path.isdir(file):
            shutil.rmtree(file)
        else:
            os.remove(file)

    shutil.copytree("src", device, dirs_exist_ok=True)
    shutil.copytree("lib", os.path.join(device, "lib"))


def error(msg: str):
    print(msg, file=sys.stderr)
    exit(1)

def warn(msg: str):
    print(msg)

def ask(msg: str) -> bool:
    msg += " [y/n]: "
    if args.yes:
        print(msg, end="")
        print("y")
        return True
    
    a = input(msg).lower()

    if a == "y":
        return True
    return False

parser = argparse.ArgumentParser(
    description="A build system for copying the correct files to the correct device and (optionally) setup the required firmware"
)
parser.add_argument("--drive", help="the drive of the connected device", required=True)
parser.add_argument("-y", "--yes", help="accept all questions", required=False, action="store_true")

args = parser.parse_args()

drive: str = args.drive

if not os.path.exists(drive):
    error("The specified device was not found")

detected_os = os_detect(drive)

if detected_os == OS.UNKNOWN:
    error("The OS-type can not be identified")

if detected_os == OS.BOOTLOADER:
    warn("The device has not been flashed with circuitpython.")
    if ask("Flash with https://github.com/Nopro263/ducky?"):
        flash_device(drive)
    else:
        exit(1)

if detected_os == OS.CIRCUITPYTHON:
    warn("You are using an unsupported port of circuitpython.\nConsider using https://github.com/Nopro263/ducky to receive support for the ATTACKMODE command")
    if not ask("Continue?"):
        exit(1)
    copy_to_device(drive)

if detected_os == OS.CIRCUITDUCKY:
    copy_to_device(drive)