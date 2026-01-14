import sys

if sys.implementation.name == "circuitpython":
	import board
else:
	import mock_board as board

from digitalio import DigitalInOut, Direction, Pull

import usb_hid
from adafruit_hid.keyboard import Keyboard

from keycodes import AnsiKey
from communication import recv

import time

keyboard = Keyboard(usb_hid.devices)

def read_keys() -> list[bool]:
	pass

def handle_keyboard_logic() -> list[tuple]:
	pass

while True:
	right_keys = recv()
	left_keys = read_keys()
	key_to_press = handle_keyboard_logic()
	keyboard.press(key_to_press)
	keyboard.release(key_to_press)