import sys

if sys.implementation.name == "circuitpython":
	import board
else:
	import mock_board as board

from digitalio import DigitalInOut, Direction, Pull

import usb_hid
from adafruit_hid.keyboard import Keyboard

from keycodes import AnsiKey
from communication import *

import time

keyboard = Keyboard(usb_hid.devices)

comm_pin = DigitalInOut(board.GP2)
comm_pin.direction = Direction.INPUT

def recv() -> list[bool]:
	wait_for_segment_send()
	sleep_us(bit_duration * 0.5) # ensures we don't read before written
	
	keys = []
	for _ in range(num_buttons):
		keys.append(comm_pin.value)
		sleep_us(bit_duration)
	return keys

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