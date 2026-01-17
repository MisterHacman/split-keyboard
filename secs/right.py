import sys

if sys.implementation.name == "circuitpython":
	import board
else:
	import mock_board as board

from digitalio import DigitalInOut, Direction, Pull

from communication import *

from time import sleep, monotonic, monotonic_ns

comm_pin = DigitalInOut(board.GP2)
comm_pin.direction = Direction.OUTPUT

origin_time = 0

def send_connect_signal():
	global origin_time
	comm_pin.value = False
	sleep(bit_duration)
	comm_pin.value = True
	sleep(connect_signal_length)
	comm_pin.value = False
	origin_time = monotonic() + bit_duration # we wait for the zero-bit to finish

def send(bits: list[bool]): # only `num_buttons` bits will be written
	wait_for_segment_send(origin_time)

	for i in range(num_buttons):
		print(i, bits[i])
		comm_pin.value = bits[i]
		sleep(bit_duration)
	comm_pin.value = False

def read_keys() -> list[bool]:
	return [False, True, True, True, True, True, True, True, True, False]

send_connect_signal()
while True:
	send(read_keys())