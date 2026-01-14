import sys

if sys.implementation.name == "circuitpython":
	import board
else:
	import mock_board as board

from digitalio import DigitalInOut, Direction, Pull

from keycodes import AnsiKey
from communication import send

import time

def read_keys() -> list[bool]:
	pass

while True:
	send(read_keys())
