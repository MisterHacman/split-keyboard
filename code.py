import sys

if sys.implementation.name == "circuitpython":
	import board
else:
	import mock_board as board

from digitalio import DigitalInOut, Direction, Pull

import usb_hid
from adafruit_hid.keyboard import Keyboard

from keycodes import AnsiKey

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

while True:
	if not switch1.value:
		keyboard.press(*keys1)
	else:
		keyboard.release(*keys1)
	if not switch2.value:
		keyboard.press(*keys2)
	else:
		keyboard.release(*keys2)
	time.sleep(0.01)