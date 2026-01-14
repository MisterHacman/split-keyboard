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

led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT

switch1 = DigitalInOut(board.GP3)
switch1.direction = Direction.INPUT
switch1.pull = Pull.UP

switch2 = DigitalInOut(board.GP8)
switch2.direction = Direction.INPUT
switch2.pull = Pull.UP

keyboard = Keyboard(usb_hid.devices)

keys1 = AnsiKey._0
keys2 = AnsiKey.A

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