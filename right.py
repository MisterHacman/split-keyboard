import sys

if sys.implementation.name == "circuitpython":
	import board
else:
	import mock_board as board

from digitalio import DigitalInOut, Direction, Pull

from keycodes import AnsiKey
from communication import *

import time

comm_pin = DigitalInOut(board.GP2)
comm_pin.direction = Direction.OUTPUT

def send(bits: list[bool]): # only `num_buttons` bits will be written
	wait_for_segment_send()

	for i in range(num_buttons):
		comm_pin.value = bits[i]
		sleep_us(bit_duration)

def read_keys() -> list[bool]:
	pass

while True:
	send(read_keys())
