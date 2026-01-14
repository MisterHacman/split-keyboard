import sys

if sys.implementation.name == "circuitpython":
	import board
else:
	import mock_board as board

from digitalio import DigitalInOut, Direction, Pull

from keycodes import AnsiKey
from communication import send

import time

led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT

switch1 = DigitalInOut(board.GP3)
switch1.direction = Direction.INPUT
switch1.pull = Pull.UP

switch2 = DigitalInOut(board.GP8)
switch2.direction = Direction.INPUT
switch2.pull = Pull.UP

keys1 = AnsiKey._0
keys2 = AnsiKey.A

def read_keys() -> list[bool]:
	pass

while True:
	send(read_keys())
